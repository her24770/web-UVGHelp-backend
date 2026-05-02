from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from app.routers import lugares, carreras, contactos, pagos, eventos, servicios, profesores, usuarios, cursos, auth

app = FastAPI(
    title="UVGHelp API",
    description="API REST para el sistema de información universitaria UVGHelp — Universidad del Valle de Guatemala",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# formatea todos los errores HTTP al formato estándar { error, code, message, status }
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "code": str(exc.status_code), "message": str(exc.detail), "status": exc.status_code},
    )


# captura errores de validación de Pydantic y los retorna en formato estándar con detalle por campo
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = [{"field": ".".join(str(loc) for loc in e["loc"]), "msg": e["msg"]} for e in exc.errors()]
    return JSONResponse(
        status_code=400,
        content={"error": True, "code": "VALIDATION_ERROR", "message": "Error de validación en los datos enviados", "details": errors, "status": 400},
    )


app.include_router(auth.router)
app.include_router(lugares.router)
app.include_router(carreras.router)
app.include_router(contactos.router)
app.include_router(pagos.router)
app.include_router(eventos.router)
app.include_router(servicios.router)
app.include_router(profesores.router)
app.include_router(usuarios.router)
app.include_router(cursos.router)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "message": "UVGHelp API corriendo"}
