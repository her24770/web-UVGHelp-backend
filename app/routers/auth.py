import hashlib
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse
from app.utils.auth import create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


# login con email y password, retorna JWT bearer token
@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == body.email).first()
    if not user or user.password_hash != hashlib.sha256(body.password.encode()).hexdigest():
        raise HTTPException(
            status_code=401,
            detail={"error": True, "code": "UNAUTHORIZED", "message": "Credenciales inválidas", "status": 401},
        )
    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}


# retorna el usuario autenticado según el token enviado
@router.get("/me", response_model=UsuarioResponse)
def me(current_user=Depends(get_current_user)):
    return current_user
