from sqlalchemy import Column, Integer, String, Float, Text
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
    
    # Tipo: "propia" o "copropiedad" (STRING, no ENUM)
    tipo = Column(String(50), nullable=False, default="propia")
    
    # Detalles físicos
    superficie = Column(Float, nullable=True)
    dormitorios = Column(Integer, nullable=True)
    banos = Column(Integer, nullable=True)
    
    # Financiero
    canon_base = Column(Float, nullable=False)
    moneda = Column(String(10), default="BOB")
    
    # Descripción
    descripcion = Column(Text, nullable=True)
    
    # Estado: "disponible", "ocupado", etc (STRING, no ENUM)
    estado = Column(String(50), default="disponible")

    # Relaciones
    copropietarios = relationship("Copropietario", back_populates="propiedad", cascade="all, delete-orphan")
    contratos = relationship("Contrato", back_populates="propiedad")
    unidades = relationship("UnidadAlquiler", back_populates="propiedad")
    gastos = relationship("GastoPropiedad", back_populates="propiedad")