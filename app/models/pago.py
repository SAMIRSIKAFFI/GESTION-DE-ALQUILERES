import enum
from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class EstadoPago(str, enum.Enum):
    """Estados de un pago"""
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    PARCIAL = "parcial"
    VENCIDO = "vencido"


class FormaPago(str, enum.Enum):
    """Formas de pago"""
    EFECTIVO = "efectivo"
    TRANSFERENCIA = "transferencia"
    CHEQUE = "cheque"
    DEPOSITO = "deposito"
    QR = "qr"


class Pago(BaseModel):
    """Modelo de Pago de Alquiler"""
    
    __tablename__ = "pagos"
    
    id = Column(Integer, primary_key=True, index=True)
    contrato_id = Column(Integer, ForeignKey("contratos.id"), nullable=False)
    
    # Periodo
    periodo = Column(String(7), nullable=False)  # Formato: YYYY-MM (ej: 2026-02)
    anio = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    
    # Fechas
    fecha_vencimiento = Column(Date, nullable=False)
    fecha_pago = Column(Date, nullable=True)
    
    # Montos
    monto_esperado = Column(Float, nullable=False)
    monto_pagado = Column(Float, default=0, nullable=False)
    mora_calculada = Column(Float, default=0, nullable=False)
    
    # Mora
    dias_atraso = Column(Integer, default=0, nullable=False)
    
    # Detalles
    forma_pago = Column(Enum(FormaPago), nullable=True)
    numero_comprobante = Column(String(100))
    nota = Column(String(500))
    
    # Estado
    estado = Column(Enum(EstadoPago), default=EstadoPago.PENDIENTE, nullable=False)
    
    # Relationships
    contrato = relationship("Contrato", back_populates="pagos")
    distribuciones = relationship("DistribucionPago", back_populates="pago", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Pago(id={self.id}, periodo='{self.periodo}', estado='{self.estado}', monto={self.monto_pagado})>"
