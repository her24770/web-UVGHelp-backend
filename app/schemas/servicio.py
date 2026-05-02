import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ServicioBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    categoria: str | None = None
    horario: str | None = None
    contacto_id: uuid.UUID | None = None


class ServicioCreate(ServicioBase):
    pass


class ServicioUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    categoria: str | None = None
    horario: str | None = None
    contacto_id: uuid.UUID | None = None


class ServicioResponse(ServicioBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
