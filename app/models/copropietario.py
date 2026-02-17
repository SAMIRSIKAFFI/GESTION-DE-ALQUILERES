from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class Copropietario(BaseModel):
    """Modelo de Copropietario de un inmueble"""
    
    __tablename__ = "copropietarios"
    
    id = Column(Integer, primary_key=True, index=True)
    propiedad_id = Column(Integer, ForeignKey("propiedades.id"), nullable=False)
    
    # Datos personales
    nombre = Column(String(200), nullable=False)
    ci = Column(String(20))
    telefono = Column(String(20))
    email = Column(String(100))
    
    # Participación
    porcentaje_participacion = Column(Float, nullable=False)  # 0-100
    
    # Datos bancarios
    cuenta_bancaria = Column(String(50))
    banco = Column(String(100))
    tipo_cuenta = Column(String(20))  # ahorro, corriente
    
    # Relationships
    propiedad = relationship("Propiedad", back_populates="copropietarios")
    distribuciones = relationship("DistribucionPago", back_populates="copropietario")
    
    def __repr__(self):
        return f"<Copropietario(id={self.id}, nombre='{self.nombre}', participacion={self.porcentaje_participacion}%)>"
