import unittest
import pytest

from app.controllers import UserController
from databases.models import (
    User,
    Task
)
from tests import get_testing_session


class UserControllerTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)

    def tearDown(self):
        self.session.query(User).delete()
        self.session.query(Task).delete()
        self.session.commit()
        self.session.close()

    def test_given_no_users_are_created_when_user_controller_gets_any_user_by_name_then_returns_none(self):
        user = self.user_controller.get_user_by_name("threezinedine")
        assert user is None

    def test_given_a_valid_user_is_created_when_user_controller_gets_that_user_by_name_then_returns_the_user(self):
        self.user_controller.create_new_user(username="threezinedine", password="threezinedine")

        user = self.user_controller.get_user_by_name(username="threezinedine")

        assert user.userId == 1
        assert user.username == "threezinedine"
        assert user.compared_password("threezinedine")

    def test_given_a_valid_user_is_created_when_ask_the_user_existance_then_returns_true(self):
        self.user_controller.create_new_user(username="threezinedine", password="threezinedine")

        assert self.user_controller.is_existed(username="threezinedine")

    def test_given_a_user_is_created_when_checking_the_validation_of_the_incoming_valid_user_then_returns_true(self):
        self.user_controller.create_new_user(username="threezinedine", password="threezinedine")

        assert self.user_controller.is_valid(username="threezinedine", password="threezinedine")

    def test_given_a_user_is_created_when_checking_the_validation_of_the_incoming_username_is_wrong_then_returns_false(self):
        self.user_controller.create_new_user(username="threezinedine", password="threezinedine")

        assert self.user_controller.is_valid(username="threezinedine1", password="threezinedine") == False

    def test_given_a_user_is_created_when_checking_the_validation_of_the_password_username_is_wrong_then_returns_false(self):
        self.user_controller.create_new_user(username="threezinedine", password="threezinedine")

        assert self.user_controller.is_valid(username="threezinedine", password="threezinedine1") == False

    def test_given_no_user_are_created_when_user_controller_gets_by_id_then_return_none(self):
        user = self.user_controller.get_user_by_id(userId=1)
        
        assert user is None

    def test_given_a_user_is_created_when_user_controller_gets_by_id_then_return_that_user(self):
        self.user_controller.create_new_user(username="threezinedine", password="threezinedine")

        user = self.user_controller.get_user_by_id(userId=1)
        
        assert user.userId == 1
