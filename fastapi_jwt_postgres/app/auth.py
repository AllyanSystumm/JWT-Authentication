from jose import JWTError, jwt
"""
JWTError → token validation error handle karne ke liye use hota hai
jwt → token encode aur decode karne ke liye library object
"""


from datetime import datetime, timedelta
"""
datetime → current time lene ke liye
timedelta → future expiry time calculate karne ke liye
"""


from dotenv import load_dotenv
"""
.env file se environment variables load karne ke liye
(jese SECRET_KEY, DATABASE_URL)
"""


import os
"""
Operating system se environment variables read karne ke liye
example: os.getenv("SECRET_KEY")
"""


from pathlib import Path
"""
Project directory ka correct path locate karne ke liye
taake .env file properly load ho
"""
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends 

env_path = Path(__file__).resolve().parent.parent / ".env"
"""
Current file ka path detect karta hai
phir project root folder me .env file ka exact location set karta hai
"""


load_dotenv(dotenv_path=env_path)
"""
.env file ko memory me load karta hai
taake variables program me accessible ho jayein
"""


SECRET_KEY = os.getenv("SECRET_KEY")
"""
.env se secret key read karta hai
ye key JWT token sign karne ke liye use hoti hai
"""


ALGORITHM = os.getenv("ALGORITHM")
"""
JWT token kis algorithm se sign hoga (example: HS256)
"""


ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)
"""
Token kitni der tak valid rahega (minutes me)
example: 30 minutes
"""


def create_access_token(data: dict):
    """
    Ye function JWT access token generate karta hai.

    data: payload dictionary (usually username)
    return: encoded JWT token string
    """

    to_encode = data.copy()
    """
    Original payload ka duplicate banata hai
    taake original dictionary change na ho
    """

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    """
    Current UTC time + expiry minutes
    token expiration timestamp calculate karta hai
    """

    to_encode.update({"exp": expire})
    """
    Payload me expiration field add karta hai
    taake token limited time tak valid rahe
    """

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    """
    Payload ko SECRET_KEY aur algorithm ke sath encode karta hai
    final JWT token generate hota hai
    """

    return encoded_jwt
    """
    Generated token caller function ko return karta hai
    """






from fastapi.security import HTTPBearer

security = HTTPBearer()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Extracts and verifies JWT token
    from Authorization header manually
    """

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


#     Ye code kya karta hai

# Is step ke baad system:

# .env se secret key read karega
# token expiry set karega
# username payload add karega
# JWT token generate karega