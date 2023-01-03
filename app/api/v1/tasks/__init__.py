from fastapi import APIRouter


router = APIRouter(prefix="/tasks")


from .tasks import *
