import uuid
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.profesor import Profesor
from app.schemas.profesor import ProfesorCreate, ProfesorUpdate, ProfesorResponse
from app.schemas.pagination import PagedResponse
from app.services import crud
from app.utils.responses import raise_not_found
from app.utils.auth import get_current_user
from app.utils.pagination import paginate

router = APIRouter(prefix="/api/profesores", tags=["profesores"], dependencies=[Depends(get_current_user)])


# retorna profesores paginados, con búsqueda por nombre y ordenamiento
@router.get("", response_model=PagedResponse[ProfesorResponse])
def listar_profesores(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    q: str | None = Query(None),
    sort: str | None = Query(None),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    return paginate(db, Profesor, page, limit, q, sort, order)


# retorna un profesor por id, error 404 si no existe
@router.get("/{id}", response_model=ProfesorResponse)
def obtener_profesor(id: uuid.UUID, db: Session = Depends(get_db)):
    profesor = crud.get_by_id(db, Profesor, id)
    if not profesor:
        raise_not_found("Profesor", id)
    return profesor


# crea un nuevo profesor, retorna 201 con el objeto creado
@router.post("", response_model=ProfesorResponse, status_code=status.HTTP_201_CREATED)
def crear_profesor(data: ProfesorCreate, db: Session = Depends(get_db)):
    return crud.create(db, Profesor, data.model_dump())


# actualiza un profesor por id, error 404 si no existe
@router.put("/{id}", response_model=ProfesorResponse)
def actualizar_profesor(id: uuid.UUID, data: ProfesorUpdate, db: Session = Depends(get_db)):
    profesor = crud.get_by_id(db, Profesor, id)
    if not profesor:
        raise_not_found("Profesor", id)
    return crud.update(db, profesor, data.model_dump(exclude_unset=True))


# elimina un profesor por id, retorna 204, error 404 si no existe
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_profesor(id: uuid.UUID, db: Session = Depends(get_db)):
    profesor = crud.get_by_id(db, Profesor, id)
    if not profesor:
        raise_not_found("Profesor", id)
    crud.delete(db, profesor)
