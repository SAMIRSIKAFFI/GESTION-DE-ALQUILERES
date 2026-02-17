"""
Calculadora de Impuestos Bolivianos para Alquileres
====================================================
Siempre calcula y devuelve DOS valores por impuesto:
  - determinado : lo que establece la ley
  - efectivo    : lo que realmente se paga

Reglas implementadas:
  IVA 13%      → compensable con facturas, límite = 30% del alquiler
  IT  3%       → NO compensable, determinado = efectivo siempre
  RC-IVA 12.5% → trimestral (Mar/Jun/Sep/Dic), compensable al 100%
"""
from typing import Dict, Any, Optional

# Meses de cierre trimestral
MESES_TRIMESTRALES = {3, 6, 9, 12}

# Alícuotas legales (porcentajes)
ALICUOTA_IVA    = 13.0
ALICUOTA_IT     =  3.0
ALICUOTA_RC_IVA = 12.5

# Límites de compensación (porcentaje del impuesto/alquiler)
LIMITE_COMP_IVA    = 30.0   # hasta 30% del ALQUILER
LIMITE_COMP_RC_IVA = 100.0  # hasta 100% del RC-IVA determinado


def get_trimestre(mes: int) -> int:
    if mes <= 3:  return 1
    if mes <= 6:  return 2
    if mes <= 9:  return 3
    return 4


def calcular_impuestos(
    monto_alquiler: float,
    mes: int,
    anio: int,
    facturas_iva: float = 0.0,
    facturas_rc_iva: float = 0.0,
    monto_acumulado_trimestre: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Calcula todos los impuestos bolivianos para un alquiler.

    Retorna para cada impuesto:
      - alicuota         → porcentaje legal
      - determinado      → monto que exige la ley
      - limite_comp      → hasta cuánto puedes compensar
      - facturas_pres    → facturas que presentaste
      - facturas_aplic   → facturas que se aplicaron efectivamente
      - efectivo         → lo que realmente pagas
      - ahorro           → determinado - efectivo
      - estado           → si compensó total, parcial o nada

    Args:
        monto_alquiler:           Canon mensual en Bs.
        mes:                      Mes del pago (1-12)
        anio:                     Año del pago
        facturas_iva:             Total facturas para compensar IVA
        facturas_rc_iva:          Total facturas para compensar RC-IVA
        monto_acumulado_trimestre: Suma de los 3 meses (para RC-IVA).
                                   Si no se pasa, se estima como alquiler × 3.
    """
    es_trimestral = mes in MESES_TRIMESTRALES
    trimestre     = get_trimestre(mes)

    # ── IVA 13% ─────────────────────────────────────────────────────────────
    iva_determinado         = round(monto_alquiler * ALICUOTA_IVA / 100, 2)
    iva_limite_compensacion = round(monto_alquiler * LIMITE_COMP_IVA / 100, 2)
    iva_facturas_aplicadas  = round(min(facturas_iva, iva_limite_compensacion), 2)
    iva_efectivo            = round(max(0.0, iva_determinado - iva_facturas_aplicadas), 2)
    iva_ahorro              = round(iva_facturas_aplicadas, 2)

    if iva_facturas_aplicadas == 0:
        iva_estado = "sin_compensacion"
    elif iva_efectivo == 0:
        iva_estado = "compensado_total"
    else:
        iva_estado = "compensado_parcial"

    # ── IT 3% (NO compensable) ──────────────────────────────────────────────
    it_determinado = round(monto_alquiler * ALICUOTA_IT / 100, 2)
    it_efectivo    = it_determinado   # siempre igual
    it_ahorro      = 0.0

    # ── RC-IVA 12.5% trimestral ─────────────────────────────────────────────
    rc_base          = 0.0
    rc_determinado   = 0.0
    rc_facturas_aplic= 0.0
    rc_efectivo      = 0.0
    rc_ahorro        = 0.0
    rc_estado        = "no_aplica"

    if es_trimestral:
        rc_base         = monto_acumulado_trimestre if monto_acumulado_trimestre \
                          else round(monto_alquiler * 3, 2)
        rc_determinado  = round(rc_base * ALICUOTA_RC_IVA / 100, 2)
        # Compensable al 100%: límite = el propio determinado
        rc_facturas_aplic = round(min(facturas_rc_iva, rc_determinado), 2)
        rc_efectivo     = round(max(0.0, rc_determinado - rc_facturas_aplic), 2)
        rc_ahorro       = round(rc_facturas_aplic, 2)

        if rc_facturas_aplic == 0:
            rc_estado = "sin_compensacion"
        elif rc_efectivo == 0:
            rc_estado = "compensado_total"
        else:
            rc_estado = "compensado_parcial"

    # ── TOTALES ──────────────────────────────────────────────────────────────
    total_determinado        = round(iva_determinado + it_determinado + rc_determinado, 2)
    total_facturas_aplicadas = round(iva_facturas_aplicadas + rc_facturas_aplic, 2)
    total_efectivo           = round(iva_efectivo + it_efectivo + rc_efectivo, 2)
    total_ahorro             = round(total_determinado - total_efectivo, 2)

    # ── NETO PARA DISTRIBUIR ─────────────────────────────────────────────────
    monto_neto = round(max(0.0, monto_alquiler - total_efectivo), 2)

    return {
        # Contexto
        "monto_alquiler" : monto_alquiler,
        "periodo"        : f"{anio}-{mes:02d}",
        "mes"            : mes,
        "anio"           : anio,
        "trimestre"      : trimestre,
        "es_mes_trimestral": es_trimestral,

        # ── IVA ────────────────────────────────────────────────────────────
        "iva": {
            "alicuota"           : ALICUOTA_IVA,
            "pct_max_compensacion": LIMITE_COMP_IVA,
            "determinado"        : iva_determinado,
            "limite_compensacion": iva_limite_compensacion,
            "facturas_presentadas": facturas_iva,
            "facturas_aplicadas" : iva_facturas_aplicadas,
            "efectivo"           : iva_efectivo,
            "ahorro"             : iva_ahorro,
            "estado"             : iva_estado,
            "nota"               : f"Alícuota {ALICUOTA_IVA}% | "
                                   f"Compensable hasta {LIMITE_COMP_IVA}% del alquiler "
                                   f"(Bs. {iva_limite_compensacion})",
        },

        # ── IT ─────────────────────────────────────────────────────────────
        "it": {
            "alicuota"    : ALICUOTA_IT,
            "compensable" : False,
            "determinado" : it_determinado,
            "efectivo"    : it_efectivo,
            "ahorro"      : it_ahorro,
            "estado"      : "no_compensable",
            "nota"        : f"Alícuota {ALICUOTA_IT}% | "
                            f"NO compensable. Siempre se paga Bs. {it_determinado}",
        },

        # ── RC-IVA ─────────────────────────────────────────────────────────
        "rc_iva": {
            "alicuota"            : ALICUOTA_RC_IVA,
            "pct_max_compensacion": LIMITE_COMP_RC_IVA,
            "aplica_este_mes"     : es_trimestral,
            "meses_cierre"        : "Marzo, Junio, Septiembre, Diciembre",
            "base_trimestral"     : rc_base,
            "determinado"         : rc_determinado,
            "facturas_presentadas": facturas_rc_iva if es_trimestral else 0,
            "facturas_aplicadas"  : rc_facturas_aplic,
            "efectivo"            : rc_efectivo,
            "ahorro"              : rc_ahorro,
            "estado"              : rc_estado,
            "nota"                : (
                f"Alícuota {ALICUOTA_RC_IVA}% sobre acumulado trimestral | "
                f"Compensable al {LIMITE_COMP_RC_IVA}%"
            ) if es_trimestral else
                "No aplica este mes (solo en Marzo, Junio, Sep, Dic)",
        },

        # ── RESUMEN TOTAL ──────────────────────────────────────────────────
        "resumen": {
            "total_determinado"         : total_determinado,
            "total_facturas_aplicadas"  : total_facturas_aplicadas,
            "total_efectivo"            : total_efectivo,
            "total_ahorro_con_facturas" : total_ahorro,
            "monto_neto_distribuir"     : monto_neto,
            "explicacion": (
                f"De Bs. {monto_alquiler} de alquiler: "
                f"impuesto determinado Bs. {total_determinado}, "
                f"efectivamente pagas Bs. {total_efectivo} "
                f"(ahorraste Bs. {total_ahorro} con facturas), "
                f"neto a distribuir: Bs. {monto_neto}"
            ),
        },
    }


def calcular_solo_determinado(monto_alquiler: float, mes: int, anio: int) -> Dict[str, Any]:
    """
    Calcula solo los impuestos DETERMINADOS (sin facturas).
    Útil para mostrar el escenario más conservador (sin compensación).
    """
    return calcular_impuestos(
        monto_alquiler=monto_alquiler,
        mes=mes,
        anio=anio,
        facturas_iva=0.0,
        facturas_rc_iva=0.0,
    )
