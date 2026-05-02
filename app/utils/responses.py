from fastapi import HTTPException


# lanza error 404 con mensaje descriptivo cuando el recurso no existe
def raise_not_found(entity: str, id) -> None:
    raise HTTPException(
        status_code=404,
        detail={"error": True, "code": "NOT_FOUND", "message": f"{entity} con id '{id}' no existe", "status": 404},
    )


# lanza error 400 para datos inválidos o reglas de negocio no cumplidas
def raise_bad_request(message: str) -> None:
    raise HTTPException(
        status_code=400,
        detail={"error": True, "code": "BAD_REQUEST", "message": message, "status": 400},
    )
