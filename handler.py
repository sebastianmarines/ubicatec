import os
from utils import get_secret

from models import Device, Sensor, Location
from sqlmodel import Session, create_engine

from jinja2 import Environment, FileSystemLoader

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


def web_app_handler(event: dict, _context):
    locations = [Location(lat=25.64941614243979, lon=-100.28944203445873, occupancy=1000),
         Location(lat=25.651384675654, lon=-100.28909563433821, occupancy=800)]

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html.jinja2")
    html = template.render(locations=locations)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": html
    }
