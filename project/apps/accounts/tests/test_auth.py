import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from faker import Faker
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_403_FORBIDDEN

from helpers.constants import KEY_USERNAME, KEY_PASSWORD, KEY_FIRST_NAME, KEY_LAST_NAME, KEY_USER, KEY_EMAIL
from main.settings import AUTHORIZATION_HEADER

client = Client()
faker = Faker()


def _register(data):
    url = reverse('accounts:user-list')
    response = client.post(url, data)
    return response.json(), response.status_code


def _login(data):
    url = reverse('accounts:user-login')
    response = client.post(url, data)
    return response.json(), response.status_code


def _update(data, user_id, token):
    url = reverse('accounts:user-detail', kwargs={'pk': user_id})
    headers = {
        AUTHORIZATION_HEADER: token,
        'content_type': 'application/json'
    }
    response = client.put(path=url, data=data, **headers)
    return response.json(), response.status_code


@pytest.mark.django_db
def test_register_user_should_success():
    initial_data = {
        KEY_USERNAME: faker.word(),
        KEY_PASSWORD: faker.word(),
    }
    data, status_code = _register(initial_data)
    assert status_code == HTTP_201_CREATED
    assert User.objects.count() == 1
    assert data[KEY_USERNAME] == initial_data[KEY_USERNAME]


@pytest.mark.django_db
def test_register_user_empty_username():
    initial_data = {
        KEY_USERNAME: '',
        KEY_PASSWORD: faker.word(),
    }
    data, status_code = _register(initial_data)
    assert status_code == HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_user_without_username():
    initial_data = {
        KEY_PASSWORD: faker.word(),
    }
    data, status_code = _register(initial_data)
    assert status_code == HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_user_empty_password():
    initial_data = {
        KEY_USERNAME: faker.word(),
        KEY_PASSWORD: '',
    }
    data, status_code = _register(initial_data)
    assert status_code == HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_user_without_password():
    initial_data = {
        KEY_USERNAME: faker.word(),
    }
    data, status_code = _register(initial_data)
    assert status_code == HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_user_without_username_password():
    initial_data = {}
    data, status_code = _register(initial_data)
    assert status_code == HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_user_empty_password_username():
    initial_data = {
        KEY_USERNAME: '',
        KEY_PASSWORD: '',
    }
    data, status_code = _register(initial_data)
    assert status_code == HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_login_success():
    initial_data = {
        KEY_USERNAME: faker.word(),
        KEY_PASSWORD: faker.word(),
    }
    data, status_code = _register(initial_data)
    assert status_code == HTTP_201_CREATED
    assert User.objects.count() == 1
    assert data[KEY_USERNAME] == initial_data[KEY_USERNAME]
    data, status_code = _login(initial_data)
    assert status_code == HTTP_200_OK
    assert data[KEY_USER][KEY_USERNAME] == initial_data[KEY_USERNAME]


@pytest.mark.django_db
def test_login_wit_empty_username_fail():
    initial_data = {
        KEY_USERNAME: faker.word(),
        KEY_PASSWORD: faker.word(),
    }
    data, status_code = _register(initial_data)
    assert status_code == HTTP_201_CREATED
    assert User.objects.count() == 1
    assert data[KEY_USERNAME] == initial_data[KEY_USERNAME]
    login_data = {
        KEY_USERNAME: '',
        KEY_PASSWORD: initial_data[KEY_PASSWORD]
    }
    data, status_code = _login(login_data)
    assert status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_without_username_fail():
    initial_data = {
        KEY_USERNAME: faker.word(),
        KEY_PASSWORD: faker.word(),
    }
    data, status_code = _register(initial_data)
    assert status_code == HTTP_201_CREATED
    assert User.objects.count() == 1
    assert data[KEY_USERNAME] == initial_data[KEY_USERNAME]

    login_data = {
        KEY_PASSWORD: initial_data[KEY_PASSWORD]
    }
    data, status_code = _login(login_data)
    assert status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_wit_empty_invalid_password_fail():
    initial_data = {
        KEY_USERNAME: faker.word(),
        KEY_PASSWORD: faker.word(),
    }
    data, status_code = _register(initial_data)
    assert status_code == HTTP_201_CREATED
    assert data[KEY_USERNAME] == initial_data[KEY_USERNAME]

    login_data = {
        KEY_USERNAME: initial_data[KEY_USERNAME],
        KEY_PASSWORD: initial_data[KEY_PASSWORD]*2
    }
    data, status_code = _login(login_data)
    assert status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_success():
    initial_data = {
        KEY_USERNAME: faker.word(),
        KEY_PASSWORD: faker.word(),
    }
    _register(initial_data)
    data, status_code = _login(initial_data)
    new_data = {
        KEY_FIRST_NAME: faker.first_name(),
        KEY_LAST_NAME: faker.last_name(),
        KEY_EMAIL: faker.email(),
    }
    data, status_code = _update(data=new_data, user_id=data[KEY_USER]['id'], token=data['token'])
    assert status_code == HTTP_200_OK
    assert initial_data[KEY_USERNAME] == data[KEY_USERNAME]
    assert new_data[KEY_FIRST_NAME] == data[KEY_FIRST_NAME]
    assert new_data[KEY_LAST_NAME] == data[KEY_LAST_NAME]
    assert new_data[KEY_EMAIL] == data[KEY_EMAIL]


@pytest.mark.django_db
def test_update_fail():
    initial_data = {
        KEY_USERNAME: faker.word(),
        KEY_PASSWORD: faker.word(),
    }
    _register(initial_data)
    data, status_code = _login(initial_data)
    new_data = {
        KEY_FIRST_NAME: faker.first_name(),
        KEY_LAST_NAME: faker.last_name(),
        KEY_EMAIL: faker.email(),
    }
    data, status_code = _update(data=new_data, user_id=data[KEY_USER]['id'], token='')
    assert status_code == HTTP_403_FORBIDDEN

