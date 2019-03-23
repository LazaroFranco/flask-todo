from flask_boilerplate import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_index(client):
    response = client.get('/')
    assert response.data == b"Welcome to Lazaro's App!!"

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello World!'


    response = client.get('/hello?name=Jim')
    assert response.data == b'Hello Jim!'

def test_number(client):
    response = client.get('/number/1')
    assert response.data == b'Number: 1'

    response = client.get('/number/2')
    assert response.data == b'Number: 2'


def test_method_route(client):
    response = client.get('/method')
    assert response.data == b'HTTP Method: GET'

    response = client.post('/method')
    assert response.data == b'HTTP Method: POST'

    response = client.patch('/method')
    assert response.data == b'HTTP Method: PATCH'

    response = client.put('/method')
    assert response.data == b'HTTP Method: PUT'

    response = client.delete('/method')
    assert response.data == b'HTTP Method: DELETE'


def test_status_route(client):
    response = client.get('/status?c=400')
    assert response.status == '400 CLIENT ERROR'

    response = client.get('/status?c=500')
    assert response.status == '500 SERVER ERROR'

    response = client.get('/status')
    assert response.status == '200 OKAY'
