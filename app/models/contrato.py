"""
Modelo de Contrato
"""
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime
from sqlalchemy import DateTime


class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relaciones
    propiedad_id = Column(Integer, ForeignKey("propiedades.id"), nullable=False)
    unidad_id = Column(Integer, ForeignKey("unidades_alquiler.id"), nullable=True)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)

    # Información del contrato
    numero_contrato = Column(String(100), unique=True, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    
    # Financiero
    canon_mensual = Column(Float, nullable=False)
    garantia = Column(Float, nullable=False)
    dia_pago = Column(Integer, nullable=False)
    
    # Incrementos y mora
    incremento_anual = Column(Float, default=0.0)
    tasa_mora_diaria = Column(Float, default=0.5)
    
    # Estado
    estado = Column(String(50), default="activo")
    
    # Observaciones
    observaciones = Column(Text, nullable=True)

    # Relaciones
    propiedad = relationship("Propiedad", back_populates="contratos")
    unidad_alquiler = relationship("UnidadAlquiler", back_populates="contratos")
    inquilino = relationship("Inquilino", back_populates="contratos")
    pagos = relationship("Pago", back_populates="contrato")