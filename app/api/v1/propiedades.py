"""
Endpoints de Propiedades
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.propiedad import Propiedad
from app.models.copropietario import Copropietario
from app.schemas.propiedad import (
    PropiedadCreate,
    PropiedadResponse,
    PropiedadListResponse,
    PropiedadUpdate
)

router = APIRouter()


@router.post("/propiedades", response_model=PropiedadResponse, status_code=status.HTTP_201_CREATED)
def crear_propiedad(
    propiedad_data: PropiedadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Crear una nueva propiedad con copropietarios (si aplica)
    """
    # Verificar que el usuario tenga una empresa asociada
    if not current_user.empresa_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario debe estar asociado a una empresa"
        )
    
    # Crear propiedad
    nueva_propiedad = Propiedad(
        empresa_id=current_user.empresa_id,
        direccion=propiedad_data.direccion,
        ciudad=propiedad_data.ciudad,
        departamento=propiedad_data.departamento,
        zona=propiedad_data.zona,
        tipo=propiedad_data.tipo,
        tipo_inmueble=propiedad_data.tipo_inmueble,
        superficie=propiedad_data.superficie,
        dormitorios=propiedad_data.dormitorios,
        banos=propiedad_data.banos,
        descripcion=propiedad_data.descripcion,
        canon_base=propiedad_data.canon_base,
        moneda=propiedad_data.moneda
    )
    
    db.add(nueva_propiedad)
    db.flush()  # Para obtener el ID antes de commit
    
    # Agregar copropietarios si existen
    if propiedad_data.copropietarios:
        for coprop_data in propiedad_data.copropietarios:
            coprop = Copropietario(
                propiedad_id=nueva_propiedad.id,
                **coprop_data.dict()
            )
            db.add(coprop)
    
    db.commit()
    db.refresh(nueva_propiedad)
    
    return nueva_propiedad


@router.get("/propiedades", response_model=List[PropiedadListResponse])
def listar_propiedades(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Listar todas las propiedades del usuario actual
    """
    propiedades = db.query(Propiedad).filter(
        Propiedad.empresa_id == current_user.empresa_id,
        Propiedad.deleted_at == None
    ).offset(skip).limit(limit).all()
    
    # Agregar conteo de copropietarios
    result = []
    for prop in propiedades:
        coprop_count = db.query(Copropietario).filter(
            Copropietario.propiedad_id == prop.id,
            Copropietario.deleted_at == None
        ).count()
        
        result.append(PropiedadListResponse(
            id=prop.id,
            direccion=prop.direccion,
            ciudad=prop.ciudad,
            tipo=prop.tipo.value,
            canon_base=prop.canon_base,
            estado=prop.estado.value,
            numero_copropietarios=coprop_count
        ))
    
    return result


@router.get("/propiedades/{propiedad_id}", response_model=PropiedadResponse)
def obtener_propiedad(
    propiedad_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener detalles de una propiedad específica
    """
    propiedad = db.query(Propiedad).filter(
        Propiedad.id == propiedad_id,
        Propiedad.empresa_id == current_user.empresa_id,
        Propiedad.deleted_at == None
    ).first()
    
    if not propiedad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Propiedad no encontrada"
        )
    
    return propiedad


@router.put("/propiedades/{propiedad_id}", response_model=PropiedadResponse)
def actualizar_propiedad(
    propiedad_id: int,
    propiedad_data: PropiedadUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Actualizar una propiedad
    """
    propiedad = db.query(Propiedad).filter(
        Propiedad.id == propiedad_id,
        Propiedad.empresa_id == current_user.empresa_id,
        Propiedad.deleted_at == None
    ).first()
    
    if not propiedad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Propiedad no encontrada"
        )
    
    # Actualizar campos
    for field, value in propiedad_data.dict(exclude_unset=True).items():
        setattr(propiedad, field, value)
    
    db.commit()
    db.refresh(propiedad)
    
    return propiedad


@router.delete("/propiedades/{propiedad_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_propiedad(
    propiedad_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Eliminar una propiedad (soft delete)
    """
    propiedad = db.query(Propiedad).filter(
        Propiedad.id == propiedad_id,
        Propiedad.empresa_id == current_user.empresa_id,
        Propiedad.deleted_at == None
    ).first()
    
    if not propiedad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Propiedad no encontrada"
        )
    
    # Soft delete
    propiedad.soft_delete()
    db.commit()
    
    return None
