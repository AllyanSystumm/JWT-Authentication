from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# What this file does (simple explanation)

# This file validates incoming API data:

# Example signup request must look like:

# {
#   "username": "tabish",
#   "email": "tabish@gmail.com",
#   "password": "12345"
# }    