import os
from utils import get_secret

from models import Device, Sensor, Location
from sqlmodel import Session, create_engine

from jinja2 import Environment, FileSystemLoader
from datetime import timedelta, datetime

ENV = os.environ.get("AWS_EXECUTION_ENV", "dev")
DB_SECRETS_ARN = os.environ.get("DB_SECRETS_ARN")
if DB_SECRETS_ARN == '[object Object]':
    # Serverless offline doesn't support referencing CloudFormation functions
    DB_SECRETS_ARN = "arn:aws:secretsmanager:us-east-1:780690093991:secret:RDSMasterCredentials-N5pBl5ozFz5g-hlA9F6"

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


def web_app_handler(_event: dict, _context):
    locations = []

    start = datetime.now() - timedelta(minutes=10)
    end = datetime.now()

    with Session(engine) as session:
        sensors = session.query(Sensor).filter((None != Sensor.lon) & (None != Sensor.lat)).all()
        for sensor in sensors:
            device_count_last_5_minutes = session.query(Device).filter(
                (start < Device.timestamp) & (Device.timestamp < end)).count()
            locations.append(Location(lat=sensor.lat, lon=sensor.lon, occupancy=device_count_last_5_minutes))

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html.jinja2")
    html = template.render(locations=locations)
    return {"statusCode": 200, "headers": {"Content-Type": "text/html"}, "body": html}
