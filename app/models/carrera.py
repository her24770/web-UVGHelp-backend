import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Carrera(Base):
    __tablename__ = "carreras"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(200))
    facultad: Mapped[str | None] = mapped_column(String(200))
    duracion_semestres: Mapped[int | None] = mapped_column(Integer)
    pensum_url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    profesores: Mapped[list["Profesor"]] = relationship("Profesor", back_populates="carrera")
    cursos: Mapped[list["Curso"]] = relationship("Curso", back_populates="carrera")
    usuarios: Mapped[list["Usuario"]] = relationship("Usuario", back_populates="carrera")
