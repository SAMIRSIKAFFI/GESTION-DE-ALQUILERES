from sqlalchemy import Column, Integer, Float, ForeignKey, Date, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime
import enum


class EstadoImpuesto(str, enum.Enum):
    PENDIENTE  = "pendiente"
    PAGADO     = "pagado"
    COMPENSADO = "compensado"
    PARCIAL    = "parcial"


class TipoImpuesto(str, enum.Enum):
    IVA    = "iva"
    IT     = "it"
    RC_IVA = "rc_iva"


class ImpuestoAlquiler(Base):
    __tablename__ = "impuestos_alquiler"

    id         = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    pago_id     = Column(Integer, ForeignKey("pagos.id"),     nullable=False)
    contrato_id = Column(Integer, ForeignKey("contratos.id"), nullable=False)

    periodo   = Column(String(7),  nullable=False)
    anio      = Column(Integer,    nullable=False)
    mes       = Column(Integer,    nullable=False)
    trimestre = Column(Integer,    nullable=True)

    monto_alquiler = Column(Float, nullable=False)

    # IVA 13% - compensable hasta 30% del alquiler
    iva_alicuota             = Column(Float, default=13.0)
    iva_pct_max_compensacion = Column(Float, default=30.0)
    iva_determinado          = Column(Float, default=0.0)
    iva_limite_compensacion  = Column(Float, default=0.0)
    iva_facturas_presentadas = Column(Float, default=0.0)
    iva_facturas_aplicadas   = Column(Float, default=0.0)
    iva_efectivo             = Column(Float, default=0.0)
    iva_estado               = Column(String(20), default="pendiente")

    # IT 3% - NO compensable
    it_alicuota    = Column(Float, default=3.0)
    it_determinado = Column(Float, default=0.0)
    it_efectivo    = Column(Float, default=0.0)

    # RC-IVA 12.5% trimestral - compensable al 100%
    rc_iva_alicuota             = Column(Float, default=12.5)
    rc_iva_pct_max_compensacion = Column(Float, default=100.0)
    rc_iva_base_trimestral      = Column(Float, default=0.0)
    rc_iva_determinado          = Column(Float, default=0.0)
    rc_iva_facturas_presentadas = Column(Float, default=0.0)
    rc_iva_facturas_aplicadas   = Column(Float, default=0.0)
    rc_iva_efectivo             = Column(Float, default=0.0)
    rc_iva_estado               = Column(String(20), default="pendiente")
    es_mes_trimestral           = Column(Boolean, default=False)

    # Totales
    total_determinado        = Column(Float, default=0.0)
    total_facturas_aplicadas = Column(Float, default=0.0)
    total_efectivo           = Column(Float, default=0.0)
    total_ahorro             = Column(Float, default=0.0)
    monto_neto_distribuir    = Column(Float, default=0.0)

    observaciones     = Column(String(500), nullable=True)
    fecha_declaracion = Column(Date,        nullable=True)


class FacturaCompensacion(Base):
    __tablename__ = "facturas_compensacion"

    id         = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    contrato_id = Column(Integer, ForeignKey("contratos.id"),          nullable=False)
    impuesto_id = Column(Integer, ForeignKey("impuestos_alquiler.id"), nullable=True)

    numero_factura = Column(String(50),  nullable=False)
    nit_emisor     = Column(String(20),  nullable=True)
    nombre_emisor  = Column(String(200), nullable=True)
    fecha_factura  = Column(Date,        nullable=False)
    monto_factura  = Column(Float,       nullable=False)

    tipo_impuesto = Column(String(10), nullable=False)
    periodo       = Column(String(7),  nullable=False)
    anio          = Column(Integer,    nullable=False)
    mes           = Column(Integer,    nullable=True)
    trimestre     = Column(Integer,    nullable=True)
    descripcion   = Column(String(300), nullable=True)
    utilizada     = Column(Boolean,     default=False)