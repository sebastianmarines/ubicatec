import os
from utils import get_secret

from models import Device
from sqlmodel import Session, create_engine

ENV = os.environ.get("AWS_EXECUTION_ENV", "dev")
DB_SECRETS_ARN = os.environ.get("DB_SECRETS_ARN")

db_config = get_secret(DB_SECRETS_ARN, ENV)
db_url = db_config.get_connection_string()
engine = create_engine(db_url, echo=ENV == "dev")


def iot_handler(event: dict, _context):

    iot_device = event.get("client_id")

    data = event.get("data")
    if type(data) != list:
        # TODO: Handle DHT11 sensor data coming as a string
        ...

    with Session(engine) as session:
        objects = [Device(sensor_id=iot_device, mac_address=mac_address) for mac_address in data]
        session.bulk_save_objects(objects)
        session.commit()

    return "ok"
