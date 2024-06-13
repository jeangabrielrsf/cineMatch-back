from http import HTTPStatus

from fastapi.testclient import TestClient

from cinematch_back.app import app


def test_root_health_check():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Server running OK!'}
