import unittest
import pytest
from fastapi.testclient import TestClient

from main import app
from databases.connection import get_session
from tests import get_testing_session


class TaskTest(unittest.TestCase):
    def setUp(self):
        app.dependency_overrides[get_session] = get_testing_session
        self.test_client = TestClient(app) 
        self.session = next(get_testing_session())
        self.task_controller = TaskController(self.session)

    def tearDown(self):
        self.session.query(Task).delete()
        self.session.commit()
        self.session.close()

    def test_given_a_user_is_created_when_login_with_right_value_and_request_the_task_then_returns_empty_string(self):
        self.test_client.post(
                "users/register",
                json={
                    "username": "threezinedine",
                    "password": "threezinedine",
                }
            )

        login_response = self.test_client.post(
                "users/login",
                json={
                    "username": "threezinedine",
                    "password": "threezinedine",
                }
            )

        token = login_response.json()["token"]

        response = self.test_client.get(
                "/tasks",
                headers={
                    'Authorization': f'Bearer {token}'
                }
            )

        assert response.status_code == 200
