from datetime import datetime
from sqlalchemy import Column, DateTime
from app.database.base import Base


class BaseModel(Base):
    """Modelo base con campos de auditoría"""
    
    __abstract__ = True
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # Para soft delete
    
    def soft_delete(self):
        """Marca el registro como eliminado sin borrarlo de la BD"""
        self.deleted_at = datetime.utcnow()
    
    @property
    def is_deleted(self) -> bool:
        """Verifica si el registro está eliminado"""
        return self.deleted_at is not None
