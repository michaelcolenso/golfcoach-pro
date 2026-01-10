"""
User service with business logic for user operations.

Handles user CRUD, authentication, profile management, etc.
"""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.user import User, UserProfile
from app.schemas.user import UserCreate, UserUpdate, UserProfileUpdate
from app.core.security import hash_password, verify_password, generate_tokens


class UserService:
    """Service class for user-related operations."""

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Get user by ID.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            User if found, None otherwise
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email.

        Args:
            db: Database session
            email: User email

        Returns:
            User if found, None otherwise
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user.

        Args:
            db: Database session
            user_data: User creation data

        Returns:
            Created user

        Raises:
            HTTPException: If email already exists
        """
        # Check if email already exists
        existing_user = UserService.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        # Hash password
        hashed_password = hash_password(user_data.password)

        # Create user
        db_user = User(
            email=user_data.email,
            password_hash=hashed_password,
            full_name=user_data.full_name,
        )

        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            ) from e

        # Create empty profile
        db_profile = UserProfile(user_id=db_user.id)
        db.add(db_profile)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.

        Args:
            db: Database session
            email: User email
            password: Plain text password

        Returns:
            User if authentication successful, None otherwise
        """
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def update_user(db: Session, user: User, user_update: UserUpdate) -> User:
        """
        Update user information.

        Args:
            db: Database session
            user: User to update
            user_update: Update data

        Returns:
            Updated user
        """
        # Update user fields
        if user_update.full_name is not None:
            user.full_name = user_update.full_name

        if user_update.handicap is not None:
            user.handicap = user_update.handicap

        # Update profile if provided
        if user_update.profile is not None:
            profile = user.profile
            if profile is None:
                # Create profile if it doesn't exist
                profile = UserProfile(user_id=user.id)
                db.add(profile)

            # Update profile fields
            profile_update = user_update.profile
            if profile_update.date_of_birth is not None:
                profile.date_of_birth = profile_update.date_of_birth
            if profile_update.height_cm is not None:
                profile.height_cm = profile_update.height_cm
            if profile_update.weight_kg is not None:
                profile.weight_kg = profile_update.weight_kg
            if profile_update.dominant_hand is not None:
                profile.dominant_hand = profile_update.dominant_hand
            if profile_update.primary_miss is not None:
                profile.primary_miss = profile_update.primary_miss
            if profile_update.goals is not None:
                profile.goals = profile_update.goals
            if profile_update.physical_limitations is not None:
                profile.physical_limitations = profile_update.physical_limitations

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user: User) -> None:
        """
        Delete a user.

        Args:
            db: Database session
            user: User to delete
        """
        db.delete(user)
        db.commit()

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> dict:
        """
        Register a new user and generate tokens.

        Args:
            db: Database session
            user_data: User registration data

        Returns:
            Dictionary with user and tokens
        """
        user = UserService.create_user(db, user_data)
        tokens = generate_tokens(user.id)

        return {
            "user": user,
            **tokens,
        }

    @staticmethod
    def login_user(db: Session, email: str, password: str) -> dict:
        """
        Login user and generate tokens.

        Args:
            db: Database session
            email: User email
            password: Plain text password

        Returns:
            Dictionary with user and tokens

        Raises:
            HTTPException: If credentials are invalid
        """
        user = UserService.authenticate_user(db, email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        tokens = generate_tokens(user.id)

        return {
            "user": user,
            **tokens,
        }
