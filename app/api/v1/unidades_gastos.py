"""
API Router para Unidades de Alquiler y Gastos de Propiedades
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

from app.core.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/unidades-gastos", tags=["Unidades y Gastos"])


# ── SCHEMAS ──────────────────────────────────────────────────────────────────

class CrearUnidadRequest(BaseModel):
    propiedad_id: int
    numero_unidad: str = Field(..., description="Ej: 'Tienda 1', 'Depto A-301'")
    nombre: Optional[str] = None
    tipo: str = Field(..., description="tienda, departamento, oficina, etc.")
    superficie: Optional[float] = None
    piso: Optional[str] = None
    dormitorios: Optional[int] = None
    banos: Optional[int] = None
    descripcion: Optional[str] = None
    canon_base: float
    moneda: str = "BOB"
    observaciones: Optional[str] = None


class ActualizarEstadoUnidadRequest(BaseModel):
    estado: str = Field(..., description="disponible, ocupado, mantenimiento, reservado")


class CrearGastoRequest(BaseModel):
    propiedad_id: int
    unidad_id: Optional[int] = None
    tipo_gasto: str = Field(..., description="impuesto_anual, mantenimiento, pintura, etc.")
    categoria: Optional[str] = None
    descripcion: str
    monto: float
    moneda: str = "BOB"
    fecha_gasto: date
    proveedor: Optional[str] = None
    numero_factura: Optional[str] = None
    periodo: Optional[str] = None
    observaciones: Optional[str] = None


# ── ENDPOINTS: UNIDADES ──────────────────────────────────────────────────────

@router.post("/unidades", summary="Crear unidad de alquiler")
def crear_unidad(
    req: CrearUnidadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crea una nueva unidad alquilable dentro de una propiedad.
    
    Ejemplo: Casa AAA tiene 5 tiendas + 2 departamentos
    """
    from app.models.unidad_gasto import UnidadAlquiler
    from app.models.propiedad import Propiedad
    
    # Verificar que la propiedad existe
    propiedad = db.query(Propiedad).filter(
        Propiedad.id == req.propiedad_id,
        Propiedad.deleted_at == None
    ).first()
    
    if not propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    
    unidad = UnidadAlquiler(
        propiedad_id=req.propiedad_id,
        numero_unidad=req.numero_unidad,
        nombre=req.nombre,
        tipo=req.tipo,
        superficie=req.superficie,
        piso=req.piso,
        dormitorios=req.dormitorios,
        banos=req.banos,
        descripcion=req.descripcion,
        canon_base=req.canon_base,
        moneda=req.moneda,
        estado="disponible",
        observaciones=req.observaciones
    )
    
    db.add(unidad)
    db.commit()
    db.refresh(unidad)
    
    return {
        "id": unidad.id,
        "mensaje": f"Unidad '{req.numero_unidad}' creada exitosamente",
        "unidad": {
            "id": unidad.id,
            "propiedad_id": unidad.propiedad_id,
            "numero_unidad": unidad.numero_unidad,
            "tipo": unidad.tipo,
            "canon_base": unidad.canon_base,
            "estado": unidad.estado
        }
    }


@router.get("/unidades/propiedad/{propiedad_id}", summary="Listar unidades de una propiedad")
def listar_unidades_propiedad(
    propiedad_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todas las unidades de una propiedad específica.
    """
    from app.models.unidad_gasto import UnidadAlquiler
    
    unidades = db.query(UnidadAlquiler).filter(
        UnidadAlquiler.propiedad_id == propiedad_id,
        UnidadAlquiler.deleted_at == None
    ).all()
    
    return {
        "propiedad_id": propiedad_id,
        "total_unidades": len(unidades),
        "unidades": [
            {
                "id": u.id,
                "numero_unidad": u.numero_unidad,
                "nombre": u.nombre,
                "tipo": u.tipo,
                "superficie": u.superficie,
                "piso": u.piso,
                "canon_base": u.canon_base,
                "estado": u.estado,
                "dormitorios": u.dormitorios,
                "banos": u.banos
            }
            for u in unidades
        ],
        "resumen_por_tipo": _resumen_por_tipo(unidades),
        "resumen_por_estado": _resumen_por_estado(unidades)
    }


@router.patch("/unidades/{unidad_id}/estado", summary="Cambiar estado de unidad")
def cambiar_estado_unidad(
    unidad_id: int,
    req: ActualizarEstadoUnidadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cambia el estado de una unidad: disponible, ocupado, mantenimiento, reservado
    """
    from app.models.unidad_gasto import UnidadAlquiler
    
    unidad = db.query(UnidadAlquiler).filter(
        UnidadAlquiler.id == unidad_id,
        UnidadAlquiler.deleted_at == None
    ).first()
    
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    
    unidad.estado = req.estado
    db.commit()
    
    return {
        "id": unidad.id,
        "numero_unidad": unidad.numero_unidad,
        "estado_anterior": unidad.estado,
        "estado_nuevo": req.estado
    }


# ── ENDPOINTS: GASTOS ────────────────────────────────────────────────────────

@router.post("/gastos", summary="Registrar gasto de propiedad")
def crear_gasto(
    req: CrearGastoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Registra un gasto asociado a una propiedad o unidad específica.
    
    Ejemplos:
    - Impuesto anual a la propiedad
    - Pintura del edificio
    - Reparación de techo
    - Mejora en lobby
    """
    from app.models.unidad_gasto import GastoPropiedad
    from app.models.propiedad import Propiedad
    
    # Verificar que la propiedad existe
    propiedad = db.query(Propiedad).filter(
        Propiedad.id == req.propiedad_id,
        Propiedad.deleted_at == None
    ).first()
    
    if not propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    
    gasto = GastoPropiedad(
        propiedad_id=req.propiedad_id,
        unidad_id=req.unidad_id,
        tipo_gasto=req.tipo_gasto,
        categoria=req.categoria,
        descripcion=req.descripcion,
        monto=req.monto,
        moneda=req.moneda,
        fecha_gasto=req.fecha_gasto,
        proveedor=req.proveedor,
        numero_factura=req.numero_factura,
        periodo=req.periodo,
        observaciones=req.observaciones
    )
    
    db.add(gasto)
    db.commit()
    db.refresh(gasto)
    
    return {
        "id": gasto.id,
        "mensaje": "Gasto registrado exitosamente",
        "gasto": {
            "id": gasto.id,
            "tipo_gasto": gasto.tipo_gasto,
            "descripcion": gasto.descripcion,
            "monto": gasto.monto,
            "fecha": str(gasto.fecha_gasto)
        }
    }


@router.get("/gastos/propiedad/{propiedad_id}", summary="Listar gastos de una propiedad")
def listar_gastos_propiedad(
    propiedad_id: int,
    anio: Optional[int] = None,
    tipo_gasto: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todos los gastos de una propiedad.
    Opcionalmente filtrar por año y/o tipo de gasto.
    """
    from app.models.unidad_gasto import GastoPropiedad
    
    query = db.query(GastoPropiedad).filter(
        GastoPropiedad.propiedad_id == propiedad_id,
        GastoPropiedad.deleted_at == None
    )
    
    if anio:
        from sqlalchemy import extract
        query = query.filter(extract('year', GastoPropiedad.fecha_gasto) == anio)
    
    if tipo_gasto:
        query = query.filter(GastoPropiedad.tipo_gasto == tipo_gasto)
    
    gastos = query.order_by(GastoPropiedad.fecha_gasto.desc()).all()
    
    total_gastos = sum(g.monto for g in gastos)
    
    return {
        "propiedad_id": propiedad_id,
        "filtros": {"anio": anio, "tipo_gasto": tipo_gasto},
        "total_gastos": len(gastos),
        "monto_total": round(total_gastos, 2),
        "gastos": [
            {
                "id": g.id,
                "tipo_gasto": g.tipo_gasto,
                "descripcion": g.descripcion,
                "monto": g.monto,
                "fecha": str(g.fecha_gasto),
                "proveedor": g.proveedor,
                "numero_factura": g.numero_factura,
                "periodo": g.periodo
            }
            for g in gastos
        ],
        "resumen_por_tipo": _resumen_gastos_por_tipo(gastos)
    }


@router.get("/gastos/resumen/{propiedad_id}/{anio}", summary="Resumen anual de gastos")
def resumen_gastos_anual(
    propiedad_id: int,
    anio: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Resumen de gastos anuales de una propiedad, agrupado por tipo.
    """
    from app.models.unidad_gasto import GastoPropiedad
    from sqlalchemy import extract
    
    gastos = db.query(GastoPropiedad).filter(
        GastoPropiedad.propiedad_id == propiedad_id,
        extract('year', GastoPropiedad.fecha_gasto) == anio,
        GastoPropiedad.deleted_at == None
    ).all()
    
    total = sum(g.monto for g in gastos)
    
    # Agrupar por tipo
    por_tipo = {}
    for g in gastos:
        tipo = g.tipo_gasto
        if tipo not in por_tipo:
            por_tipo[tipo] = {"cantidad": 0, "monto_total": 0, "gastos": []}
        por_tipo[tipo]["cantidad"] += 1
        por_tipo[tipo]["monto_total"] += g.monto
        por_tipo[tipo]["gastos"].append({
            "descripcion": g.descripcion,
            "monto": g.monto,
            "fecha": str(g.fecha_gasto)
        })
    
    return {
        "propiedad_id": propiedad_id,
        "anio": anio,
        "total_gastos": len(gastos),
        "monto_total": round(total, 2),
        "por_tipo": {
            tipo: {
                "cantidad": data["cantidad"],
                "monto_total": round(data["monto_total"], 2),
                "promedio": round(data["monto_total"] / data["cantidad"], 2),
                "gastos": data["gastos"]
            }
            for tipo, data in por_tipo.items()
        }
    }


# ── FUNCIONES AUXILIARES ─────────────────────────────────────────────────────

def _resumen_por_tipo(unidades):
    """Cuenta unidades por tipo"""
    resumen = {}
    for u in unidades:
        tipo = u.tipo
        if tipo not in resumen:
            resumen[tipo] = 0
        resumen[tipo] += 1
    return resumen


def _resumen_por_estado(unidades):
    """Cuenta unidades por estado"""
    resumen = {}
    for u in unidades:
        estado = u.estado
        if estado not in resumen:
            resumen[estado] = 0
        resumen[estado] += 1
    return resumen


def _resumen_gastos_por_tipo(gastos):
    """Agrupa gastos por tipo y suma montos"""
    resumen = {}
    for g in gastos:
        tipo = g.tipo_gasto
        if tipo not in resumen:
            resumen[tipo] = {"cantidad": 0, "monto_total": 0}
        resumen[tipo]["cantidad"] += 1
        resumen[tipo]["monto_total"] += g.monto
    
    for tipo in resumen:
        resumen[tipo]["monto_total"] = round(resumen[tipo]["monto_total"], 2)
    
    return resumen
