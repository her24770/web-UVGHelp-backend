import uuid
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.evento import Evento
from app.schemas.evento import EventoCreate, EventoUpdate, EventoResponse
from app.schemas.pagination import PagedResponse
from app.services import crud
from app.utils.responses import raise_not_found
from app.utils.auth import get_current_user
from app.utils.pagination import paginate

router = APIRouter(prefix="/api/eventos", tags=["eventos"], dependencies=[Depends(get_current_user)])


# retorna eventos paginados, con búsqueda por título y ordenamiento
@router.get("", response_model=PagedResponse[EventoResponse])
def listar_eventos(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    q: str | None = Query(None),
    sort: str | None = Query(None),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    return paginate(db, Evento, page, limit, q, sort, order, search_field="titulo")


# retorna un evento por id, error 404 si no existe
@router.get("/{id}", response_model=EventoResponse)
def obtener_evento(id: uuid.UUID, db: Session = Depends(get_db)):
    evento = crud.get_by_id(db, Evento, id)
    if not evento:
        raise_not_found("Evento", id)
    return evento


# crea un nuevo evento, retorna 201 con el objeto creado
@router.post("", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
def crear_evento(data: EventoCreate, db: Session = Depends(get_db)):
    return crud.create(db, Evento, data.model_dump())


# actualiza un evento por id, error 404 si no existe
@router.put("/{id}", response_model=EventoResponse)
def actualizar_evento(id: uuid.UUID, data: EventoUpdate, db: Session = Depends(get_db)):
    evento = crud.get_by_id(db, Evento, id)
    if not evento:
        raise_not_found("Evento", id)
    return crud.update(db, evento, data.model_dump(exclude_unset=True))


# elimina un evento por id, retorna 204, error 404 si no existe
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_evento(id: uuid.UUID, db: Session = Depends(get_db)):
    evento = crud.get_by_id(db, Evento, id)
    if not evento:
        raise_not_found("Evento", id)
    crud.delete(db, evento)
