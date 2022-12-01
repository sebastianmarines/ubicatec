import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel


class Sensor(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    lat: Optional[float] = Field(default=None)
    lon: Optional[float] = Field(default=None)
    devices: List["Device"] = Relationship(back_populates="sensor")


class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mac_address: str = Field(default=None, index=True)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False, index=True)
    sensor_id: Optional[str] = Field(default=None, index=True, foreign_key="sensor.id")
    sensor: Optional[Sensor] = Relationship(back_populates="devices")


class Temperature(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    temperature: float = Field(default=None)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False, index=True)
    sensor_id: Optional[str] = Field(default=None, index=True, foreign_key="sensor.id")


class MqttMessage(BaseModel):
    client_id: str
    humidity: int
    temperature: float
    people: int


class Location(BaseModel):
    lat: float
    lon: float
    occupancy: int


class DBConfig(BaseModel):
    username: str
    password: str
    dbname: str
    host: str
    port: str

    def get_connection_string(self):
        return f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"
