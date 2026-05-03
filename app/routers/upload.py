import uuid
import os
from fastapi import APIRouter, UploadFile, File, Request
from app.utils.responses import raise_bad_request

router = APIRouter(prefix="/api/upload", tags=["upload"])

# límites y tipos aceptados — se validan por content_type y extensión
MAX_SIZE_BYTES = 1 * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
UPLOADS_DIR = "static/uploads"


# recibe una imagen, valida tipo y tamaño, la guarda en static/uploads y retorna la URL accesible
@router.post("/imagen", status_code=201)
async def upload_imagen(request: Request, file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename or "")[1].lower()

    # se verifica tanto el MIME type como la extensión para evitar spoofing
    if file.content_type not in ALLOWED_TYPES or ext not in ALLOWED_EXTENSIONS:
        raise_bad_request("Tipo de archivo no permitido. Solo se aceptan jpg, png y webp.")

    # se lee completo antes de guardar para poder medir el tamaño real
    contents = await file.read()

    if len(contents) > MAX_SIZE_BYTES:
        raise_bad_request("El archivo supera el límite de 1MB.")

    # nombre único con uuid para evitar colisiones entre archivos
    filename = f"{uuid.uuid4()}{ext}"
    dest = os.path.join(UPLOADS_DIR, filename)

    with open(dest, "wb") as f:
        f.write(contents)

    # base_url dinámico para que la URL funcione igual en local y en producción
    base_url = str(request.base_url).rstrip("/")
    return {"url": f"{base_url}/static/uploads/{filename}", "filename": filename}
