import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.curso import Curso
from app.schemas.curso import CursoCreate, CursoUpdate, CursoResponse
from app.services import crud
from app.utils.responses import raise_not_found
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/cursos", tags=["cursos"], dependencies=[Depends(get_current_user)])


# retorna lista de todos los cursos
@router.get("", response_model=list[CursoResponse])
def listar_cursos(db: Session = Depends(get_db)):
    return crud.get_all(db, Curso)


# retorna un curso por id, error 404 si no existe
@router.get("/{id}", response_model=CursoResponse)
def obtener_curso(id: uuid.UUID, db: Session = Depends(get_db)):
    curso = crud.get_by_id(db, Curso, id)
    if not curso:
        raise_not_found("Curso", id)
    return curso


# crea un nuevo curso, retorna 201 con el objeto creado
@router.post("", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def crear_curso(data: CursoCreate, db: Session = Depends(get_db)):
    return crud.create(db, Curso, data.model_dump())


# actualiza un curso por id, error 404 si no existe
@router.put("/{id}", response_model=CursoResponse)
def actualizar_curso(id: uuid.UUID, data: CursoUpdate, db: Session = Depends(get_db)):
    curso = crud.get_by_id(db, Curso, id)
    if not curso:
        raise_not_found("Curso", id)
    return crud.update(db, curso, data.model_dump(exclude_unset=True))


# elimina un curso por id, retorna 204, error 404 si no existe
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_curso(id: uuid.UUID, db: Session = Depends(get_db)):
    curso = crud.get_by_id(db, Curso, id)
    if not curso:
        raise_not_found("Curso", id)
    crud.delete(db, curso)
