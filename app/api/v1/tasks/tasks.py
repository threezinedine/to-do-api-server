from app.api.v1.tasks import router


@router.get("/")
def get_all_tasks():
    return []
