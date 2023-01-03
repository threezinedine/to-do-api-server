from sqlalchemy.orm import Session


class TaskController:
    def __init__(self, session: Session):
        self.session = Session
