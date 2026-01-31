from pydantic import BaseModel
import enum

# Enums

class ModelStatus(str, enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"

class PredictionLabel(str, enum.Enum):
    UP = "UP"
    DOWN = "DOWN"




# Schema
class User(BaseModel):
    name: str
    email:str
    password:str
    role: str


