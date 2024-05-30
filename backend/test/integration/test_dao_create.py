import pytest
import unittest.mock as mock
from unittest.mock import patch
import pymongo
import json
from src.util.dao import DAO

@pytest.fixture()
def test_db():
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client.create_testdb

    yield db
    client.drop_database('create_testdb')
    client.close()


@pytest.fixture
def sut(test_db):
    with patch('src.util.dao.pymongo.MongoClient', autospec=True) as mock_pymongo, \
        patch('src.util.dao.getValidator', autospec=True) as mock_getValidator:

        with open('./src/static/validators/create_test.json', 'r') as f:
            mock_getValidator.return_value = json.load(f)

        mock_client = mock.MagicMock()
        type(mock_client).edutask = mock.PropertyMock(return_value=test_db)
        mock_pymongo.return_value = mock_client

        sut = DAO(collection_name='create_test')
        yield sut

        test_db.drop_collection('create_test')


# includes the required property
valid_obj_1 = {
    "email": "name@email.com",
}

# includes required and optional properties
valid_obj_2 = {
    "email": "name@email.com",
    "name": "Firstname Lastname",
    "task": "Some task"
}

# includes one property but missing required property
invalid_obj_1 = {
    "name": "Firstname Lastname"
}

# includes properties and one external property
invalid_obj_2 = {
    "email": "name@email.com",
    "name": "Firstname Lastname",
    "task": "Some task",
    "address": "Stockholm"
}

# includes wrong type's property
invalid_obj_3 = {
    "email": "name@email.com",
    "task": False
}

@pytest.mark.integration
@pytest.mark.parametrize('new_obj', [
    (valid_obj_1),
    (valid_obj_2),
    ])
def test_create_valid_returns_same_object(sut, new_obj):
    """
    Tests valid scenarios when the
    new object is registered to the database.
    Should return newly created object.
    """
    res = sut.create(new_obj)
    res.pop('_id')
    assert res == new_obj

@pytest.mark.integration
@pytest.mark.parametrize('new_obj', [
    (invalid_obj_1),
    (invalid_obj_2),
    (invalid_obj_3)
    ])
def test_create_invalid_obj_raise_error(sut, new_obj):
    """
    Tests create object with invalid object,
    WriteError should be raised.
    """
    with pytest.raises(pymongo.errors.WriteError):
        sut.create(new_obj)


@pytest.mark.integration
@pytest.mark.parametrize('new_obj', [
    (invalid_obj_1),
    (invalid_obj_2),
    (invalid_obj_3)
    ])
def test_create_invalid_not_create(sut, new_obj):
    """
    Tests create object with invalid object,
    Object should not be created.
    """
    try:
        sut.create(new_obj)
    except:
        pass

    count_users = sut.collection.count_documents(new_obj)
    assert count_users == 0


@pytest.mark.integration
def test_create_dup_raise_error(sut):
    """
    Tests create object with duplicate unique property,
    WriteError should be raised.
    """
    sut.create(valid_obj_1)

    with pytest.raises(pymongo.errors.WriteError):
        sut.create(valid_obj_1)


@pytest.mark.integration
def test_create_create_not_dup(sut):
    """
    Tests create object with duplicate unique property,
    duplicate object should not be created.
    """
    sut.create(valid_obj_1)

    try:
        sut.create(valid_obj_1)
    except:
        pass

    count_users = sut.collection.count_documents(valid_obj_1)
    assert count_users == 1
