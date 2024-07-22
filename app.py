from aiohttp import web
from peewee import IntegrityError

from models import Device, db, APIUser, Location
from utils import serialize_device


async def get_all_devices(request):
    devices = [serialize_device(device) for device in Device.select()]
    return web.json_response(devices)


async def create_api_user(request):
    data = await request.json()
    try:
        user = APIUser.create(
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        return web.json_response({
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }, status=201)
    except IntegrityError:
        return web.json_response({'error': 'Email already exists'}, status=400)


async def create_location(request):
    data = await request.json()
    try:
        location = Location.create(name=data['name'])
        return web.json_response({
            'id': location.id,
            'name': location.name
        }, status=201)
    except IntegrityError:
        return web.json_response({'error': 'Location name already exists'}, status=400)


async def get_device(request):
    device_id = int(request.match_info['id'])
    try:
        device = Device.get(Device.id == device_id)
        return web.json_response(serialize_device(device))
    except Device.DoesNotExist:
        return web.json_response({'error': 'Device not found'}, status=404)


async def create_device(request):
    data = await request.json()
    try:
        device = Device.create(
            name=data['name'],
            type=data['type'],
            login=data['login'],
            password=data['password'],
            location=data['location_id'],
            api_user=data['api_user_id']
        )
        return web.json_response(serialize_device(device), status=201)
    except IntegrityError:
        return web.json_response({'error': 'Invalid input or foreign key'}, status=400)


async def update_device(request):
    device_id = int(request.match_info['id'])
    data = await request.json()

    try:
        device = Device.get(Device.id == device_id)
        device.name = data.get('name', device.name)
        device.type = data.get('type', device.type)
        device.password = data.get('password', device.password)
        device.location = data.get('location_id', device.location.id)
        device.api_user = data.get('api_user_id', device.api_user.id)
        device.save()

        return web.json_response(serialize_device(device))
    except Device.DoesNotExist:
        return web.json_response({'error': 'Device not found'}, status=404)


async def delete_device(request):
    device_id = int(request.match_info['id'])

    try:
        device = Device.get(Device.id == device_id)
        device.delete_instance()
        return web.json_response({'message': 'Device deleted successfully'})
    except Device.DoesNotExist:
        return web.json_response({'error': 'Device not found'}, status=404)


async def init_app():
    app = web.Application()
    app.router.add_get('/devices', get_all_devices)
    app.router.add_get('/devices/{id}', get_device)
    app.router.add_post('/devices', create_device)
    app.router.add_put('/devices/{id}', update_device)
    app.router.add_delete('/devices/{id}', delete_device)
    app.router.add_post('/api_users', create_api_user)
    app.router.add_post('/locations', create_location)

    db.connect()

    return app


if __name__ == '__main__':
    app = init_app()
    web.run_app(app, host='localhost', port=8080)
