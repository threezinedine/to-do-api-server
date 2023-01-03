from fastapi import APIRouter


router = APIRouter(prefix="/users")


from app.api.v1.users import *
