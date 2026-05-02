import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProfesorBase(BaseModel):
    nombre: str
    apellido: str
    email: str | None = None
    telefono: str | None = None
    carrera_id: uuid.UUID | None = None
    departamento: str | None = None


class ProfesorCreate(ProfesorBase):
    pass


class ProfesorUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    email: str | None = None
    telefono: str | None = None
    carrera_id: uuid.UUID | None = None
    departamento: str | None = None


class ProfesorResponse(ProfesorBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
