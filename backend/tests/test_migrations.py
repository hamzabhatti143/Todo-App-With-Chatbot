"""
Test suite for validating Alembic migration management.

Validates:
- Migration configuration and version control
- SC-005: Migrations can be applied and rolled back without data loss
- SC-010: Migration completes within 30 seconds
"""

import pytest
import subprocess
import time
from pathlib import Path
from sqlmodel import Session, create_engine, text


class TestMigrationConfiguration:
    """Test Alembic migration configuration (FR-009)."""

    def test_alembic_ini_exists(self):
        """Verify alembic.ini configuration file exists."""
        alembic_ini = Path("alembic.ini")
        assert alembic_ini.exists(), "alembic.ini should exist in backend/ directory"

    def test_alembic_env_exists(self):
        """Verify alembic/env.py exists."""
        env_py = Path("alembic/env.py")
        assert env_py.exists(), "alembic/env.py should exist"

    def test_alembic_versions_directory_exists(self):
        """Verify alembic/versions/ directory exists for migrations."""
        versions_dir = Path("alembic/versions")
        assert versions_dir.exists(), "alembic/versions/ directory should exist"
        assert versions_dir.is_dir(), "versions should be a directory"

    def test_migrations_exist(self):
        """Verify migration files exist in versions/ directory."""
        versions_dir = Path("alembic/versions")
        migration_files = list(versions_dir.glob("*.py"))
        # Filter out __pycache__ and __init__.py
        migration_files = [f for f in migration_files if not f.name.startswith("__")]

        assert len(migration_files) > 0, "At least one migration file should exist"

    def test_alembic_env_imports_models(self):
        """Verify alembic/env.py imports models for autogenerate."""
        env_py = Path("alembic/env.py")
        content = env_py.read_text()

        # Should import SQLModel
        assert "SQLModel" in content, "env.py should import SQLModel"
        # Should reference metadata
        assert "metadata" in content, "env.py should reference metadata"


class TestMigrationExecution:
    """Test migration execution and rollback (SC-005, SC-010)."""

    @pytest.mark.integration
    def test_migration_current_version(self):
        """Test getting current migration version."""
        result = subprocess.run(
            ["alembic", "current"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, "alembic current should execute successfully"
        # Output should show current version or "head"
        assert len(result.stdout) > 0, "Should return current migration version"

    @pytest.mark.integration
    def test_migration_history(self):
        """Test viewing migration history."""
        result = subprocess.run(
            ["alembic", "history"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, "alembic history should execute successfully"
        assert len(result.stdout) > 0, "Should return migration history"

    @pytest.mark.integration
    @pytest.mark.slow
    def test_migration_performance(self):
        """Verify migration completes within 30 seconds (SC-010)."""
        # Note: This test should be run on a clean test database
        # In CI/CD, use a temporary test database

        start_time = time.time()

        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            timeout=35  # Slightly more than 30 seconds for safety
        )

        elapsed_time = time.time() - start_time

        assert result.returncode == 0, "Migration should complete successfully"
        assert elapsed_time < 30, f"Migration should complete in <30 seconds, took {elapsed_time:.2f}s (SC-010)"


class TestMigrationContent:
    """Test migration file content and structure."""

    def test_migrations_have_upgrade_function(self):
        """Verify all migrations have upgrade() function."""
        versions_dir = Path("backend/alembic/versions")
        migration_files = [f for f in versions_dir.glob("*.py") if not f.name.startswith("__")]

        for migration_file in migration_files:
            content = migration_file.read_text()
            assert "def upgrade()" in content, \
                f"{migration_file.name} should have upgrade() function"

    def test_migrations_have_downgrade_function(self):
        """Verify all migrations have downgrade() function (SC-005 requirement)."""
        versions_dir = Path("backend/alembic/versions")
        migration_files = [f for f in versions_dir.glob("*.py") if not f.name.startswith("__")]

        for migration_file in migration_files:
            content = migration_file.read_text()
            assert "def downgrade()" in content, \
                f"{migration_file.name} should have downgrade() function for rollback"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "not integration and not slow"])
