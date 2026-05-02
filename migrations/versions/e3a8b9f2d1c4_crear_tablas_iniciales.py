"""crear tablas iniciales

Revision ID: e3a8b9f2d1c4
Revises:
Create Date: 2026-05-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'e3a8b9f2d1c4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'carreras',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('facultad', sa.String(200), nullable=True),
        sa.Column('duracion_semestres', sa.Integer(), nullable=True),
        sa.Column('pensum_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'contactos',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('cargo', sa.String(100), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('telefono', sa.String(20), nullable=True),
        sa.Column('extension', sa.String(20), nullable=True),
        sa.Column('departamento', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'lugares',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('edificio', sa.String(100), nullable=True),
        sa.Column('piso', sa.String(50), nullable=True),
        sa.Column('categoria', sa.String(100), nullable=True),
        sa.Column('horario_apertura', sa.String(10), nullable=True),
        sa.Column('horario_cierre', sa.String(10), nullable=True),
        sa.Column('imagen_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'pagos',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('concepto', sa.String(200), nullable=False),
        sa.Column('tipo', sa.String(50), nullable=True),
        sa.Column('monto', sa.Numeric(10, 2), nullable=False),
        sa.Column('moneda', sa.String(10), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('periodo', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'profesores',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('apellido', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('telefono', sa.String(20), nullable=True),
        sa.Column('carrera_id', sa.Uuid(), nullable=True),
        sa.Column('departamento', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['carrera_id'], ['carreras.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('apellido', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('carnet', sa.String(20), nullable=True),
        sa.Column('carrera_id', sa.Uuid(), nullable=True),
        sa.Column('rol', sa.String(20), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['carrera_id'], ['carreras.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('carnet'),
    )
    op.create_table(
        'cursos',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('codigo', sa.String(20), nullable=True),
        sa.Column('creditos', sa.Integer(), nullable=True),
        sa.Column('carrera_id', sa.Uuid(), nullable=True),
        sa.Column('profesor_id', sa.Uuid(), nullable=True),
        sa.Column('semestre', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['carrera_id'], ['carreras.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['profesor_id'], ['profesores.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'eventos',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('titulo', sa.String(200), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('tipo', sa.String(50), nullable=True),
        sa.Column('fecha_inicio', sa.DateTime(timezone=True), nullable=True),
        sa.Column('fecha_fin', sa.DateTime(timezone=True), nullable=True),
        sa.Column('lugar_id', sa.Uuid(), nullable=True),
        sa.Column('imagen_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['lugar_id'], ['lugares.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'servicios',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('categoria', sa.String(100), nullable=True),
        sa.Column('horario', sa.String(200), nullable=True),
        sa.Column('contacto_id', sa.Uuid(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['contacto_id'], ['contactos.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('servicios')
    op.drop_table('eventos')
    op.drop_table('cursos')
    op.drop_table('usuarios')
    op.drop_table('profesores')
    op.drop_table('pagos')
    op.drop_table('lugares')
    op.drop_table('contactos')
    op.drop_table('carreras')
