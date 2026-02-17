"""
Schemas Pydantic para Propiedades
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum


class TipoPropiedadEnum(str, Enum):
    PROPIA = "propia"
    COPROPIEDAD = "copropiedad"


class EstadoPropiedadEnum(str, Enum):
    DISPONIBLE = "disponible"
    ALQUILADO = "alquilado"
    MANTENIMIENTO = "mantenimiento"


# Schemas para Copropietario
class CopropietarioBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=200)
    ci: Optional[str] = Field(None, max_length=20)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = None
    porcentaje_participacion: float = Field(..., gt=0, le=100)
    cuenta_bancaria: Optional[str] = None
    banco: Optional[str] = None
    tipo_cuenta: Optional[str] = None


class CopropietarioCreate(CopropietarioBase):
    pass


class CopropietarioResponse(CopropietarioBase):
    id: int
    propiedad_id: int
    
    class Config:
        from_attributes = True


# Schemas para Propiedad
class PropiedadBase(BaseModel):
    direccion: str = Field(..., min_length=10, max_length=300)
    ciudad: str = Field(default="La Paz", max_length=100)
    departamento: str = Field(default="La Paz", max_length=100)
    zona: Optional[str] = None
    tipo: TipoPropiedadEnum
    tipo_inmueble: Optional[str] = None
    superficie: Optional[float] = Field(None, gt=0)
    dormitorios: Optional[int] = Field(None, ge=0)
    banos: Optional[int] = Field(None, ge=0)
    descripcion: Optional[str] = None
    canon_base: float = Field(..., gt=0)
    moneda: str = Field(default="BOB", max_length=3)


class PropiedadCreate(PropiedadBase):
    copropietarios: Optional[List[CopropietarioCreate]] = []
    
    @validator('copropietarios')
    def validar_copropietarios(cls, v, values):
        """Valida que los copropietarios sean correctos para copropiedades"""
        tipo = values.get('tipo')
        
        if tipo == TipoPropiedadEnum.COPROPIEDAD:
            if not v or len(v) == 0:
                raise ValueError("Copropiedad debe tener al menos un copropietario")
            
            total = sum(c.porcentaje_participacion for c in v)
            if abs(total - 100) > 0.01:
                raise ValueError(
                    f"Los porcentajes deben sumar 100% (suma actual: {total}%)"
                )
        
        return v


class PropiedadUpdate(BaseModel):
    direccion: Optional[str] = Field(None, min_length=10, max_length=300)
    ciudad: Optional[str] = None
    zona: Optional[str] = None
    tipo_inmueble: Optional[str] = None
    superficie: Optional[float] = Field(None, gt=0)
    dormitorios: Optional[int] = Field(None, ge=0)
    banos: Optional[int] = Field(None, ge=0)
    descripcion: Optional[str] = None
    canon_base: Optional[float] = Field(None, gt=0)
    estado: Optional[EstadoPropiedadEnum] = None


class PropiedadResponse(PropiedadBase):
    id: int
    empresa_id: int
    estado: str
    copropietarios: List[CopropietarioResponse] = []
    
    class Config:
        from_attributes = True


class PropiedadListResponse(BaseModel):
    id: int
    direccion: str
    ciudad: str
    tipo: str
    canon_base: float
    estado: str
    numero_copropietarios: int = 0
    
    class Config:
        from_attributes = True
