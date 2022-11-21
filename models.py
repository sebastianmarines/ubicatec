from dataclasses import dataclass

from pydantic import BaseModel, Field
from typing import List, Union


class IoTData(BaseModel):
    data: Union[List[str], str]
    client_id: str = Field(alias="clientid")


@dataclass
class Config:
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: str

    def get_url_string(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

