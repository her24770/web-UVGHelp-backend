import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    carnet: str | None = None
    carrera_id: uuid.UUID | None = None
    rol: str = "estudiante"


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    email: str | None = None
    carnet: str | None = None
    carrera_id: uuid.UUID | None = None
    rol: str | None = None
    password: str | None = None


class UsuarioResponse(UsuarioBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
