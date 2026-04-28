from pydantic import BaseModel
from typing import List

class SystemData(BaseModel):
    # Agregamos timestamp porque tu recolector y modelo lo usan
    timestamp: str 
    cpu: float
    ram: float
    disk: float
    machine_id: str

class SystemDataBatch(BaseModel):
    observations: List[SystemData]