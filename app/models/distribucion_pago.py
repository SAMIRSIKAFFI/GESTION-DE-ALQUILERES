import enum
from sqlalchemy import Column, Integer, Float, ForeignKey, Date, Enum, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class EstadoDistribucion(str, enum.Enum):
    """Estados de distribución de pago"""
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    EN_PROCESO = "en_proceso"


class DistribucionPago(BaseModel):
    """Modelo de Distribución de Pagos a Copropietarios"""
    
    __tablename__ = "distribuciones_pago"
    
    id = Column(Integer, primary_key=True, index=True)
    pago_id = Column(Integer, ForeignKey("pagos.id"), nullable=False)
    copropietario_id = Column(Integer, ForeignKey("copropietarios.id"), nullable=False)
    
    # Montos
    monto_asignado = Column(Float, nullable=False)
    porcentaje_aplicado = Column(Float, nullable=False)
    
    # Fechas
    fecha_distribucion = Column(Date, nullable=False)
    fecha_pago_efectivo = Column(Date, nullable=True)
    
    # Estado
    estado = Column(Enum(EstadoDistribucion), default=EstadoDistribucion.PENDIENTE, nullable=False)
    
    # Comprobante
    numero_transferencia = Column(String(100))
    nota = Column(String(500))
    
    # Relationships
    pago = relationship("Pago", back_populates="distribuciones")
    copropietario = relationship("Copropietario", back_populates="distribuciones")
    
    def __repr__(self):
        return f"<DistribucionPago(id={self.id}, monto={self.monto_asignado}, estado='{self.estado}')>"
