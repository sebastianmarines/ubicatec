import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class Device(SQLModel, table=True):
    __tablename__ = "devices"
    id: Optional[int] = Field(default=None, primary_key=True)
    mac_address: str = Field(default=None, index=True)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False, index=True)
    sensor_id: str = Field(index=True)


class Temperature(SQLModel, table=True):
    __tablename__ = "temperatures"
    id: Optional[int] = Field(default=None, primary_key=True)
    temperature: float = Field(default=None)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False, index=True)
    sensor_id: str = Field(index=True)


class DBConfig(BaseModel):
    username: str
    password: str
    dbname: str
    host: str
    port: str

    def get_connection_string(self):
        return f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"

