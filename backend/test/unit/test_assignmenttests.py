import pytest
import unittest.mock as mock
from unittest.mock import patch, MagicMock
from src.util.helpers import ValidationHelper
from src.controllers.usercontroller import UserController




# Test cases

# Tests for get_user_by_email, ValueError separated due to more info shown if put in 
# pytest.raises.



# I am splitting up the test cases in order for each case to only have one assertion.
@pytest.mark.parametrize('email', 
                         [("ojsan")])
def test_get_user_by_email_exceptions_badmail(email):
              mock_dao = MagicMock()
              user_controller_instance = UserController(mock_dao)
              with pytest.raises(ValueError):
                     user_controller_instance.get_user_by_email(email)

def test_get_user_by_email_exceptions_mail(email="examplename.lastname@example.com"):
              mock_dao = MagicMock()
              user_controller_instance = UserController(mock_dao)
              assert user_controller_instance.get_user_by_email(email)
    

