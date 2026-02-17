import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class TipoPropiedad(str, enum.Enum):
    """Tipos de propiedad"""
    PROPIA = "propia"
    COPROPIEDAD = "copropiedad"


class EstadoPropiedad(str, enum.Enum):
    """Estados de una propiedad"""
    DISPONIBLE = "disponible"
    ALQUILADO = "alquilado"
    MANTENIMIENTO = "mantenimiento"


class Propiedad(BaseModel):
    """Modelo de Propiedad Inmobiliaria"""
    
    __tablename__ = "propiedades"
    
    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    
    # Datos de ubicación
    direccion = Column(String(300), nullable=False)
    ciudad = Column(String(100), default="La Paz", nullable=False)
    departamento = Column(String(100), default="La Paz", nullable=False)
    zona = Column(String(100))
    
    # Características
    tipo = Column(Enum(TipoPropiedad), nullable=False)
    tipo_inmueble = Column(String(50))  # casa, departamento, oficina, local
    superficie = Column(Float)  # metros cuadrados
    dormitorios = Column(Integer)
    banos = Column(Integer)
    descripcion = Column(Text)
    
    # Financiero
    canon_base = Column(Float, nullable=False)
    moneda = Column(String(3), default="BOB", nullable=False)
    estado = Column(Enum(EstadoPropiedad), default=EstadoPropiedad.DISPONIBLE, nullable=False)
    
    # Relationships
    empresa = relationship("Empresa", back_populates="propiedades")
    copropietarios = relationship("Copropietario", back_populates="propiedad", cascade="all, delete-orphan")
    contratos = relationship("Contrato", back_populates="propiedad")
    
    def __repr__(self):
        return f"<Propiedad(id={self.id}, direccion='{self.direccion}', tipo='{self.tipo}')>"
