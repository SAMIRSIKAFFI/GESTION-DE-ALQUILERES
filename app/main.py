"""
Sistema Profesional de Gestión de Alquileres
Punto de entrada de la aplicación FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.database.base import Base
from app.database.session import engine
import app.models  # Importar todos los modelos

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistema profesional de gestión de alquileres con soporte para copropiedades",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar routers
from app.api.v1 import auth, propiedades, inquilinos, contratos, pagos, reportes, impuestos

# Registrar routers
app.include_router(auth.router, prefix="/api/v1", tags=["Autenticación"])
app.include_router(propiedades.router, prefix="/api/v1", tags=["Propiedades"])
app.include_router(inquilinos.router, prefix="/api/v1", tags=["Inquilinos"])
app.include_router(contratos.router, prefix="/api/v1", tags=["Contratos"])
app.include_router(pagos.router, prefix="/api/v1", tags=["Pagos"])
app.include_router(impuestos.router, prefix="/api/v1", tags=["Impuestos"])

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/app")
def serve_app():
    return FileResponse("frontend/index.html")

@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "mensaje": "Sistema de Gestión de Alquileres - API",
        "version": settings.APP_VERSION,
        "documentacion": "/docs",
        "estado": "activo"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
