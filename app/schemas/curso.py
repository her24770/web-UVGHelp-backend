import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CursoBase(BaseModel):
    nombre: str
    codigo: str | None = None
    creditos: int | None = None
    carrera_id: uuid.UUID | None = None
    profesor_id: uuid.UUID | None = None
    semestre: str | None = None


class CursoCreate(CursoBase):
    pass


class CursoUpdate(BaseModel):
    nombre: str | None = None
    codigo: str | None = None
    creditos: int | None = None
    carrera_id: uuid.UUID | None = None
    profesor_id: uuid.UUID | None = None
    semestre: str | None = None


class CursoResponse(CursoBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
