"""
Importar todos los modelos para que SQLAlchemy los registre
"""
from app.models.user import User
from app.models.propiedad import Propiedad
from app.models.copropietario import Copropietario
from app.models.inquilino import Inquilino
from app.models.contrato import Contrato
from app.models.pago import Pago
from app.models.distribucion_pago import DistribucionPago
from app.models.impuesto import ImpuestoAlquiler, FacturaCompensacion
from app.models.unidad_gasto import UnidadAlquiler, GastoPropiedad
from app.models.base_model import BaseModel

__all__ = [
    "User",
    "Propiedad",
    "Copropietario",
    "Inquilino",
    "Contrato",
    "Pago",
    "DistribucionPago",
    "ImpuestoAlquiler",
    "FacturaCompensacion",
    "UnidadAlquiler",
    "GastoPropiedad",
    "BaseModel"
]