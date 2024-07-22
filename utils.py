def serialize_device(device):
    return {
        'id': device.id,
        'name': device.name,
        'type': device.type,
        'login': device.login,
        'location': device.location.name,
        'api_user': device.api_user.name
    }
