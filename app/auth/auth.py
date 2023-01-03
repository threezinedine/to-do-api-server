import jwt
import datetime
import os 
from fastapi import (
    HTTPException,
    Depends,
)
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


secret_key = os.getenv("SECRET_KEY", "secret_key")
algorithm = os.getenv("ALGORITHM", "HS256")
encrypted_obj = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user_from_token(token: str = Depends(security)):
    claims = None

    try:
        claims = jwt.decode(token, secret_key, algorithm)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="The token is expired.")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    return claims


def create_token(data: dict, expired_delta: datetime.timedelta) -> str:
    """
    Create a new JWT token for a user 

    Paratemers
    ----------
        data: dict 
            The data that is attached with the token.

        expired_delta: datetime.timedelta
            The available range of time that user can use this token 

    Returns
    -------
        token: string 
            The generated token
    """
    return jwt.encode(data, secret_key, algorithm=algorithm) 

def get_hased_password(password: str) -> str:
    """
    The function that is used for encrypting the password.

    Paratemers
    ----------
        password: str 
            The input password that will be encrypted.

    Returns
    -------
        hased_password: str 
            The hased password, which is stored inside the database

    """
    return encrypted_obj.hash(password)

def verify_the_password(hased_password: str, compared_password: str) -> bool:
    """
    The function that is used for verifying the password.

    Paratemers
    ----------
        hased_password: str 
            The hased password that is obtained from the databse.
        
        compared_password: str 
            The password that must be verified.

    Returns
    -------
        is_machted: bool
            True of 2 password is matched, vice versa.
    """
    return encrypted_obj.verify(compared_password, hased_password)
