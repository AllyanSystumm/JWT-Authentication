from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from .schemas import UserCreate
from .crud import create_user, get_user
from .utils import hash_password
from .schemas import UserLogin
from .auth import create_access_token
from .utils import verify_password
from .auth import verify_token

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """
    Ye function database session create karta hai
    aur request complete hone ke baad automatically close karta hai
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    New user create karta hai database me

    Steps:
    1. Check karta hai user already exist karta hai ya nahi
    2. Password hash karta hai
    3. Database me save karta hai
    """

    existing_user = get_user(db, user.username)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    hashed_password = hash_password(user.password)

    create_user(
        db,
        user.username,
        user.email,
        hashed_password
    )

    return {"message": "User created successfully"}
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    User login endpoint

    Steps:
    1. Username check
    2. Password verify
    3. JWT token generate
    """

    db_user = get_user(db, user.username)

    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid username"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )

    access_token = create_access_token(
        data={"sub": db_user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Ab system:

# PostgreSQL me users table create karega
# /signup endpoint available ho jayega
# new user database me store ho sakta hai




@app.get("/profile")
def get_profile(username: str = Depends(verify_token)):
    """
    Ye protected endpoint hai

    Sirf valid JWT token se access hoga
    """

    return {
        "message": f"Welcome {username}, this is your profile"
    }