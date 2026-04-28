from pydantic import BaseModel

class SystemData(BaseModel):
    cpu: float
    ram: float
    disk: float