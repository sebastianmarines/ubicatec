from models import IoTData
import os
from utils import get_secret

ENV = os.environ.get("AWS_EXECUTION_ENV", "dev")


def iot_handler(event: dict, _context):
    print(ENV)
    print(os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))
    print(os.environ.get("DB_SECRETS_ARN"))
    print(get_secret(os.environ.get("DB_SECRETS_ARN")))
    data = adapter(event)
    return data.json()


def adapter(event) -> IoTData:
    return IoTData(**event)
