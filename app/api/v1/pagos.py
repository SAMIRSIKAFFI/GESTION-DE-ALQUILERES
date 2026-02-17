"""
Endpoints de Pagos
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import date
from app.core.dependencies import get_db, get_current_active_user
from app.models.pago import Pago, EstadoPago, FormaPago
from app.models.contrato import Contrato
from app.models.propiedad import Propiedad
from app.services.mora_calculator import MoraCalculator
from app.services.payment_distributor import PaymentDistributor

router = APIRouter()


class PagoCreate(BaseModel):
    contrato_id: int
    periodo: str  # YYYY-MM
    fecha_vencimiento: date
    monto_esperado: float


class PagoRegistrar(BaseModel):
    monto_pagado: float
    fecha_pago: date
    forma_pago: FormaPago
    numero_comprobante: str = None
    nota: str = None


class PagoResponse(BaseModel):
    id: int
    contrato_id: int
    periodo: str
    fecha_vencimiento: date
    monto_esperado: float
    monto_pagado: float
    mora_calculada: float
    dias_atraso: int
    estado: str
    
    class Config:
        from_attributes = True


@router.post("/pagos", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def crear_pago(
    pago_data: PagoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Crear nuevo registro de pago (pendiente)"""
    # Verificar contrato
    contrato = db.query(Contrato).join(Propiedad).filter(
        Contrato.id == pago_data.contrato_id,
        Propiedad.empresa_id == current_user.empresa_id
    ).first()
    
    if not contrato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato no encontrado"
        )
    
    # Extraer año y mes del periodo
    anio, mes = map(int, pago_data.periodo.split('-'))
    
    nuevo_pago = Pago(
        contrato_id=pago_data.contrato_id,
        periodo=pago_data.periodo,
        anio=anio,
        mes=mes,
        fecha_vencimiento=pago_data.fecha_vencimiento,
        monto_esperado=pago_data.monto_esperado
    )
    
    db.add(nuevo_pago)
    db.commit()
    db.refresh(nuevo_pago)
    
    return nuevo_pago


@router.post("/pagos/{pago_id}/registrar", response_model=dict)
def registrar_pago(
    pago_id: int,
    pago_data: PagoRegistrar,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Registrar un pago efectuado y distribuir automáticamente a copropietarios
    """
    # Obtener pago
    pago = db.query(Pago).join(Contrato).join(Propiedad).filter(
        Pago.id == pago_id,
        Propiedad.empresa_id == current_user.empresa_id
    ).first()
    
    if not pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado"
        )
    
    # Actualizar información del pago
    pago.monto_pagado = pago_data.monto_pagado
    pago.fecha_pago = pago_data.fecha_pago
    pago.forma_pago = pago_data.forma_pago
    pago.numero_comprobante = pago_data.numero_comprobante
    pago.nota = pago_data.nota
    
    # Determinar estado
    if pago.monto_pagado >= pago.monto_esperado:
        pago.estado = EstadoPago.PAGADO
    elif pago.monto_pagado > 0:
        pago.estado = EstadoPago.PARCIAL
    
    db.commit()
    
    # Calcular mora
    mora_info = MoraCalculator.actualizar_mora_pago(db, pago_id)
    
    # Distribuir a copropietarios si aplica
    try:
        distribucion_info = PaymentDistributor.distribuir_pago(db, pago_id)
    except ValueError as e:
        distribucion_info = {"error": str(e)}
    
    return {
        "pago": {
            "id": pago.id,
            "periodo": pago.periodo,
            "monto_pagado": pago.monto_pagado,
            "estado": pago.estado.value
        },
        "mora": mora_info,
        "distribucion": distribucion_info
    }


@router.get("/pagos/contrato/{contrato_id}", response_model=List[PagoResponse])
def listar_pagos_contrato(
    contrato_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Listar todos los pagos de un contrato"""
    # Verificar contrato
    contrato = db.query(Contrato).join(Propiedad).filter(
        Contrato.id == contrato_id,
        Propiedad.empresa_id == current_user.empresa_id
    ).first()
    
    if not contrato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato no encontrado"
        )
    
    pagos = db.query(Pago).filter(
        Pago.contrato_id == contrato_id,
        Pago.deleted_at == None
    ).all()
    
    return pagos


@router.get("/pagos/{pago_id}/mora")
def calcular_mora_pago(
    pago_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Calcular mora actual de un pago"""
    try:
        mora_info = MoraCalculator.actualizar_mora_pago(db, pago_id)
        return mora_info
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
