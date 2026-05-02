import uuid
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.lugar import Lugar
from app.schemas.lugar import LugarCreate, LugarUpdate, LugarResponse
from app.schemas.pagination import PagedResponse
from app.services import crud
from app.utils.responses import raise_not_found
from app.utils.auth import get_current_user
from app.utils.pagination import paginate
from app.services.export_service import generate_csv, generate_xlsx
from fastapi.responses import Response

router = APIRouter(prefix="/api/lugares", tags=["lugares"], dependencies=[Depends(get_current_user)])


# retorna lugares paginados, con búsqueda por nombre y ordenamiento
@router.get("", response_model=PagedResponse[LugarResponse])
def listar_lugares(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    q: str | None = Query(None),
    sort: str | None = Query(None),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    return paginate(db, Lugar, page, limit, q, sort, order)


# retorna un lugar por id, error 404 si no existe
@router.get("/{id}", response_model=LugarResponse)
def obtener_lugar(id: uuid.UUID, db: Session = Depends(get_db)):
    lugar = crud.get_by_id(db, Lugar, id)
    if not lugar:
        raise_not_found("Lugar", id)
    return lugar


# crea un nuevo lugar, retorna 201 con el objeto creado
@router.post("", response_model=LugarResponse, status_code=status.HTTP_201_CREATED)
def crear_lugar(data: LugarCreate, db: Session = Depends(get_db)):
    return crud.create(db, Lugar, data.model_dump())


# actualiza un lugar por id, error 404 si no existe
@router.put("/{id}", response_model=LugarResponse)
def actualizar_lugar(id: uuid.UUID, data: LugarUpdate, db: Session = Depends(get_db)):
    lugar = crud.get_by_id(db, Lugar, id)
    if not lugar:
        raise_not_found("Lugar", id)
    return crud.update(db, lugar, data.model_dump(exclude_unset=True))


# elimina un lugar por id, retorna 204, error 404 si no existe
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_lugar(id: uuid.UUID, db: Session = Depends(get_db)):
    lugar = crud.get_by_id(db, Lugar, id)
    if not lugar:
        raise_not_found("Lugar", id)
    crud.delete(db, lugar)


# exporta todos los lugares a CSV descargable
@router.get("/export/csv")
def exportar_csv(db: Session = Depends(get_db)):
    content = generate_csv(db, Lugar)
    return Response(content=content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=lugares.csv"})


# exporta todos los lugares a Excel XLSX descargable
@router.get("/export/xlsx")
def exportar_xlsx(db: Session = Depends(get_db)):
    content = generate_xlsx(db, Lugar)
    return Response(content=content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=lugares.xlsx"})
