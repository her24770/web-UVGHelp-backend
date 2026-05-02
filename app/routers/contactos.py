import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.contacto import Contacto
from app.schemas.contacto import ContactoCreate, ContactoUpdate, ContactoResponse
from app.services import crud
from app.utils.responses import raise_not_found
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/contactos", tags=["contactos"], dependencies=[Depends(get_current_user)])


# retorna lista de todos los contactos
@router.get("", response_model=list[ContactoResponse])
def listar_contactos(db: Session = Depends(get_db)):
    return crud.get_all(db, Contacto)


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
