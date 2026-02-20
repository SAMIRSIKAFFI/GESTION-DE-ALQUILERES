from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.propiedad import Propiedad
from app.models.copropietario import Copropietario

router = APIRouter(prefix="/propiedades", tags=["Propiedades"])

class CopropietarioCreate(BaseModel):
    nombre_completo: str
    ci: str
    telefono: str
    email: str = None
    porcentaje_participacion: float
    cuenta_bancaria: str
    banco: str
    tipo_cuenta: str = "ahorro"

class PropiedadCreate(BaseModel):
    direccion: str
    ciudad: str
    tipo: str
    canon_base: float
    superficie: float = None
    dormitorios: int = None
    banos: int = None
    descripcion: str = None
    # numero_copropietarios: int = 1
    copropietarios: List[CopropietarioCreate] = []

class PropiedadResponse(BaseModel):
    id: int
    direccion: str
    ciudad: str
    tipo: str
    canon_base: float
    estado: str
    # numero_copropietarios: int    # Campo eliminado

@router.post("/", response_model=PropiedadResponse, status_code=status.HTTP_201_CREATED)
def crear_propiedad(propiedad: PropiedadCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if propiedad.tipo == "copropiedad":
        if not propiedad.copropietarios:
            raise HTTPException(status_code=400, detail="Debe agregar al menos un copropietario")
        total_porcentaje = sum(c.porcentaje_participacion for c in propiedad.copropietarios)
        if abs(total_porcentaje - 100) > 0.01:
            raise HTTPException(status_code=400, detail=f"Los porcentajes deben sumar 100%. Suman {total_porcentaje}%")
    
    nueva_propiedad = Propiedad(
        direccion=propiedad.direccion,
        ciudad=propiedad.ciudad,
        tipo=propiedad.tipo,
        canon_base=propiedad.canon_base,
        superficie=propiedad.superficie,
        dormitorios=propiedad.dormitorios,
        banos=propiedad.banos,
        descripcion=propiedad.descripcion,
        estado="disponible"
    )
    db.add(nueva_propiedad)
    db.flush()
    
    for coprop_data in propiedad.copropietarios:
        copropietario = Copropietario(
            propiedad_id=nueva_propiedad.id,
            nombre_completo=coprop_data.nombre_completo,
            ci=coprop_data.ci,
            telefono=coprop_data.telefono,
            email=coprop_data.email,
            porcentaje_participacion=coprop_data.porcentaje_participacion,
            cuenta_bancaria=coprop_data.cuenta_bancaria,
            banco=coprop_data.banco,
            tipo_cuenta=coprop_data.tipo_cuenta
        )
        db.add(copropietario)
    
    db.commit()
    db.refresh(nueva_propiedad)
    return nueva_propiedad

@router.get("/", response_model=List[PropiedadResponse])
def listar_propiedades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    propiedades = db.query(Propiedad).filter(Propiedad.deleted_at == None).offset(skip).limit(limit).all()
    return propiedades

@router.get("/{propiedad_id}", response_model=PropiedadResponse)
def obtener_propiedad(propiedad_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id, Propiedad.deleted_at == None).first()
    if not propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    return propiedad

@router.delete("/{propiedad_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_propiedad(propiedad_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id, Propiedad.deleted_at == None).first()
    if not propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    propiedad.deleted_at = datetime.utcnow()
    db.commit()
    return None