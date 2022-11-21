import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mac_address: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False, index=True)
    sensor_id: str = Field(index=True)


class DBConfig(BaseModel):
    username: str
    password: str
    dbname: str
    host: str
    port: str

    def get_connection_string(self):
        return f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"

