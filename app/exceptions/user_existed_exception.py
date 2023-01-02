from fastapi import HTTPException

HTTP_409_CONFLICT = 409
USER_EXISTED_MESSAGE = "The user existed."

UserExistedException = HTTPException(status_code=HTTP_409_CONFLICT, detail=USER_EXISTED_MESSAGE)
