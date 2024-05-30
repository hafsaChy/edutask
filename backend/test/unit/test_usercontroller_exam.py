import pytest
from unittest.mock import patch, MagicMock
from src.controllers.usercontroller import UserController

@pytest.fixture
def sut(user_array: list):
    mock_dao = MagicMock()
    mock_dao.find.return_value = user_array
    sut_obj = UserController(dao = mock_dao)
    return sut_obj

# Test case for a valid email
@pytest.mark.parametrize('user_array, email, exp_user',
    [
        (
            [{'firstName': 'Jane', 'lastName': 'Doe'}],
            'jane.doe@email.com',
            {'firstName': 'Jane','lastName': 'Doe'}
        ),
        (
            [
                {'firstName': 'Some','lastName': 'Doe'},
                {'firstName': 'Jane','lastName': 'Doe'}
            ],
            'jane.doe@email.com',
            {'firstName': 'Some', 'lastName': 'Doe'}
        )
    ])
def test_valid_email_users_found(sut, email, exp_user):
    """
    Tests get_user_by_email method for
    valid email. It should
    1. return the user for one user
    2. return the first user for multiple user
    """
    assert sut.get_user_by_email(email) == exp_user


# Test case for a valid email with multiple users prints warning message
@pytest.mark.parametrize('user_array, email, exp_user', [(
    [
        {'firstName': 'Some','lastName': 'Doe'},
        {'firstName': 'Jane','lastName': 'Doe'}
    ],
    'jane.doe@email.com',
    {'firstName': 'Some','lastName': 'Doe'}
    )])
def test_valid_email_multiple_users_found(sut, email):
    """
    Tests get_user_by_email method for
    valid email with multiple users. It should
    print a warning message containing that email. It is a white box test. 
    """
    with patch('builtins.print') as mock_print:
        sut.get_user_by_email(email=email)
        mock_print.assert_called()
        mock_print.assert_any_call(f'Error: more than one user found with mail {email}')


# Test case for an invalid email
@pytest.mark.parametrize('user_array, email', 
                         [([{
        'firstName': 'Jane',
        'lastName': 'Doe'
    }], "@email.com"), ([{
        'firstName': 'Jane',
        'lastName': 'Doe'
    }], "janeemail.com"),([{
        'firstName': 'Jane',
        'lastName': 'Doe'
    }], "jane.doe@.com"),([{
        'firstName': 'Jane',
        'lastName': 'Doe'
    }], "jane.doe@email"),([{
        'firstName': 'Jane',
        'lastName': 'Doe'
    }], "jane.doe@emailcom"),([{
        'firstName': 'Jane',
        'lastName': 'Doe'
    }], "jane@doe@email.com"),([{
        'firstName': 'Jane',
        'lastName': 'Doe'
    }], "")])
def test_invalid_email(sut, email):
    """
    Tests get_user_by_email method for
    invalid email. It should raise Value Error.
    The following errors are tested for:
    1. missing local part
    2. missing @
    3. missing domain
    4. missing TLD part
    5. missing dot separator (.) between domain and TLD part
    6. more than one @
    7. empty string
    """
    with pytest.raises(ValueError):
        sut.get_user_by_email(email)

# Test case for a valid email with no user found
@pytest.mark.parametrize('user_array, email', [([],
    "examplename.lastname@example.com"
)])
def test_valid_email_with_no_user(sut, email):
    """
    Tests get_user_by_email method for valid email but
    no user found. It should return None.
    """
    user = sut.get_user_by_email(email)
    assert user is None



# Test case for database fail
@pytest.mark.parametrize('user_array', [Exception])
def test_database_fail(sut):
    """
    Tests get_user_by_email method for
    database fail. It should
    raise Exception. 
    """
    email = 'jane@email.com'
    with pytest.raises(Exception):
        sut.get_user_by_email(email)    

