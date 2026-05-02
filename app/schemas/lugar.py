import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LugarBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    edificio: str | None = None
    piso: str | None = None
    categoria: str | None = None
    horario_apertura: str | None = None
    horario_cierre: str | None = None
    imagen_url: str | None = None


class LugarCreate(LugarBase):
    pass


class LugarUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    edificio: str | None = None
    piso: str | None = None
    categoria: str | None = None
    horario_apertura: str | None = None
    horario_cierre: str | None = None
    imagen_url: str | None = None


class LugarResponse(LugarBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
