from pydantic import BaseModel, Field


class IoTData(BaseModel):
    data: list[str] | str
    client_id: str = Field(alias="clientid")
