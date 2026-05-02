import uuid
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.contacto import Contacto
from app.schemas.contacto import ContactoCreate, ContactoUpdate, ContactoResponse
from app.schemas.pagination import PagedResponse
from app.services import crud
from app.utils.responses import raise_not_found
from app.utils.auth import get_current_user
from app.utils.pagination import paginate
from app.services.export_service import generate_csv, generate_xlsx
from fastapi.responses import Response

router = APIRouter(prefix="/api/contactos", tags=["contactos"], dependencies=[Depends(get_current_user)])


# retorna contactos paginados, con búsqueda por nombre y ordenamiento
@router.get("", response_model=PagedResponse[ContactoResponse])
def listar_contactos(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    q: str | None = Query(None),
    sort: str | None = Query(None),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    return paginate(db, Contacto, page, limit, q, sort, order)


# retorna un contacto por id, error 404 si no existe
@router.get("/{id}", response_model=ContactoResponse)
def obtener_contacto(id: uuid.UUID, db: Session = Depends(get_db)):
    contacto = crud.get_by_id(db, Contacto, id)
    if not contacto:
        raise_not_found("Contacto", id)
    return contacto


# crea un nuevo contacto, retorna 201 con el objeto creado
@router.post("", response_model=ContactoResponse, status_code=status.HTTP_201_CREATED)
def crear_contacto(data: ContactoCreate, db: Session = Depends(get_db)):
    return crud.create(db, Contacto, data.model_dump())


# actualiza un contacto por id, error 404 si no existe
@router.put("/{id}", response_model=ContactoResponse)
def actualizar_contacto(id: uuid.UUID, data: ContactoUpdate, db: Session = Depends(get_db)):
    contacto = crud.get_by_id(db, Contacto, id)
    if not contacto:
        raise_not_found("Contacto", id)
    return crud.update(db, contacto, data.model_dump(exclude_unset=True))


# elimina un contacto por id, retorna 204, error 404 si no existe
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_contacto(id: uuid.UUID, db: Session = Depends(get_db)):
    contacto = crud.get_by_id(db, Contacto, id)
    if not contacto:
        raise_not_found("Contacto", id)
    crud.delete(db, contacto)


@router.get("/export/csv")
def exportar_csv(db: Session = Depends(get_db)):
    content = generate_csv(db, Contacto)
    return Response(content=content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=contactos.csv"})


@router.get("/export/xlsx")
def exportar_xlsx(db: Session = Depends(get_db)):
    content = generate_xlsx(db, Contacto)
    return Response(content=content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=contactos.xlsx"})
