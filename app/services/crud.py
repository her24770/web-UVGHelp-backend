from typing import Type, TypeVar
from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar("T")


# retorna todos los registros de la entidad
def get_all(db: Session, model: Type[T]) -> list:
    return list(db.execute(select(model)).scalars().all())


# busca un registro por id, retorna None si no existe
def get_by_id(db: Session, model: Type[T], id) -> T | None:
    return db.get(model, id)


# inserta un nuevo registro y retorna el objeto con su id generado
def create(db: Session, model: Type[T], data: dict) -> T:
    obj = model(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# actualiza solo los campos presentes en data, ignora los no enviados
def update(db: Session, obj: T, data: dict) -> T:
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


# elimina el registro de la base de datos
def delete(db: Session, obj) -> None:
    db.delete(obj)
    db.commit()
