import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Lugar(Base):
    __tablename__ = "lugares"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(200))
    descripcion: Mapped[str | None] = mapped_column(Text)
    edificio: Mapped[str | None] = mapped_column(String(100))
    piso: Mapped[str | None] = mapped_column(String(50))
    categoria: Mapped[str | None] = mapped_column(String(100))
    horario_apertura: Mapped[str | None] = mapped_column(String(10))
    horario_cierre: Mapped[str | None] = mapped_column(String(10))
    imagen_url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    eventos: Mapped[list["Evento"]] = relationship("Evento", back_populates="lugar")
