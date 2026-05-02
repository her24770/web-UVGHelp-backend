import uuid
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.servicio import Servicio
from app.schemas.servicio import ServicioCreate, ServicioUpdate, ServicioResponse
from app.schemas.pagination import PagedResponse
from app.services import crud
from app.utils.responses import raise_not_found
from app.utils.auth import get_current_user
from app.utils.pagination import paginate

router = APIRouter(prefix="/api/servicios", tags=["servicios"], dependencies=[Depends(get_current_user)])


# retorna servicios paginados, con búsqueda por nombre y ordenamiento
@router.get("", response_model=PagedResponse[ServicioResponse])
def listar_servicios(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    q: str | None = Query(None),
    sort: str | None = Query(None),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    return paginate(db, Servicio, page, limit, q, sort, order)


# retorna un servicio por id, error 404 si no existe
@router.get("/{id}", response_model=ServicioResponse)
def obtener_servicio(id: uuid.UUID, db: Session = Depends(get_db)):
    servicio = crud.get_by_id(db, Servicio, id)
    if not servicio:
        raise_not_found("Servicio", id)
    return servicio


# crea un nuevo servicio, retorna 201 con el objeto creado
@router.post("", response_model=ServicioResponse, status_code=status.HTTP_201_CREATED)
def crear_servicio(data: ServicioCreate, db: Session = Depends(get_db)):
    return crud.create(db, Servicio, data.model_dump())


# actualiza un servicio por id, error 404 si no existe
@router.put("/{id}", response_model=ServicioResponse)
def actualizar_servicio(id: uuid.UUID, data: ServicioUpdate, db: Session = Depends(get_db)):
    servicio = crud.get_by_id(db, Servicio, id)
    if not servicio:
        raise_not_found("Servicio", id)
    return crud.update(db, servicio, data.model_dump(exclude_unset=True))


# elimina un servicio por id, retorna 204, error 404 si no existe
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_servicio(id: uuid.UUID, db: Session = Depends(get_db)):
    servicio = crud.get_by_id(db, Servicio, id)
    if not servicio:
        raise_not_found("Servicio", id)
    crud.delete(db, servicio)
