"""
Modelos de la aplicación

Importar todos los modelos aquí para que Alembic los detecte
"""

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.empresa import Empresa
from app.models.propiedad import Propiedad, TipoPropiedad, EstadoPropiedad
from app.models.copropietario import Copropietario
from app.models.inquilino import Inquilino
from app.models.contrato import Contrato, EstadoContrato
from app.models.pago import Pago, EstadoPago, FormaPago
from app.models.distribucion_pago import DistribucionPago, EstadoDistribucion

__all__ = [
    "BaseModel",
    "User",
    "Empresa",
    "Propiedad",
    "TipoPropiedad",
    "EstadoPropiedad",
    "Copropietario",
    "Inquilino",
    "Contrato",
    "EstadoContrato",
    "Pago",
    "EstadoPago",
    "FormaPago",
    "DistribucionPago",
    "EstadoDistribucion",
]

from app.models.impuesto import ImpuestoAlquiler, FacturaCompensacion
