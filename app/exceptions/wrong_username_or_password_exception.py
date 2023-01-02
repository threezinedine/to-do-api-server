from fastapi import (
    HTTPException,
)


HTTP_401_UNAUTHORIZED = 401
WRONG_USERNAME_OR_PASSWORD_MESSAGE = "The username or password is not correct."


WrongUsernameOrPasswordException = HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=WRONG_USERNAME_OR_PASSWORD_MESSAGE)
