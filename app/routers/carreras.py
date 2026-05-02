import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.carrera import Carrera
from app.schemas.carrera import CarreraCreate, CarreraUpdate, CarreraResponse
from app.services import crud
from app.utils.responses import raise_not_found
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/carreras", tags=["carreras"], dependencies=[Depends(get_current_user)])


# retorna lista de todas las carreras
@router.get("", response_model=list[CarreraResponse])
def listar_carreras(db: Session = Depends(get_db)):
    return crud.get_all(db, Carrera)


# retorna una carrera por id, error 404 si no existe
@router.get("/{id}", response_model=CarreraResponse)
def obtener_carrera(id: uuid.UUID, db: Session = Depends(get_db)):
    carrera = crud.get_by_id(db, Carrera, id)
    if not carrera:
        raise_not_found("Carrera", id)
    return carrera


# crea una nueva carrera, retorna 201 con el objeto creado
@router.post("", response_model=CarreraResponse, status_code=status.HTTP_201_CREATED)
def crear_carrera(data: CarreraCreate, db: Session = Depends(get_db)):
    return crud.create(db, Carrera, data.model_dump())


# actualiza una carrera por id, error 404 si no existe
@router.put("/{id}", response_model=CarreraResponse)
def actualizar_carrera(id: uuid.UUID, data: CarreraUpdate, db: Session = Depends(get_db)):
    carrera = crud.get_by_id(db, Carrera, id)
    if not carrera:
        raise_not_found("Carrera", id)
    return crud.update(db, carrera, data.model_dump(exclude_unset=True))


# elimina una carrera por id, retorna 204, error 404 si no existe
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_carrera(id: uuid.UUID, db: Session = Depends(get_db)):
    carrera = crud.get_by_id(db, Carrera, id)
    if not carrera:
        raise_not_found("Carrera", id)
    crud.delete(db, carrera)
