import enum
from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String, Text, Enum
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class EstadoContrato(str, enum.Enum):
    """Estados de un contrato"""
    VIGENTE = "vigente"
    FINALIZADO = "finalizado"
    RESCINDIDO = "rescindido"


class Contrato(BaseModel):
    """Modelo de Contrato de Arrendamiento"""
    
    __tablename__ = "contratos"
    
    id = Column(Integer, primary_key=True, index=True)
    numero_contrato = Column(String(50), unique=True, nullable=False)
    
    # Relaciones
    propiedad_id = Column(Integer, ForeignKey("propiedades.id"), nullable=False)
    unidad_id = Column(Integer, ForeignKey("unidades_alquiler.id"), nullable=True)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    
    # Fechas
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    
    # Financiero
    canon_mensual = Column(Float, nullable=False)
    garantia = Column(Float, nullable=False)
    incremento_anual = Column(Float, default=0)  # Porcentaje (ej: 5.5 = 5.5%)
    dia_pago = Column(Integer, default=5, nullable=False)  # Día del mes para pago (1-31)
    
    # Mora
    tasa_mora_diaria = Column(Float, default=0.5, nullable=False)  # % por día
    
    # Cláusulas
    clausulas_adicionales = Column(Text)
    permite_mascotas = Column(String(10), default="no")  # si, no, negociable
    
    # Estado
    estado = Column(Enum(EstadoContrato), default=EstadoContrato.VIGENTE, nullable=False)
    
    # Archivos (rutas)
    archivo_contrato = Column(String(500))  # Ruta al PDF/DOCX del contrato firmado
    
    # Relationships
    propiedad = relationship("Propiedad", back_populates="contratos")
    inquilino = relationship("Inquilino", back_populates="contratos")
    pagos = relationship("Pago", back_populates="contrato", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Contrato(id={self.id}, numero='{self.numero_contrato}', estado='{self.estado}')>"
