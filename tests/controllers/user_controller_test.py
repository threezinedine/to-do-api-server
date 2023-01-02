import unittest
import pytest

from app.controllers import UserController
from databases.models import User
from tests import get_testing_session


class UserControllerTest(unittest.TestCase):
    def setUp(self):
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