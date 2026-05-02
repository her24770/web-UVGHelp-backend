import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PagoBase(BaseModel):
    concepto: str
    tipo: str | None = None
    monto: float
    moneda: str = "GTQ"
    descripcion: str | None = None
    periodo: str | None = None


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    concepto: str | None = None
    tipo: str | None = None
    monto: float | None = None
    moneda: str | None = None
    descripcion: str | None = None
    periodo: str | None = None


class PagoResponse(PagoBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
