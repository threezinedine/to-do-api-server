import unittest

from tests.api.v1.tasks import TaskTest


if __name__ == "__main__":
    test_class = unittest.TestLoader().loadTestsFromTestCase(UserControllerTest)

    unittest.TextTestRunner().run(test_class)
