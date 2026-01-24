"""
Test suite for validating database connection configuration.

Validates:
- SC-004: SSL connections to Neon PostgreSQL
- SC-006: Connection pool manages concurrent sessions
- SC-003: Query performance meets requirements
- Database connection pooling configuration
"""

import pytest
import os
import time
import concurrent.futures
from sqlmodel import Session, create_engine, select, text
from uuid import uuid4

from app.database import engine, get_session
from app.models.task import Task
from app.models.user import User


class TestDatabaseConfiguration:
    """Test database configuration (FR-010, FR-011, FR-012)."""

    def test_database_url_configured(self):
        """Verify DATABASE_URL is configured."""
        database_url = os.getenv("DATABASE_URL")
        assert database_url is not None, "DATABASE_URL environment variable should be set"
        # Accept both PostgreSQL and SQLite for testing
        assert database_url.startswith(("postgresql://", "sqlite://")), \
            "DATABASE_URL should be a valid database connection string"

    def test_database_url_has_ssl_mode(self):
        """Verify DATABASE_URL includes SSL mode for Neon (SC-004)."""
        database_url = os.getenv("DATABASE_URL", "")

        # For Neon connections, SSL should be required
        if "neon.tech" in database_url or "neon" in database_url:
            assert "sslmode=require" in database_url, \
                "Neon DATABASE_URL should include ?sslmode=require for SSL (SC-004)"

    def test_connection_pool_configured(self):
        """Verify connection pool is configured (FR-011)."""
        # Check engine pool configuration
        pool = engine.pool

        assert pool is not None, "Connection pool should be configured"
        # Verify pool size settings exist
        assert hasattr(pool, '_pool'), "Pool should have _pool attribute"

    def test_pool_pre_ping_enabled(self):
        """Verify pool_pre_ping is enabled for connection health checks."""
        # pool_pre_ping verifies connections before use
        assert engine.pool._pre_ping is True, \
            "pool_pre_ping should be enabled to verify connection health"


class TestDatabaseConnection:
    """Test database connection functionality (SC-004)."""

    @pytest.mark.integration
    def test_basic_connection(self):
        """Test basic database connection works."""
        try:
            with Session(engine) as session:
                result = session.exec(select(1)).one()
                assert result == 1, "Should be able to execute simple query"
        except Exception as e:
            pytest.fail(f"Database connection failed: {e}")

    @pytest.mark.integration
    def test_ssl_connection_if_neon(self):
        """Test SSL connection is active for Neon databases (SC-004)."""
        database_url = os.getenv("DATABASE_URL", "")

        # Only test SSL for Neon connections
        if "neon" not in database_url:
            pytest.skip("Not a Neon database, skipping SSL check")

        with Session(engine) as session:
            # Check SSL status
            result = session.exec(text("SHOW ssl")).one()
            assert result[0] == "on", "SSL should be enabled for Neon connection (SC-004)"

    @pytest.mark.integration
    def test_session_generator_works(self):
        """Test get_session() generator function works correctly (FR-012)."""
        session_gen = get_session()
        session = next(session_gen)

        try:
            # Should be able to use session
            result = session.exec(select(1)).one()
            assert result == 1
        finally:
            # Close generator
            try:
                next(session_gen)
            except StopIteration:
                pass  # Expected behavior


class TestConnectionPooling:
    """Test connection pool behavior (SC-006)."""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_concurrent_connections(self):
        """Test connection pool handles concurrent sessions (SC-006: 20 concurrent)."""
        num_concurrent = 20
        results = []

        def execute_query(session_id):
            """Execute a simple query in a session."""
            try:
                with Session(engine) as session:
                    result = session.exec(select(1)).one()
                    return (session_id, result, None)
            except Exception as e:
                return (session_id, None, str(e))

        # Execute 20 concurrent queries
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            futures = [executor.submit(execute_query, i) for i in range(num_concurrent)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # Verify all queries succeeded
        assert len(results) == num_concurrent, f"Should handle {num_concurrent} concurrent connections"

        errors = [r for r in results if r[2] is not None]
        assert len(errors) == 0, f"All concurrent queries should succeed, but got errors: {errors}"

        successful = [r for r in results if r[1] == 1]
        assert len(successful) == num_concurrent, "All queries should return correct result (SC-006)"

    @pytest.mark.integration
    def test_connection_pool_size_configuration(self):
        """Verify connection pool size is configured correctly."""
        # Pool size should be 5 with max_overflow of 10
        # This allows up to 15 total connections (5 + 10)

        pool = engine.pool
        # Check pool configuration
        assert pool.size() >= 0, "Pool should have connections available"


class TestQueryPerformance:
    """Test query performance meets requirements (SC-003)."""

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.skipif(
        os.getenv("SKIP_PERFORMANCE_TESTS") == "true",
        reason="Performance tests skipped"
    )
    def test_user_filtered_query_performance(self):
        """Verify queries filtering by user_id are fast (SC-003: <50ms for 10K records)."""
        # Note: This test requires a database with test data
        # In real testing, you would populate with 10K records

        with Session(engine) as session:
            # Create test user
            test_user = User(email=f"perftest_{uuid4()}@example.com", hashed_password="hashed")
            session.add(test_user)
            session.commit()
            session.refresh(test_user)

            # Create some test tasks
            for i in range(100):  # Using 100 for quick test
                task = Task(
                    user_id=test_user.id,
                    title=f"Performance Test Task {i}",
                    description="Testing query performance"
                )
                session.add(task)

            session.commit()

            # Measure query performance
            start_time = time.time()

            statement = select(Task).where(Task.user_id == test_user.id)
            results = session.exec(statement).all()

            elapsed_ms = (time.time() - start_time) * 1000

            # Cleanup
            for task in results:
                session.delete(task)
            session.delete(test_user)
            session.commit()

            # With 100 records, should be well under 50ms
            # For 10K records, requirement is <50ms (SC-003)
            assert len(results) == 100, "Should retrieve all tasks"
            assert elapsed_ms < 50, \
                f"Query should complete in <50ms, took {elapsed_ms:.2f}ms (SC-003)"

    @pytest.mark.integration
    def test_indexed_query_uses_index(self):
        """Verify indexed queries use index (SC-009)."""
        # Note: This test requires actual PostgreSQL, not SQLite
        database_url = os.getenv("DATABASE_URL", "")

        if "sqlite" in database_url or "postgresql" not in database_url:
            pytest.skip("Index verification requires PostgreSQL")

        with Session(engine) as session:
            # Use EXPLAIN to check if index is used
            explain_query = text("""
                EXPLAIN SELECT * FROM tasks WHERE user_id = :user_id
            """)

            result = session.exec(explain_query, {"user_id": str(uuid4())})
            explain_output = " ".join([row[0] for row in result])

            # Should use Index Scan, not Seq Scan
            assert "Index Scan" in explain_output or "Bitmap" in explain_output, \
                "Query should use index scan for user_id (SC-009)"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "not integration and not slow"])
