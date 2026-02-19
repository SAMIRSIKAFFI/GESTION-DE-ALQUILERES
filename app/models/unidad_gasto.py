"""
Modelos para Unidades de Alquiler y Gastos de Propiedades
"""
from sqlalchemy import Column, Integer, Float, ForeignKey, Date, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime


class UnidadAlquiler(Base):
    """Unidad alquilable dentro de una propiedad"""
    __tablename__ = "unidades_alquiler"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    propiedad_id = Column(Integer, ForeignKey("propiedades.id"), nullable=False)
    numero_unidad = Column(String(50), nullable=False)
    nombre = Column(String(200), nullable=True)
    tipo = Column(String(30), nullable=False)
    superficie = Column(Float, nullable=True)
    piso = Column(String(20), nullable=True)
    dormitorios = Column(Integer, nullable=True)
    banos = Column(Integer, nullable=True)
    descripcion = Column(String(500), nullable=True)
    canon_base = Column(Float, nullable=False)
    moneda = Column(String(10), default="BOB")
    estado = Column(String(20), default="disponible")
    observaciones = Column(String(500), nullable=True)

    propiedad = relationship("Propiedad", back_populates="unidades")
    contratos = relationship("Contrato", back_populates="unidad_alquiler")


class GastoPropiedad(Base):
    """Gastos asociados a una propiedad"""
    __tablename__ = "gastos_propiedad"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    propiedad_id = Column(Integer, ForeignKey("propiedades.id"), nullable=False)
    unidad_id = Column(Integer, ForeignKey("unidades_alquiler.id"), nullable=True)
    tipo_gasto = Column(String(30), nullable=False)
    categoria = Column(String(100), nullable=True)
    descripcion = Column(String(500), nullable=False)
    monto = Column(Float, nullable=False)
    moneda = Column(String(10), default="BOB")
    fecha_gasto = Column(Date, nullable=False)
    proveedor = Column(String(200), nullable=True)
    numero_factura = Column(String(100), nullable=True)
    comprobante = Column(String(200), nullable=True)
    periodo = Column(String(20), nullable=True)
    observaciones = Column(String(500), nullable=True)

    propiedad = relationship("Propiedad", back_populates="gastos")
    unidad = relationship("UnidadAlquiler", backref="gastos")