from aiohttp import web
from peewee import IntegrityError
from loguru import logger

from models import Device, db, APIUser, Location
from utils import serialize_device


logger.add("file.log", rotation="1 MB")


async def get_all_devices(request):
    logger.info("Fetching all devices")
    devices = [serialize_device(device) for device in Device.select()]
    return web.json_response(devices)


async def create_api_user(request):
    data = await request.json()
    logger.info(f"Creating API user with data: {data}")
    try:
        user = APIUser.create(
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        logger.info(f"API user created: {user.id}")
        return web.json_response({
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }, status=201)
    except IntegrityError as e:
        logger.error(f"Error creating API user: {e}")
        return web.json_response({'error': 'Email already exists'}, status=400)


async def create_location(request):
    data = await request.json()
    logger.info(f"Creating location with data: {data}")
    try:
        location = Location.create(name=data['name'])
        logger.info(f"Location created: {location.id}")
        return web.json_response({
            'id': location.id,
            'name': location.name
        }, status=201)
    except IntegrityError as e:
        logger.error(f"Error creating location: {e}")
        return web.json_response({'error': 'Location name already exists'}, status=400)


async def get_device(request):
    device_id = int(request.match_info['id'])
    logger.info(f"Fetching device with ID: {device_id}")
    try:
        device = Device.get(Device.id == device_id)
        return web.json_response(serialize_device(device))
    except Device.DoesNotExist:
        logger.warning(f"Device not found: {device_id}")
        return web.json_response({'error': 'Device not found'}, status=404)


async def create_device(request):
    data = await request.json()
    logger.info(f"Creating device with data: {data}")
    try:
        device = Device.create(
            name=data['name'],
            type=data['type'],
            login=data['login'],
            password=data['password'],
            location=data['location_id'],
            api_user=data['api_user_id']
        )
        logger.info(f"Device created: {device.id}")
        return web.json_response(serialize_device(device), status=201)
    except IntegrityError as e:
        logger.error(f"Error creating device: {e}")
        return web.json_response({'error': 'Invalid input or foreign key'}, status=400)


async def update_device(request):
    device_id = int(request.match_info['id'])
    data = await request.json()
    logger.info(f"Updating device with ID: {device_id} with data: {data}")

    try:
        device = Device.get(Device.id == device_id)

        device.name = data.get('name', device.name)
        device.type = data.get('type', device.type)
        device.password = data.get('password', device.password)

        location_id = data.get('location_id')
        if location_id:
            try:
                location = Location.get(Location.id == location_id)
                device.location = location
            except Location.DoesNotExist:
                logger.warning(f"Location not found: {location_id}")
                return web.json_response({'error': 'Location not found'}, status=404)

        api_user_id = data.get('api_user_id')
        if api_user_id:
            try:
                api_user = APIUser.get(APIUser.id == api_user_id)
                device.api_user = api_user
            except APIUser.DoesNotExist:
                logger.warning(f"API user not found: {api_user_id}")
                return web.json_response({'error': 'API user not found'}, status=404)

        device.save()
        logger.info(f"Device updated: {device.id}")
        return web.json_response(serialize_device(device))
    except Device.DoesNotExist:
        logger.warning(f"Device not found: {device_id}")
        return web.json_response({'error': 'Device not found'}, status=404)


async def delete_device(request):
    device_id = int(request.match_info['id'])
    logger.info(f"Deleting device with ID: {device_id}")

    try:
        device = Device.get(Device.id == device_id)
        device.delete_instance()
        logger.info(f"Device deleted: {device_id}")
        return web.json_response({'message': 'Device deleted successfully'})
    except Device.DoesNotExist:
        logger.warning(f"Device not found: {device_id}")
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

    if db.is_closed():
        db.connect()

    return app


async def close_db():
    if not db.is_closed():
        db.close()

if __name__ == '__main__':
    app = init_app()
    web.run_app(app, host='localhost', port=8080)
