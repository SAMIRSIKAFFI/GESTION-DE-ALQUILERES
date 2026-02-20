"""
Endpoints de Contratos
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import date
from app.core.dependencies import get_db, get_current_active_user
from app.models.contrato import Contrato
from app.models.propiedad import Propiedad

router = APIRouter()


class ContratoCreate(BaseModel):
    numero_contrato: str
    propiedad_id: int
    inquilino_id: int
    fecha_inicio: date
    fecha_fin: date
    canon_mensual: float
    garantia: float
    incremento_anual: float = 0
    dia_pago: int = 5
    tasa_mora_diaria: float = 0.5


class ContratoResponse(BaseModel):
    id: int
    numero_contrato: str
    propiedad_id: int
    inquilino_id: int
    fecha_inicio: date
    fecha_fin: date
    canon_mensual: float
    garantia: float
    estado: str
    
    class Config:
        from_attributes = True


@router.post("/contratos", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
def crear_contrato(
    contrato_data: ContratoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Crear nuevo contrato"""
    # Verificar que la propiedad existe y pertenece al usuario
    propiedad = db.query(Propiedad).filter(
        Propiedad.id == contrato_data.propiedad_id,
         ).first()
    
    if not propiedad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Propiedad no encontrada"
        )
    
    # Verificar número de contrato único
    existing = db.query(Contrato).filter(
        Contrato.numero_contrato == contrato_data.numero_contrato
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un contrato con este número"
        )
    
    nuevo_contrato = Contrato(**contrato_data.dict())
    db.add(nuevo_contrato)
    db.commit()
    db.refresh(nuevo_contrato)
    
    return nuevo_contrato


@router.get("/contratos", response_model=List[ContratoResponse])
def listar_contratos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Listar todos los contratos"""
    contratos = db.query(Contrato).join(Propiedad).filter(
        Contrato.deleted_at == None
    ).offset(skip).limit(limit).all()
    
    return contratos


@router.get("/contratos/{contrato_id}", response_model=ContratoResponse)
def obtener_contrato(
    contrato_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtener detalles de un contrato"""
    contrato = db.query(Contrato).join(Propiedad).filter(
        Contrato.id == contrato_id,
                Contrato.deleted_at == None
    ).first()
    
    if not contrato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato no encontrado"
        )
    
    return contrato
