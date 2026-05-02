import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Curso(Base):
    __tablename__ = "cursos"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(200))
    codigo: Mapped[str | None] = mapped_column(String(20))
    creditos: Mapped[int | None] = mapped_column(Integer)
    carrera_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("carreras.id", ondelete="SET NULL"))
    profesor_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("profesores.id", ondelete="SET NULL"))
    semestre: Mapped[str | None] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    carrera: Mapped["Carrera | None"] = relationship("Carrera", back_populates="cursos")
    profesor: Mapped["Profesor | None"] = relationship("Profesor", back_populates="cursos")
