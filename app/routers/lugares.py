import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.lugar import Lugar
from app.schemas.lugar import LugarCreate, LugarUpdate, LugarResponse
from app.services import crud
from app.utils.responses import raise_not_found
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/lugares", tags=["lugares"], dependencies=[Depends(get_current_user)])


# retorna lista de todos los lugares
@router.get("", response_model=list[LugarResponse])
def listar_lugares(db: Session = Depends(get_db)):
    return crud.get_all(db, Lugar)


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
