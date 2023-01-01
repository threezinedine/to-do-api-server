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

    def test_given_no_users_are_created_when_user_controller_gets_any_user_by_name_then_returns_none(self):
        user = self.user_controller.get_by_name("threezinedine")
        assert user is None

    def test_given_a_valid_user_is_created_when_user_controller_gets_that_user_by_name_then_returns_the_user(self):
        self.user_controller.create_new_user(username="threezinedine", password="threezinedine")

        user = self.user_controller.get_by_name(username="threezinedine")

        assert user.userId == 1
        assert user.username == "threezinedine"
        assert user.compared_password("threezinedine")

    def test_when_user_regists_a_new_valid_account_then_this_account_is_created(self):
        response = self.test_client.post(
                "/users/register",
                json={"username": "threezinedine", "password": "threezinedine"})

        print(response)
        assert response.status_code == 200
    
        data = response.json()
        assert set(data.keys()) == set(["userId", "username"])
        assert data["userId"] == 1
        assert data["username"] == "threezinedine"

        user = self.user_controller.get_by_name("threezinedine")
        assert user.userId == 1
