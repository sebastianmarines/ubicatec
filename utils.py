import boto3
from models import DBConfig
import json


def get_secret(secret_arn: str, env: str) -> DBConfig:
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager')
    get_secret_value_response = client.get_secret_value(SecretId=secret_arn)

    secrets = json.loads(get_secret_value_response['SecretString'])

    db_config = DBConfig(**secrets)

    if env == "dev":
        db_config.dbname = "dev"

    return db_config
