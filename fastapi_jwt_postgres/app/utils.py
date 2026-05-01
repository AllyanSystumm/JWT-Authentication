from passlib.context import CryptContext
# CryptContext ek password hashing manager hota hai
# jo hashing algorithm configure karta hai (yahan bcrypt use ho raha hai)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
"""
pwd_context ek configuration object hai jo password hashing handle karta hai.

schemes=["bcrypt"]
→ batata hai kaunsa hashing algorithm use hoga (bcrypt secure hota hai)

deprecated="auto"
→ agar future me algorithm change ho jaye to automatically update handle karega
"""


def hash_password(password: str):
    """
    Ye function plain password ko secure hashed password me convert karta hai.

    Parameters:
    password (str): user ka original password (plain text form me)

    Returns:
    str: hashed password jo database me store hota hai
    """
    return pwd_context.hash(password)
    # pwd_context.hash() bcrypt algorithm se password encrypt karta hai
    # example:
    # input:  "admin123"
    # output: "$2b$12$kjhdfkjsdhfkjshdfkjsdhf..."


def verify_password(plain_password, hashed_password):
    """
    Ye function check karta hai ke login ke waqt user ka entered password
    database me stored hashed password se match karta hai ya nahi.

    Parameters:
    plain_password (str): login ke waqt user ka entered password
    hashed_password (str): database me stored encrypted password

    Returns:
    bool:
        True  → agar password match kare
        False → agar password match na kare
    """
    return pwd_context.verify(
        plain_password,
        hashed_password
    )
    # verify() internally plain password ko hash karta hai
    # aur database wale hashed password se compare karta hai