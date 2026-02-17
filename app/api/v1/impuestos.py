"""
API de Impuestos Bolivianos
Endpoints para calcular, registrar y consultar impuestos
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.services.tax_calculator import calcular_impuestos, calcular_solo_determinado

router = APIRouter(prefix="/impuestos", tags=["Impuestos"])


# ── SCHEMAS ──────────────────────────────────────────────────────────────────

class CalcularRequest(BaseModel):
    monto_alquiler: float = Field(..., description="Canon mensual en Bs.", example=3000)
    mes: int             = Field(..., ge=1, le=12, description="Mes (1-12)", example=2)
    anio: int            = Field(..., description="Año", example=2026)
    facturas_iva: float  = Field(0.0, description="Total facturas para compensar IVA", example=300)
    facturas_rc_iva: float = Field(0.0, description="Total facturas para compensar RC-IVA", example=0)
    monto_acumulado_trimestre: Optional[float] = Field(
        None,
        description="Suma alquileres del trimestre. Si no se pasa, se estima × 3",
        example=9000
    )

class RegistrarImpuestoRequest(BaseModel):
    pago_id: int
    contrato_id: int
    monto_alquiler: float
    mes: int
    anio: int
    facturas_iva: float = 0.0
    facturas_rc_iva: float = 0.0
    monto_acumulado_trimestre: Optional[float] = None
    observaciones: Optional[str] = None
    fecha_declaracion: Optional[date] = None

class RegistrarFacturaRequest(BaseModel):
    contrato_id: int
    numero_factura: str
    nit_emisor: Optional[str] = None
    nombre_emisor: Optional[str] = None
    fecha_factura: date
    monto_factura: float
    tipo_impuesto: str  # "iva" o "rc_iva"
    periodo: str        # "2026-03"
    anio: int
    mes: Optional[int] = None
    trimestre: Optional[int] = None
    descripcion: Optional[str] = None


# ── ENDPOINTS ────────────────────────────────────────────────────────────────

@router.post("/calcular", summary="Calcular impuestos (sin guardar)")
def calcular(
    req: CalcularRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Calcula los impuestos bolivianos mostrando SIEMPRE:
    - Impuesto DETERMINADO (lo que exige la ley)
    - Impuesto EFECTIVO (lo que realmente pagas con facturas)
    - Ahorro con facturas
    - Neto a distribuir entre copropietarios

    NO guarda en base de datos. Útil para previsualizar.
    """
    return calcular_impuestos(
        monto_alquiler=req.monto_alquiler,
        mes=req.mes,
        anio=req.anio,
        facturas_iva=req.facturas_iva,
        facturas_rc_iva=req.facturas_rc_iva,
        monto_acumulado_trimestre=req.monto_acumulado_trimestre,
    )


@router.post("/calcular/sin-facturas", summary="Ver impuesto determinado puro (sin compensación)")
def calcular_sin_facturas(
    req: CalcularRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Muestra el peor escenario: sin ninguna factura de compensación.
    Útil para saber el máximo que podrías pagar.
    """
    return calcular_solo_determinado(
        monto_alquiler=req.monto_alquiler,
        mes=req.mes,
        anio=req.anio,
    )


@router.post("/registrar", summary="Registrar impuesto en base de datos")
def registrar_impuesto(
    req: RegistrarImpuestoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Calcula Y guarda el registro de impuestos en la base de datos.
    Se llama después de registrar el pago del alquiler.
    """
    from app.models.impuesto import ImpuestoAlquiler, EstadoImpuesto
    from app.services.tax_calculator import get_trimestre, MESES_TRIMESTRALES

    calculo = calcular_impuestos(
        monto_alquiler=req.monto_alquiler,
        mes=req.mes,
        anio=req.anio,
        facturas_iva=req.facturas_iva,
        facturas_rc_iva=req.facturas_rc_iva,
        monto_acumulado_trimestre=req.monto_acumulado_trimestre,
    )

    impuesto = ImpuestoAlquiler(
        pago_id     = req.pago_id,
        contrato_id = req.contrato_id,
        periodo     = calculo["periodo"],
        anio        = req.anio,
        mes         = req.mes,
        trimestre   = calculo["trimestre"],
        monto_alquiler = req.monto_alquiler,

        # IVA
        iva_alicuota             = calculo["iva"]["alicuota"],
        iva_pct_max_compensacion = calculo["iva"]["pct_max_compensacion"],
        iva_determinado          = calculo["iva"]["determinado"],
        iva_limite_compensacion  = calculo["iva"]["limite_compensacion"],
        iva_facturas_presentadas = calculo["iva"]["facturas_presentadas"],
        iva_facturas_aplicadas   = calculo["iva"]["facturas_aplicadas"],
        iva_efectivo             = calculo["iva"]["efectivo"],

        # IT
        it_alicuota    = calculo["it"]["alicuota"],
        it_determinado = calculo["it"]["determinado"],
        it_efectivo    = calculo["it"]["efectivo"],

        # RC-IVA
        rc_iva_alicuota              = calculo["rc_iva"]["alicuota"],
        rc_iva_pct_max_compensacion  = calculo["rc_iva"]["pct_max_compensacion"],
        rc_iva_base_trimestral       = calculo["rc_iva"]["base_trimestral"],
        rc_iva_determinado           = calculo["rc_iva"]["determinado"],
        rc_iva_facturas_presentadas  = calculo["rc_iva"]["facturas_presentadas"],
        rc_iva_facturas_aplicadas    = calculo["rc_iva"]["facturas_aplicadas"],
        rc_iva_efectivo              = calculo["rc_iva"]["efectivo"],
        es_mes_trimestral            = calculo["es_mes_trimestral"],

        # Totales
        total_determinado        = calculo["resumen"]["total_determinado"],
        total_facturas_aplicadas = calculo["resumen"]["total_facturas_aplicadas"],
        total_efectivo           = calculo["resumen"]["total_efectivo"],
        total_ahorro             = calculo["resumen"]["total_ahorro_con_facturas"],
        monto_neto_distribuir    = calculo["resumen"]["monto_neto_distribuir"],

        observaciones    = req.observaciones,
        fecha_declaracion= req.fecha_declaracion,
    )

    db.add(impuesto)
    db.commit()
    db.refresh(impuesto)

    return {
        "id": impuesto.id,
        "mensaje": "Impuesto registrado exitosamente",
        "calculo": calculo,
    }


@router.get("/contrato/{contrato_id}/anio/{anio}",
            summary="Resumen anual de impuestos de un contrato")
def resumen_anual(
    contrato_id: int,
    anio: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Muestra mes a mes para un contrato:
    - Impuesto determinado vs efectivamente pagado
    - Ahorro acumulado con facturas
    - Totales anuales
    """
    from app.models.impuesto import ImpuestoAlquiler

    registros = db.query(ImpuestoAlquiler).filter(
        ImpuestoAlquiler.contrato_id == contrato_id,
        ImpuestoAlquiler.anio == anio,
        ImpuestoAlquiler.deleted_at == None
    ).order_by(ImpuestoAlquiler.mes).all()

    if not registros:
        return {
            "contrato_id": contrato_id,
            "anio": anio,
            "mensaje": "Sin registros de impuestos para este año",
            "registros": [],
            "totales": {}
        }

    detalle = []
    for r in registros:
        detalle.append({
            "mes": r.mes,
            "periodo": r.periodo,
            "es_trimestral": r.es_mes_trimestral,
            "monto_alquiler": r.monto_alquiler,

            "iva": {
                "alicuota": r.iva_alicuota,
                "pct_max_compensacion": r.iva_pct_max_compensacion,
                "determinado": r.iva_determinado,
                "limite_compensacion": r.iva_limite_compensacion,
                "facturas_presentadas": r.iva_facturas_presentadas,
                "facturas_aplicadas": r.iva_facturas_aplicadas,
                "efectivo": r.iva_efectivo,
                "ahorro": r.iva_facturas_aplicadas,
            },
            "it": {
                "alicuota": r.it_alicuota,
                "determinado": r.it_determinado,
                "efectivo": r.it_efectivo,
                "compensable": False,
            },
            "rc_iva": {
                "alicuota": r.rc_iva_alicuota,
                "aplico": r.es_mes_trimestral,
                "base_trimestral": r.rc_iva_base_trimestral,
                "determinado": r.rc_iva_determinado,
                "facturas_presentadas": r.rc_iva_facturas_presentadas,
                "facturas_aplicadas": r.rc_iva_facturas_aplicadas,
                "efectivo": r.rc_iva_efectivo,
                "ahorro": r.rc_iva_facturas_aplicadas,
            },
            "totales_mes": {
                "determinado": r.total_determinado,
                "facturas_aplicadas": r.total_facturas_aplicadas,
                "efectivo": r.total_efectivo,
                "ahorro": r.total_ahorro,
                "neto_distribuido": r.monto_neto_distribuir,
            },
        })

    # Totales anuales
    sum_det   = round(sum(r.total_determinado for r in registros), 2)
    sum_efect = round(sum(r.total_efectivo for r in registros), 2)
    sum_ahorro= round(sum(r.total_ahorro for r in registros), 2)
    sum_neto  = round(sum(r.monto_neto_distribuir for r in registros), 2)
    sum_iva_d = round(sum(r.iva_determinado for r in registros), 2)
    sum_iva_e = round(sum(r.iva_efectivo for r in registros), 2)
    sum_it    = round(sum(r.it_monto for r in registros), 2)
    sum_rciva_d = round(sum(r.rc_iva_determinado for r in registros), 2)
    sum_rciva_e = round(sum(r.rc_iva_efectivo for r in registros), 2)

    return {
        "contrato_id": contrato_id,
        "anio": anio,
        "total_meses_registrados": len(registros),
        "registros": detalle,
        "totales_anuales": {
            "iva": {
                "determinado": sum_iva_d,
                "efectivo": sum_iva_e,
                "ahorro_facturas": round(sum_iva_d - sum_iva_e, 2),
            },
            "it": {
                "determinado": sum_it,
                "efectivo": sum_it,
                "ahorro_facturas": 0.0,
                "nota": "No compensable"
            },
            "rc_iva": {
                "determinado": sum_rciva_d,
                "efectivo": sum_rciva_e,
                "ahorro_facturas": round(sum_rciva_d - sum_rciva_e, 2),
            },
            "total": {
                "determinado": sum_det,
                "efectivo": sum_efect,
                "ahorro_total_facturas": sum_ahorro,
                "neto_distribuido_copropietarios": sum_neto,
            }
        }
    }
