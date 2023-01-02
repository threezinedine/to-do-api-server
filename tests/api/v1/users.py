import unittest
import pytest
from fastapi.testclient import TestClient

from main import app
from app.controllers import UserController
from databases.connection import get_session
from databases.models import User
from tests import get_testing_session


class UserTest(unittest.TestCase):
    def setUp(self):
        app.dependency_overrides[get_session] = get_testing_session
        self.test_client = TestClient(app) 
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)

    def tearDown(self):
        self.session.query(User).delete()
        self.session.commit()
        self.session.close()

    def test_when_user_regists_a_new_valid_account_then_this_account_is_created(self):
        response = self.test_client.post(
                "/users/register",
                json={"username": "threezinedine", "password": "threezinedine"})

        assert response.status_code == 200
    
        data = response.json()
        assert set(data.keys()) == set(["userId", "username"])
        assert data["userId"] == 1
        assert data["username"] == "threezinedine"

        user = self.user_controller.get_by_name("threezinedine")
        assert user.userId == 1

    def test_given_a_user_is_created_when_log_in_with_right_value_then_return_the_token(self):
        self.user_controller.create_new_user(username="threezinedine", password="threezinedine")

        response = self.test_client.post(
                "/users/login",
                json={"username": "threezinedine", "password": "threezinedine"}
                )

        assert response.status_code == 200 

        data = response.json()
        assert set(data.keys()) == set(["userId", "username", "description", "image", "token"])
        self.assertDictContainsSubset({
            "userId": 1,
            "username": "threezinedine",
            "description": "",
            "image": ""
            }, data)
