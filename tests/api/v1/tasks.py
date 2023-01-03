import unittest
import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from main import app
from databases.connection import get_session
from databases.models import (
    Task,
    User,
)
from tests import get_testing_session
from app.controllers import (
    TaskController,
    UserController,
)


class TaskTest(unittest.TestCase):
    test_user = {
                "username": "threezinedine",
                "password": "threezinedine",
            }
    test_task = {
                "taskName": "Implement the API server",
                "taskDescription": "",
                "taskType": "project",
                "plannedDate": "2023-03-01"
            }

    def setUp(self):
        app.dependency_overrides[get_session] = get_testing_session
        self.test_client = TestClient(app) 
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)
        self.task_controller = TaskController(self.session, self.user_controller)

        self.user_controller.create_new_user(**self.test_user)

        login_response = self.test_client.post(
                "users/login",
                json=self.test_user
            )

        token = login_response.json()["token"]
        self.header = {
                'Authorization': f'Bearer {token}'
            } 

    def tearDown(self):
        self.session.query(User).delete()
        self.session.query(Task).delete()
        self.session.commit()
        self.session.close()

    def assertTaskContains(self, task, compared_task):
        for key, value in compared_task.items():
            assert task[key] == value

    def test_given_a_user_is_created_when_login_with_right_value_and_request_the_task_then_returns_empty_string(self):
        response = self.test_client.get(
                "/tasks",
                headers=self.header
            )

        assert response.status_code == 200
        self.assertListEqual(response.json(), [])

    def test_given_a_user_is_created_and_a_task_are_created_when_login_with_right_value_and_request_the_task_then_returns_the_array_contains_that_string(self):
        self.task_controller.create_new_task_by_username(username=self.test_user["username"], **self.test_task)
        response = self.test_client.get(
                "/tasks",
                headers=self.header
            )

        assert response.status_code == 200

        first_task = response.json()[0]
        self.assertTaskContains(first_task, dict(taskId=1, taskComplete=False, **self.test_task))
        
