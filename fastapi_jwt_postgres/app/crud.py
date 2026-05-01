from sqlalchemy.orm import Session
from .models import User


def get_user(db: Session, username: str):
    """
    Database se username ke basis par user fetch karta hai.

    Parameters:
    db (Session): database connection session
    username (str): login username

    Returns:
    User object agar mil jaye
    None agar user exist na kare
    """

    return db.query(User).filter(
        User.username == username
    ).first()


def create_user(
        db: Session,
        username: str,
        email: str,
        password: str
):
    """
    Database me new user create karta hai.

    Parameters:
    db (Session): database session
    username (str): user ka username
    email (str): user ka email
    password (str): hashed password

    Returns:
    created User object
    """

    user = User(
        username=username,
        email=email,
        password=password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# Ye step kya karta hai

# Ab system:

# database se user check kar sakta hai
# new user create kar sakta hai
# signup/login logic ke liye backend ready ho gaya