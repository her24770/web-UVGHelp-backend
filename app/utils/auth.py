from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db

# esquema OAuth2 — le dice a Swagger dónde está el endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# genera un token JWT con el id del usuario y tiempo de expiración
def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRE_HOURS)
    return jwt.encode({"sub": user_id, "exp": expire}, settings.JWT_SECRET, algorithm="HS256")


# valida el token y retorna el usuario autenticado, error 401 si es inválido o expirado
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from app.models.usuario import Usuario
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if not user_id:
            raise ValueError
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=401,
            detail={"error": True, "code": "UNAUTHORIZED", "message": "Token inválido o expirado", "status": 401},
        )
    user = db.get(Usuario, user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "code": "UNAUTHORIZED", "message": "Usuario no encontrado", "status": 401},
        )
    return user
