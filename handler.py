import os
from utils import get_secret

from models import Device, Sensor
from sqlmodel import Session, create_engine

ENV = os.environ.get("AWS_EXECUTION_ENV", "dev")
DB_SECRETS_ARN = os.environ.get("DB_SECRETS_ARN")

db_config = get_secret(DB_SECRETS_ARN, ENV)
db_url = db_config.get_connection_string()
engine = create_engine(db_url, echo=ENV == "dev")


def iot_handler(event: dict, _context):

    sensor_id = event.get("client_id")
    with Session(engine) as session:
        sensor = session.query(Sensor).filter(Sensor.id == sensor_id).first()
        if not sensor:
            sensor = Sensor(id=sensor_id)
            session.add(sensor)
            session.commit()
            session.refresh(sensor)

    data = event.get("data")
    if type(data) != list:
        # TODO: Handle DHT11 sensor data coming as a string
        ...

    with Session(engine) as session:
        objects = [Device(sensor_id=sensor.id, mac_address=mac_address) for mac_address in data]
        session.bulk_save_objects(objects)
        session.commit()

    return "ok"
