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

def test_get_user_by_email_database_fail(email = "examplename.lastname@example.com"):
       with patch('src.util.helpers.DAO', autospec=True):
              with patch('re.fullmatch', autospec=True) as mockfullmatch:
                     mockfullmatch.return_value = True
                     mockedDAO = MagicMock()
                     mockedDAO.find.side_effect = Exception()
                     ucinstance = UserController(dao=mockedDAO)
                     with pytest.raises(Exception):
                            ucinstance.get_user_by_email(email)

@pytest.mark.parametrize('email, outcome', 
                         [("examplename.lastname@example.com", None), ("jane.doe@gmail.com", {'Email: jane.doe@gmail.com'})])
def test_get_user_by_email_nomatch(email, outcome):

       with patch('src.util.helpers.DAO', autospec=True):
              mockedDAO = MagicMock()
              mockedDAO.find.return_value = outcome
              uc = UserController(dao=mockedDAO)
              with pytest.raises(Exception):
                     assert uc.get_user_by_email(email) == outcome

    


