import unittest
import pytest
from fastapi.testclient import TestClient

from main import app
from databases.connection import get_session
from databases.models import (
    Task,
    User,
)
from tests import get_testing_session
from app.controllers import TaskController


class TaskTest(unittest.TestCase):
    test_user = {
                "username": "threezinedine",
                "password": "threezinedine",
            }

    def setUp(self):
        app.dependency_overrides[get_session] = get_testing_session
        self.test_client = TestClient(app) 
        self.session = next(get_testing_session())
        self.task_controller = TaskController(self.session)

        self.test_client.post(
                "users/register",
                json=self.test_user
            )

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

    def test_given_a_user_is_created_when_login_with_right_value_and_request_the_task_then_returns_empty_string(self):

        response = self.test_client.get(
                "/tasks",
                headers=self.header
            )

        assert response.status_code == 200
        self.assertListEqual(response.json(), [])
