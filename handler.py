from models import IoTData


def iot_handler(event: dict, context):
    data = adapter(event)
    return data.json()


def adapter(event) -> IoTData:
    return IoTData(**event)
