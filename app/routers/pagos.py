import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.pago import Pago
from app.schemas.pago import PagoCreate, PagoUpdate, PagoResponse
from app.services import crud
from app.utils.responses import raise_not_found
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/pagos", tags=["pagos"], dependencies=[Depends(get_current_user)])


# retorna lista de todos los pagos/aranceles
@router.get("", response_model=list[PagoResponse])
def listar_pagos(db: Session = Depends(get_db)):
    return crud.get_all(db, Pago)


# retorna un pago por id, error 404 si no existe
@router.get("/{id}", response_model=PagoResponse)
def obtener_pago(id: uuid.UUID, db: Session = Depends(get_db)):
    pago = crud.get_by_id(db, Pago, id)
    if not pago:
        raise_not_found("Pago", id)
    return pago


# crea un nuevo registro de pago, retorna 201 con el objeto creado
@router.post("", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def crear_pago(data: PagoCreate, db: Session = Depends(get_db)):
    return crud.create(db, Pago, data.model_dump())


# actualiza un pago por id, error 404 si no existe
@router.put("/{id}", response_model=PagoResponse)
def actualizar_pago(id: uuid.UUID, data: PagoUpdate, db: Session = Depends(get_db)):
    pago = crud.get_by_id(db, Pago, id)
    if not pago:
        raise_not_found("Pago", id)
    return crud.update(db, pago, data.model_dump(exclude_unset=True))


# elimina un pago por id, retorna 204, error 404 si no existe
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pago(id: uuid.UUID, db: Session = Depends(get_db)):
    pago = crud.get_by_id(db, Pago, id)
    if not pago:
        raise_not_found("Pago", id)
    crud.delete(db, pago)
