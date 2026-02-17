"""
Modelos para Unidades de Alquiler y Gastos de Propiedades
"""
from sqlalchemy import Column, Integer, Float, ForeignKey, Date, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime
import enum


class TipoUnidad(str, enum.Enum):
    """Tipos de unidades alquilables"""
    TIENDA = "tienda"
    DEPARTAMENTO = "departamento"
    OFICINA = "oficina"
    CONSULTORIO = "consultorio"
    DEPOSITO = "deposito"
    ESTACIONAMIENTO = "estacionamiento"
    LOCAL_COMERCIAL = "local_comercial"
    OTRO = "otro"


class EstadoUnidad(str, enum.Enum):
    """Estado de disponibilidad de la unidad"""
    DISPONIBLE = "disponible"
    OCUPADO = "ocupado"
    MANTENIMIENTO = "mantenimiento"
    RESERVADO = "reservado"


class TipoGasto(str, enum.Enum):
    """Tipos de gastos de propiedades"""
    IMPUESTO_ANUAL = "impuesto_anual"
    MANTENIMIENTO = "mantenimiento"
    PINTURA = "pintura"
    REFACCION = "refaccion"
    MEJORA = "mejora"
    REPARACION = "reparacion"
    SERVICIOS = "servicios"
    SEGUROS = "seguros"
    ADMINISTRATIVO = "administrativo"
    LEGAL = "legal"
    OTRO = "otro"


class UnidadAlquiler(Base):
    """
    Unidad alquilable dentro de una propiedad.
    
    Una propiedad puede tener múltiples unidades:
    - Casa AAA → 5 tiendas + 2 departamentos
    - Edificio BBB → 10 oficinas + 20 estacionamientos
    """
    __tablename__ = "unidades_alquiler"

    id         = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relación con propiedad
    propiedad_id = Column(Integer, ForeignKey("propiedades.id"), nullable=False)

    # Identificación de la unidad
    numero_unidad  = Column(String(50), nullable=False)  # "Tienda 1", "Depto A-301"
    nombre         = Column(String(200), nullable=True)   # Nombre descriptivo opcional
    tipo           = Column(String(30), nullable=False)   # tienda, departamento, etc.

    # Características físicas
    superficie     = Column(Float, nullable=True)         # Metros cuadrados
    piso           = Column(String(20), nullable=True)    # PB, 1, 2, etc.
    dormitorios    = Column(Integer, nullable=True)       # Si aplica
    banos          = Column(Integer, nullable=True)       # Si aplica
    
    # Descripción
    descripcion    = Column(String(500), nullable=True)
    
    # Canon específico de esta unidad
    canon_base     = Column(Float, nullable=False)        # Puede ser diferente al de la propiedad
    moneda         = Column(String(10), default="BOB")
    
    # Estado
    estado         = Column(String(20), default="disponible")  # disponible, ocupado, mantenimiento
    
    # Observaciones
    observaciones  = Column(String(500), nullable=True)

    # Relaciones
    propiedad = relationship("Propiedad", back_populates="unidades")
    contratos = relationship("Contrato", back_populates="unidad_alquiler")


class GastoPropiedad(Base):
    """
    Gastos asociados a una propiedad o unidad.
    
    Ejemplos:
    - Impuesto anual a la propiedad
    - Pintura general del edificio
    - Reparación de techo
    - Mejoras en lobby
    - Seguros
    """
    __tablename__ = "gastos_propiedad"

    id         = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relación con propiedad
    propiedad_id = Column(Integer, ForeignKey("propiedades.id"), nullable=False)
    
    # Relación opcional con unidad específica
    unidad_id = Column(Integer, ForeignKey("unidades_alquiler.id"), nullable=True)

    # Tipo de gasto
    tipo_gasto = Column(String(30), nullable=False)  # impuesto_anual, mantenimiento, etc.
    categoria  = Column(String(100), nullable=True)  # Subcategoría opcional

    # Detalles del gasto
    descripcion = Column(String(500), nullable=False)
    monto       = Column(Float, nullable=False)
    moneda      = Column(String(10), default="BOB")
    fecha_gasto = Column(Date, nullable=False)
    
    # Información adicional
    proveedor      = Column(String(200), nullable=True)   # Empresa que hizo el trabajo
    numero_factura = Column(String(100), nullable=True)   # Número de factura
    comprobante    = Column(String(200), nullable=True)   # Path al archivo escaneado
    
    # Periodo (para gastos recurrentes como impuestos anuales)
    periodo = Column(String(20), nullable=True)  # "2026", "2026-Q1", etc.
    
    # Notas
    observaciones = Column(String(500), nullable=True)

    # Relaciones
    propiedad = relationship("Propiedad", back_populates="gastos")
    unidad    = relationship("UnidadAlquiler", backref="gastos")
