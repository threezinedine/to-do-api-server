import unittest
import pytest
from fastapi.testclient import TestClient

from main import app
from databases.connection import get_session
from databases.models import User
from tests import get_testing_session
from app.controllers import UserController
from app.constants import (
    HTTP_200_OK,
)
from app.exceptions import (
    HTTP_409_CONFLICT,
    USER_EXISTED_MESSAGE,
)


class UserTest(unittest.TestCase):
    testing_user = {UserController.USERNAME_KEY: "threezinedine", UserController.PASSWORD_KEY: "threezinedine"}
    wrong_testing_user = {UserController.USERNAME_KEY: "threezinedine1", UserController.PASSWORD_KEY: "threezinedine"}
    loggin_response_dict = {
            UserController.USER_ID_KEY: 1,
            UserController.USERNAME_KEY: "threezinedine",
            UserController.DESCRIPTION_KEY: "",
            UserController.IMAGE_KEY: ""
        }
    register_response_keys = set([UserController.USER_ID_KEY, UserController.USERNAME_KEY])
    login_response_keys = set([UserController.USER_KEY, UserController.TOKEN_KEY])

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
                json=self.testing_user)

        assert response.status_code == HTTP_200_OK
    
        data = response.json()
        assert set(data.keys()) == self.register_response_keys
        assert data[UserController.USERNAME_KEY] == self.testing_user[UserController.USERNAME_KEY]

        user = self.user_controller.get_user_by_name(self.testing_user[UserController.USERNAME_KEY])
        assert user.userId == data[UserController.USER_ID_KEY]

    def test_given_a_user_is_created_when_register_a_new_account_with_existed_username_then_returns_HTTP_409_CONFLICT(self):
        self.user_controller.create_new_user(**self.testing_user)

        response = self.test_client.post(
                "/users/register",
                json=self.testing_user
                )

        assert response.status_code == HTTP_409_CONFLICT
        assert response.json()["detail"] == USER_EXISTED_MESSAGE

    def test_given_a_user_is_created_when_log_in_with_right_value_then_return_the_token(self):
        self.user_controller.create_new_user(**self.testing_user)

        response = self.test_client.post(
                "/users/login",
                json=self.testing_user
                )

        assert response.status_code == HTTP_200_OK 

        data = response.json()
        assert set(data.keys()) == self.login_response_keys
        self.assertDictEqual(self.loggin_response_dict, data[UserController.USER_KEY])

    def test_given_a_user_is_created_when_login_with_wrong_username_then_returns_no_user_existed(self):
        self.user_controller.create_new_user(**self.testing_user)

        response = self.test_client.post(
                "/users/login",
                json=self.wrong_testing_user
                )

        assert response.status_code == 401 

        detail = response.json()["detail"]
        assert detail == "The username or password is not correct."
