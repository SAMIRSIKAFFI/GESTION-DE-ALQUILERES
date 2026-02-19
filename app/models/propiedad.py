"""
Modelo de Propiedad
"""
from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime
from sqlalchemy import DateTime


class Propiedad(Base):
    __tablename__ = "propiedades"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Información básica
    direccion = Column(String(255), nullable=False)
    ciudad = Column(String(100), nullable=False)
    zona = Column(String(100), nullable=True)
    
    # Tipo de propiedad: propia o copropiedad
    tipo = Column(String(50), nullable=False)  # "propia" o "copropiedad"
    
    # Tipo de inmueble
    tipo_inmueble = Column(String(100), nullable=True)
    
    # Detalles físicos
    superficie = Column(Float, nullable=True)
    dormitorios = Column(Integer, nullable=True)
    banos = Column(Integer, nullable=True)
    
    # Financiero
    canon_base = Column(Float, nullable=False)
    moneda = Column(String(10), default="BOB")
    
    # Descripción
    descripcion = Column(Text, nullable=True)
    
    # Estado
    estado = Column(String(50), default="disponible")
    
    # Copropiedades
    numero_copropietarios = Column(Integer, default=1)

    # Relaciones
    copropietarios = relationship("Copropietario", back_populates="propiedad", cascade="all, delete-orphan")
    contratos = relationship("Contrato", back_populates="propiedad")
    unidades = relationship("UnidadAlquiler", back_populates="propiedad")
    gastos = relationship("GastoPropiedad", back_populates="propiedad")