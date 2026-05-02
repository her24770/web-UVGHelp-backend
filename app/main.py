from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "message": "UVGHelp API corriendo"}
