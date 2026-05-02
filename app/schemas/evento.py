import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EventoBase(BaseModel):
    titulo: str
    descripcion: str | None = None
    tipo: str | None = None
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    lugar_id: uuid.UUID | None = None
    imagen_url: str | None = None


class EventoCreate(EventoBase):
    pass


class EventoUpdate(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    tipo: str | None = None
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    lugar_id: uuid.UUID | None = None
    imagen_url: str | None = None


class EventoResponse(EventoBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
