import uuid
import hashlib
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.schemas.pagination import PagedResponse
from app.services import crud
from app.utils.responses import raise_not_found
from app.utils.auth import get_current_user
from app.utils.pagination import paginate

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"], dependencies=[Depends(get_current_user)])


# convierte password en texto plano a hash SHA-256 antes de guardar
def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# retorna usuarios paginados, con búsqueda por nombre y ordenamiento
@router.get("", response_model=PagedResponse[UsuarioResponse])
def listar_usuarios(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    q: str | None = Query(None),
    sort: str | None = Query(None),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    return paginate(db, Usuario, page, limit, q, sort, order)


# retorna un usuario por id, error 404 si no existe
@router.get("/{id}", response_model=UsuarioResponse)
def obtener_usuario(id: uuid.UUID, db: Session = Depends(get_db)):
    usuario = crud.get_by_id(db, Usuario, id)
    if not usuario:
        raise_not_found("Usuario", id)
    return usuario


# crea un usuario nuevo, hashea el password antes de guardarlo, retorna 201
@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    obj = data.model_dump()
    obj["password_hash"] = _hash(obj.pop("password"))
    return crud.create(db, Usuario, obj)


# actualiza un usuario por id, si viene password lo hashea, error 404 si no existe
@router.put("/{id}", response_model=UsuarioResponse)
def actualizar_usuario(id: uuid.UUID, data: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = crud.get_by_id(db, Usuario, id)
    if not usuario:
        raise_not_found("Usuario", id)
    obj = data.model_dump(exclude_unset=True)
    if "password" in obj:
        obj["password_hash"] = _hash(obj.pop("password"))
    return crud.update(db, usuario, obj)


# elimina un usuario por id, retorna 204, error 404 si no existe
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id: uuid.UUID, db: Session = Depends(get_db)):
    usuario = crud.get_by_id(db, Usuario, id)
    if not usuario:
        raise_not_found("Usuario", id)
    crud.delete(db, usuario)
