import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CarreraBase(BaseModel):
    nombre: str
    facultad: str | None = None
    duracion_semestres: int | None = None
    pensum_url: str | None = None


class CarreraCreate(CarreraBase):
    pass


class CarreraUpdate(BaseModel):
    nombre: str | None = None
    facultad: str | None = None
    duracion_semestres: int | None = None
    pensum_url: str | None = None


class CarreraResponse(CarreraBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
