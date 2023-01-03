import unittest
from datetime import datetime

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
        self.task_controller = TaskController(self.session, self.user_controller)

        self.user_controller.create_new_user(username="threezinedine", password="threezinedine")

    def tearDown(self):
        self.session.query(User).delete()
        self.session.query(Task).delete()
        self.session.commit()
        self.session.close()

    def assertTaskContainsDict(self, task:Task, compared_dict: dict) -> bool:
        for key, value in compared_dict.items():
            assert getattr(task, key) == value

    def test_given_a_user_is_created_when_query_all_tasks_then_returns_empty_array(self):
        tasks = self.task_controller.get_all_tasks_by_username(username="threezinedine")

        self.assertListEqual(tasks, [])

    def test_given_a_user_is_created_when_a_task_is_created_then_the_get_all_tasks_query_returns_a_list_contain_that_task(self):
        task = dict(
                taskName="Implement API server",
                taskDescription="",
                taskType="project",
                plannedDate=datetime.strptime("2023-01-01", "%Y-%m-%d").date()
            )
        self.task_controller.create_new_task_by_username(username="threezinedine", **task)
        
        tasks = self.task_controller.get_all_tasks_by_username(username="threezinedine")

        assert len(tasks) == 1
        self.assertTaskContainsDict(tasks[0], dict(taskComplete=False, **task))

    def test_given_a_user_is_created_when_a_task_is_created_for_a_wrong_user_then_returns_none(self):
        task = dict(
                taskName="Implement API server",
                taskDescription="",
                taskType="project",
                plannedDate=datetime.strptime("2023-01-01", "%Y-%m-%d").date()
            )
        self.task_controller.create_new_task_by_username(username="threezinedine1", **task)

        tasks = self.task_controller.get_all_tasks_by_username(username="threezinedine")

        assert tasks is None
