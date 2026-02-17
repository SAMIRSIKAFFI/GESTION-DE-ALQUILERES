from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class Empresa(BaseModel):
    """Modelo de Empresa/Propietario"""
    
    __tablename__ = "empresas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    nit = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(20))
    email = Column(String(100))
    direccion = Column(String(300))
    ciudad = Column(String(100), default="La Paz")
    
    # Relationships
    users = relationship("User", back_populates="empresa")
    propiedades = relationship("Propiedad", back_populates="empresa", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Empresa(id={self.id}, nombre='{self.nombre}', nit='{self.nit}')>"
