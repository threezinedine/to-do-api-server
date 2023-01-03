import unittest

from app.controllers import (
    TaskController,
    UserController,
)
from tests import get_testing_session
from databases.models import (
    User,
    Task,
)


class TaskControllerTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)
        self.task_controller = TaskController(self.session)

        self.user_controller.create_new_user(username="threezinedine", password="threezinedine")

    def tearDown(self):
        self.session.query(Task).delete()
        self.session.query(User).delete()

    def test_given_a_user_is_created_when_query_all_tasks_then_returns_empty_array(self):
        self.task_controller.get_all_tasks_by_username(username="threezinedine")
