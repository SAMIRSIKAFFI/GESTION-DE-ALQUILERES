from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class Inquilino(BaseModel):
    """Modelo de Inquilino/Arrendatario"""
    
    __tablename__ = "inquilinos"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos personales
    nombre_completo = Column(String(200), nullable=False)
    ci = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(20))
    telefono_alternativo = Column(String(20))
    email = Column(String(100))
    
    # Dirección
    direccion_actual = Column(String(300))
    ciudad_origen = Column(String(100))
    
    # Laboral
    ocupacion = Column(String(100))
    lugar_trabajo = Column(String(200))
    telefono_trabajo = Column(String(20))
    
    # Estado
    estado = Column(String(20), default="activo", nullable=False)  # activo, inactivo
    
    # Referencias
    referencia_nombre = Column(String(200))
    referencia_telefono = Column(String(20))
    
    # Relationships
    contratos = relationship("Contrato", back_populates="inquilino")
    
    def __repr__(self):
        return f"<Inquilino(id={self.id}, nombre='{self.nombre_completo}', ci='{self.ci}')>"
