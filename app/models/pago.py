import uuid
from datetime import datetime
from sqlalchemy import String, Text, Numeric, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Pago(Base):
    __tablename__ = "pagos"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    concepto: Mapped[str] = mapped_column(String(200))
    tipo: Mapped[str | None] = mapped_column(String(50))
    monto: Mapped[float] = mapped_column(Numeric(10, 2))
    moneda: Mapped[str] = mapped_column(String(10), default="GTQ")
    descripcion: Mapped[str | None] = mapped_column(Text)
    periodo: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
