"""
Endpoints de Reportes y Analytics
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from app.core.dependencies import get_db, get_current_active_user
from app.models.pago import Pago, EstadoPago
from app.models.contrato import Contrato
from app.models.propiedad import Propiedad
from app.models.copropietario import Copropietario
from app.models.distribucion_pago import DistribucionPago
from app.services.payment_distributor import PaymentDistributor

router = APIRouter()


@router.get("/reportes/dashboard")
def dashboard_general(
    anio: int = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Dashboard general con indicadores clave
    """
    if anio is None:
        anio = datetime.now().year
    
    # Total propiedades
    total_propiedades = db.query(Propiedad).filter(
        Propiedad.empresa_id == current_user.empresa_id,
        Propiedad.deleted_at == None
    ).count()
    
    # Ingresos del año
    ingresos_anio = db.query(func.sum(Pago.monto_pagado)).join(Contrato).join(Propiedad).filter(
        Propiedad.empresa_id == current_user.empresa_id,
        Pago.anio == anio,
        Pago.estado.in_([EstadoPago.PAGADO, EstadoPago.PARCIAL])
    ).scalar() or 0
    
    # Mora acumulada
    mora_total = db.query(func.sum(Pago.mora_calculada)).join(Contrato).join(Propiedad).filter(
        Propiedad.empresa_id == current_user.empresa_id,
        Pago.estado.in_([EstadoPago.VENCIDO, EstadoPago.PARCIAL])
    ).scalar() or 0
    
    # Pagos pendientes
    pagos_pendientes = db.query(func.count(Pago.id)).join(Contrato).join(Propiedad).filter(
        Propiedad.empresa_id == current_user.empresa_id,
        Pago.estado.in_([EstadoPago.PENDIENTE, EstadoPago.VENCIDO])
    ).scalar() or 0
    
    # Ingresos por mes
    ingresos_mensuales = db.query(
        Pago.mes,
        func.sum(Pago.monto_pagado).label('total')
    ).join(Contrato).join(Propiedad).filter(
        Propiedad.empresa_id == current_user.empresa_id,
        Pago.anio == anio,
        Pago.estado.in_([EstadoPago.PAGADO, EstadoPago.PARCIAL])
    ).group_by(Pago.mes).all()
    
    ingresos_por_mes = {mes: 0 for mes in range(1, 13)}
    for mes, total in ingresos_mensuales:
        ingresos_por_mes[mes] = float(total)
    
    return {
        "anio": anio,
        "resumen": {
            "total_propiedades": total_propiedades,
            "ingresos_anio": round(float(ingresos_anio), 2),
            "mora_acumulada": round(float(mora_total), 2),
            "pagos_pendientes": pagos_pendientes
        },
        "ingresos_mensuales": ingresos_por_mes
    }


@router.get("/reportes/copropietarios/{copropietario_id}")
def reporte_copropietario(
    copropietario_id: int,
    anio: int = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Reporte de ingresos de un copropietario específico
    """
    try:
        reporte = PaymentDistributor.obtener_reporte_copropietario(
            db=db,
            copropietario_id=copropietario_id,
            anio=anio
        )
        return reporte
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/reportes/morosidad")
def reporte_morosidad(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Reporte de morosidad por contrato
    """
    contratos_mora = db.query(
        Contrato.id,
        Contrato.numero_contrato,
        Propiedad.direccion,
        func.sum(Pago.mora_calculada).label('mora_total'),
        func.sum(Pago.monto_esperado - Pago.monto_pagado).label('monto_pendiente'),
        func.count(Pago.id).label('pagos_atrasados')
    ).join(Propiedad).join(Pago).filter(
        Propiedad.empresa_id == current_user.empresa_id,
        Pago.estado.in_([EstadoPago.VENCIDO, EstadoPago.PARCIAL, EstadoPago.PENDIENTE]),
        Pago.dias_atraso > 0
    ).group_by(
        Contrato.id,
        Contrato.numero_contrato,
        Propiedad.direccion
    ).all()
    
    resultados = []
    for item in contratos_mora:
        resultados.append({
            "contrato_id": item[0],
            "numero_contrato": item[1],
            "propiedad": item[2],
            "mora_total": round(float(item[3] or 0), 2),
            "monto_pendiente": round(float(item[4] or 0), 2),
            "pagos_atrasados": item[5]
        })
    
    # Ordenar por mora total descendente
    resultados.sort(key=lambda x: x['mora_total'], reverse=True)
    
    return {
        "total_contratos_mora": len(resultados),
        "mora_total_sistema": sum(r['mora_total'] for r in resultados),
        "contratos": resultados
    }


@router.get("/reportes/rendimiento-propiedades")
def rendimiento_propiedades(
    anio: int = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Rendimiento financiero por propiedad
    """
    if anio is None:
        anio = datetime.now().year
    
    propiedades = db.query(Propiedad).filter(
        Propiedad.empresa_id == current_user.empresa_id,
        Propiedad.deleted_at == None
    ).all()
    
    resultados = []
    
    for prop in propiedades:
        # Ingresos de la propiedad
        ingresos = db.query(func.sum(Pago.monto_pagado)).join(Contrato).filter(
            Contrato.propiedad_id == prop.id,
            Pago.anio == anio,
            Pago.estado.in_([EstadoPago.PAGADO, EstadoPago.PARCIAL])
        ).scalar() or 0
        
        # Mora pendiente
        mora = db.query(func.sum(Pago.mora_calculada)).join(Contrato).filter(
            Contrato.propiedad_id == prop.id,
            Pago.estado.in_([EstadoPago.VENCIDO, EstadoPago.PARCIAL])
        ).scalar() or 0
        
        resultados.append({
            "propiedad_id": prop.id,
            "direccion": prop.direccion,
            "tipo": prop.tipo.value,
            "canon_base": prop.canon_base,
            "ingresos_anio": round(float(ingresos), 2),
            "mora_pendiente": round(float(mora), 2),
            "ocupacion_meses": 0  # TODO: Calcular meses ocupados
        })
    
    # Ordenar por ingresos descendente
    resultados.sort(key=lambda x: x['ingresos_anio'], reverse=True)
    
    return {
        "anio": anio,
        "propiedades": resultados
    }
