import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ContactoBase(BaseModel):
    nombre: str
    cargo: str | None = None
    email: str | None = None
    telefono: str | None = None
    extension: str | None = None
    departamento: str | None = None


class ContactoCreate(ContactoBase):
    pass


class ContactoUpdate(BaseModel):
    nombre: str | None = None
    cargo: str | None = None
    email: str | None = None
    telefono: str | None = None
    extension: str | None = None
    departamento: str | None = None


class ContactoResponse(ContactoBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
