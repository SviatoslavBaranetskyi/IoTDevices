import json
import pytest
from unittest.mock import patch, AsyncMock

from app import init_app


@pytest.fixture
async def client(aiohttp_client):
    app = await init_app()
    return await aiohttp_client(app)


@pytest.fixture
def mock_objects():
    mock_location = AsyncMock()
    mock_location.id = 1
    mock_location.name = 'Living Room'

    mock_api_user = AsyncMock()
    mock_api_user.id = 1
    mock_api_user.name = 'John Doe'
    mock_api_user.email = "john.doe@example.com"
    mock_api_user.password = "securepassword"

    mock_device = AsyncMock()
    mock_device.id = 1
    mock_device.name = 'Thermostat'
    mock_device.type = 'Temperature Sensor'
    mock_device.login = 'admin'
    mock_device.location = mock_location
    mock_device.api_user = mock_api_user

    return mock_location, mock_api_user, mock_device


@pytest.mark.asyncio
async def test_create_api_user(client, mock_objects):
    mock_location, mock_api_user, mock_device = mock_objects

    with patch('app.APIUser.create', return_value=mock_api_user):
        data = {'name': 'John Doe', 'email': 'john.doe@example.com', 'password': 'securepassword'}
        response = await client.post('/api_users', json=data)
        assert response.status == 201
        response_data = await response.json()
        assert response_data['id'] == 1
        assert response_data['name'] == 'John Doe'
        assert response_data['email'] == 'john.doe@example.com'


@pytest.mark.asyncio
async def test_create_location(client, mock_objects):
    mock_location, mock_api_user, mock_device = mock_objects

    with patch('app.Location.create', return_value=mock_location):
        data = {'name': 'Living Room'}
        response = await client.post('/locations', json=data)
        assert response.status == 201
        assert json.loads(await response.text()) == {
            'id': 1,
            'name': 'Living Room'
        }


@pytest.mark.asyncio
async def test_get_device(client, mock_objects):
    mock_location, mock_api_user, mock_device = mock_objects

    with patch('app.Device.get', return_value=mock_device):
        response = await client.get('/devices/1')
        assert response.status == 200
        response_data = await response.json()
        assert response_data['id'] == 1
        assert response_data['name'] == 'Thermostat'
        assert response_data['type'] == 'Temperature Sensor'
        assert response_data['location'] == mock_location.name
        assert response_data['api_user'] == mock_api_user.name


@pytest.mark.asyncio
async def test_create_device(client, mock_objects):
    mock_location, mock_api_user, mock_device = mock_objects

    with patch('app.Device.create', return_value=mock_device):
        data = {
            'name': 'Thermostat',
            'type': 'Temperature Sensor',
            'login': 'admin',
            'password': 'password',
            'location_id': 1,
            'api_user_id': 1
        }
        response = await client.post('/devices', json=data)
        assert response.status == 201
        response_data = await response.json()
        assert response_data['id'] == 1
        assert response_data['name'] == 'Thermostat'
        assert response_data['type'] == 'Temperature Sensor'


@pytest.mark.asyncio
async def test_update_device(client, mock_objects):
    mock_location, mock_api_user, mock_device = mock_objects

    with patch('app.Device.get', return_value=mock_device), patch('app.Device.save', new_callable=AsyncMock):
        data = {
            'name': 'iPhone',
            'type': '15 Pro Max',
            'password': 'newpassword',
            'location_id': 1,
            'api_user_id': 1
        }
        response = await client.put('/devices/1', json=data)

        assert response.status == 200
        response_data = await response.json()
        assert response_data['id'] == 1
        assert response_data['name'] == 'iPhone'
        assert response_data['type'] == '15 Pro Max'
        assert response_data['login'] == 'admin'
        assert response_data['location'] == 'Lviv'
        assert response_data['api_user'] == 'John Doe'


@pytest.mark.asyncio
async def test_delete_device(client, mock_objects):
    mock_location, mock_api_user, mock_device = mock_objects

    with patch('app.Device.get', return_value=mock_device), patch('app.Device.delete_instance', new_callable=AsyncMock):
        response = await client.delete('/devices/1')
        assert response.status == 200
