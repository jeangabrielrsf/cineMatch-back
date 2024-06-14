from http import HTTPStatus

from cinematch_back.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Jean',
            'email': 'jean@teste.com',
            'password': '1234',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Jean',
        'email': 'jean@teste.com',
        'id': 1,
    }


def test_create_user_username_error(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'novoemail@teste.com',
            'password': '1234567',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_error(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'novu user',
            'email': user.email,
            'password': '1234567',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_list_users_empty(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_list_users(client, user):
    users_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [users_schema]}
