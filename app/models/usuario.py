import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(100))
    apellido: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    carnet: Mapped[str | None] = mapped_column(String(20), unique=True)
    carrera_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("carreras.id", ondelete="SET NULL"))
    rol: Mapped[str] = mapped_column(String(20), default="estudiante")
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    carrera: Mapped["Carrera | None"] = relationship("Carrera", back_populates="usuarios")
