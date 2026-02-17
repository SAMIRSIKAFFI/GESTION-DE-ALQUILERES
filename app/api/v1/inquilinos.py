"""
Endpoints de Inquilinos
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.dependencies import get_db, get_current_active_user
from app.models.inquilino import Inquilino

router = APIRouter()


class InquilinoCreate(BaseModel):
    nombre_completo: str
    ci: str
    telefono: str = None
    email: str = None
    direccion_actual: str = None
    ocupacion: str = None


class InquilinoResponse(BaseModel):
    id: int
    nombre_completo: str
    ci: str
    telefono: str = None
    email: str = None
    estado: str
    
    class Config:
        from_attributes = True


@router.post("/inquilinos", response_model=InquilinoResponse, status_code=status.HTTP_201_CREATED)
def crear_inquilino(
    inquilino_data: InquilinoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Crear nuevo inquilino"""
    # Verificar si CI ya existe
    existing = db.query(Inquilino).filter(Inquilino.ci == inquilino_data.ci).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un inquilino con este CI"
        )
    
    nuevo_inquilino = Inquilino(**inquilino_data.dict())
    db.add(nuevo_inquilino)
    db.commit()
    db.refresh(nuevo_inquilino)
    
    return nuevo_inquilino


@router.get("/inquilinos", response_model=List[InquilinoResponse])
def listar_inquilinos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Listar todos los inquilinos"""
    inquilinos = db.query(Inquilino).filter(
        Inquilino.deleted_at == None
    ).offset(skip).limit(limit).all()
    
    return inquilinos


@router.get("/inquilinos/{inquilino_id}", response_model=InquilinoResponse)
def obtener_inquilino(
    inquilino_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtener detalles de un inquilino"""
    inquilino = db.query(Inquilino).filter(
        Inquilino.id == inquilino_id,
        Inquilino.deleted_at == None
    ).first()
    
    if not inquilino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inquilino no encontrado"
        )
    
    return inquilino
