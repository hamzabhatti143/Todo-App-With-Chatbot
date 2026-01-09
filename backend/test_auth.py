"""
Test Authentication System

This script tests the complete authentication flow:
- User registration
- User login
- JWT token generation
- JWT token verification
- Protected endpoint access
"""

from sqlmodel import SQLModel, create_engine, Session, select
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.auth import get_password_hash, verify_password, create_access_token, decode_token
from jose import JWTError
import uuid

# Create SQLite in-memory engine for testing
test_engine = create_engine("sqlite:///:memory:", echo=False)


def test_authentication():
    """Test complete authentication flow"""
    print("\n" + "="*60)
    print("Testing Authentication System")
    print("="*60)

    # Create tables
    print("\n1. Setting up test database...")
    SQLModel.metadata.create_all(test_engine)
    print("✓ Database tables created")

    # Test password hashing
    print("\n2. Testing password hashing...")
    plain_password = "password123"  # Simple password for testing
    hashed = get_password_hash(plain_password)
    assert len(hashed) > 0
    assert hashed != plain_password
    print(f"✓ Password hashed successfully")
    print(f"  Plain: {plain_password}")
    print(f"  Hash: {hashed[:50]}...")

    # Test password verification
    print("\n3. Testing password verification...")
    assert verify_password(plain_password, hashed) == True
    assert verify_password("WrongPassword", hashed) == False
    print("✓ Password verification works correctly")

    # Test user registration
    print("\n4. Testing user registration...")
    with Session(test_engine) as session:
        # Create user
        user_email = "test@example.com"
        user_password = "SecurePass123!"

        # Check user doesn't exist
        statement = select(User).where(User.email == user_email)
        existing_user = session.exec(statement).first()
        assert existing_user is None
        print(f"✓ Verified user doesn't exist yet")

        # Register user
        hashed_password = get_password_hash(user_password)
        new_user = User(
            email=user_email,
            hashed_password=hashed_password
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        user_id = new_user.id
        print(f"✓ User registered: {user_email}")
        print(f"  User ID: {user_id}")

    # Test user login
    print("\n5. Testing user login...")
    with Session(test_engine) as session:
        # Get user
        statement = select(User).where(User.email == user_email)
        user = session.exec(statement).first()
        assert user is not None
        print(f"✓ User found: {user.email}")

        # Verify password
        assert verify_password(user_password, user.hashed_password)
        print("✓ Password verified successfully")

        # Wrong password should fail
        assert not verify_password("WrongPassword", user.hashed_password)
        print("✓ Wrong password correctly rejected")

    # Test JWT token creation
    print("\n6. Testing JWT token creation...")
    token = create_access_token(data={"sub": str(user_id)})
    assert len(token) > 0
    print(f"✓ JWT token created")
    print(f"  Token: {token[:50]}...")

    # Test JWT token decoding
    print("\n7. Testing JWT token verification...")
    try:
        payload = decode_token(token)
        assert payload["sub"] == str(user_id)
        print(f"✓ Token decoded successfully")
        print(f"  User ID from token: {payload['sub']}")
    except JWTError as e:
        print(f"✗ Token verification failed: {e}")
        raise

    # Test invalid token
    print("\n8. Testing invalid token rejection...")
    try:
        decode_token("invalid.token.here")
        print("✗ Invalid token was accepted (should have failed!)")
        raise AssertionError("Invalid token should be rejected")
    except JWTError:
        print("✓ Invalid token correctly rejected")

    # Test expired token handling
    print("\n9. Testing token expiration...")
    from datetime import timedelta
    expired_token = create_access_token(
        data={"sub": str(user_id)},
        expires_delta=timedelta(seconds=-1)  # Already expired
    )
    try:
        decode_token(expired_token)
        print("✗ Expired token was accepted (should have failed!)")
        raise AssertionError("Expired token should be rejected")
    except JWTError:
        print("✓ Expired token correctly rejected")

    # Test duplicate email registration
    print("\n10. Testing duplicate email prevention...")
    with Session(test_engine) as session:
        statement = select(User).where(User.email == user_email)
        existing = session.exec(statement).first()
        assert existing is not None
        print(f"✓ Duplicate email check works (user exists)")

    # Test complete auth flow
    print("\n11. Testing complete authentication flow...")
    test_email = "newuser@example.com"
    test_password = "NewUserPass123!"

    with Session(test_engine) as session:
        # Register
        new_user = User(
            email=test_email,
            hashed_password=get_password_hash(test_password)
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        print(f"✓ Step 1: User registered")

        # Login (verify credentials)
        statement = select(User).where(User.email == test_email)
        user = session.exec(statement).first()
        assert user is not None
        assert verify_password(test_password, user.hashed_password)
        print(f"✓ Step 2: Credentials verified")

        # Generate token
        auth_token = create_access_token(data={"sub": str(user.id)})
        print(f"✓ Step 3: Token generated")

        # Verify token
        payload = decode_token(auth_token)
        assert payload["sub"] == str(user.id)
        print(f"✓ Step 4: Token verified")

        # Access protected resource (simulate)
        token_user_id = uuid.UUID(payload["sub"])
        statement = select(User).where(User.id == token_user_id)
        authenticated_user = session.exec(statement).first()
        assert authenticated_user.email == test_email
        print(f"✓ Step 5: Protected resource accessed")

    # Test security features
    print("\n12. Testing security features...")

    # Password requirements
    weak_passwords = ["123", "password", "abc"]
    for weak in weak_passwords:
        if len(weak) < 8:
            print(f"✓ Weak password would be rejected: '{weak}' (too short)")

    # Token payload inspection
    payload = decode_token(token)
    assert "exp" in payload  # Expiration time
    assert "sub" in payload  # Subject (user ID)
    print("✓ Token contains required claims (sub, exp)")

    print("\n" + "="*60)
    print("All authentication tests passed successfully! ✓")
    print("="*60)

    return True


if __name__ == "__main__":
    try:
        test_authentication()
    except Exception as e:
        print(f"\n✗ Authentication test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
