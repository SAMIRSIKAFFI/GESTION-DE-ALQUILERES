"""
Servicio para calcular mora según normativa boliviana
"""

from datetime import datetime, date
from typing import Dict
from sqlalchemy.orm import Session
from app.models.pago import Pago, EstadoPago
from app.models.contrato import Contrato


class MoraCalculator:
    """
    Calcula mora según normativa boliviana y configuración del contrato.
    
    Normativa: Según Código Civil Boliviano, se puede pactar mora.
    Default: 0.5% por día de atraso sobre el monto pendiente.
    """
    
    @staticmethod
    def calcular_mora(
        pago: Pago,
        contrato: Contrato,
        fecha_calculo: date = None
    ) -> Dict[str, float]:
        """
        Calcula la mora acumulada hasta una fecha específica.
        
        Args:
            pago: Objeto Pago
            contrato: Objeto Contrato
            fecha_calculo: Fecha hasta la cual calcular (default: hoy)
            
        Returns:
            Dict con: dias_atraso, mora_calculada, monto_total, monto_pendiente
        """
        if fecha_calculo is None:
            fecha_calculo = datetime.now().date()
        
        # Si ya está pagado completamente, no hay mora adicional
        if pago.estado == EstadoPago.PAGADO and pago.monto_pagado >= pago.monto_esperado:
            return {
                "dias_atraso": 0,
                "mora_calculada": pago.mora_calculada,  # Mora ya pagada
                "monto_total": pago.monto_pagado,
                "monto_pendiente": 0
            }
        
        # Calcular días de atraso
        if fecha_calculo > pago.fecha_vencimiento:
            dias_atraso = (fecha_calculo - pago.fecha_vencimiento).days
        else:
            dias_atraso = 0
        
        # Calcular monto pendiente
        monto_pendiente = pago.monto_esperado - pago.monto_pagado
        
        # Calcular mora
        if dias_atraso > 0 and monto_pendiente > 0:
            tasa_diaria = contrato.tasa_mora_diaria / 100  # Convertir a decimal
            mora = monto_pendiente * tasa_diaria * dias_atraso
        else:
            mora = 0
        
        return {
            "dias_atraso": dias_atraso,
            "mora_calculada": round(mora, 2),
            "monto_total": round(pago.monto_pagado + mora, 2),
            "monto_pendiente": round(monto_pendiente, 2)
        }
    
    @staticmethod
    def actualizar_mora_pago(
        db: Session,
        pago_id: int,
        fecha_calculo: date = None
    ) -> Dict[str, float]:
        """
        Actualiza la mora de un pago específico.
        
        Args:
            db: Sesión de base de datos
            pago_id: ID del pago
            fecha_calculo: Fecha hasta la cual calcular (default: hoy)
            
        Returns:
            Dict con información de la mora actualizada
        """
        pago = db.query(Pago).filter(Pago.id == pago_id).first()
        if not pago:
            raise ValueError(f"Pago con ID {pago_id} no encontrado")
        
        contrato = db.query(Contrato).filter(Contrato.id == pago.contrato_id).first()
        if not contrato:
            raise ValueError(f"Contrato con ID {pago.contrato_id} no encontrado")
        
        mora_data = MoraCalculator.calcular_mora(pago, contrato, fecha_calculo)
        
        # Actualizar pago
        pago.dias_atraso = mora_data["dias_atraso"]
        pago.mora_calculada = mora_data["mora_calculada"]
        
        # Actualizar estado
        if mora_data["monto_pendiente"] == 0:
            pago.estado = EstadoPago.PAGADO
        elif mora_data["dias_atraso"] > 0:
            pago.estado = EstadoPago.VENCIDO
        elif pago.monto_pagado > 0:
            pago.estado = EstadoPago.PARCIAL
        
        db.commit()
        db.refresh(pago)
        
        return mora_data
    
    @staticmethod
    def actualizar_mora_contrato(
        db: Session,
        contrato_id: int,
        fecha_calculo: date = None
    ) -> int:
        """
        Actualiza la mora de todos los pagos pendientes de un contrato.
        
        Args:
            db: Sesión de base de datos
            contrato_id: ID del contrato
            fecha_calculo: Fecha hasta la cual calcular (default: hoy)
            
        Returns:
            Número de pagos actualizados
        """
        contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
        if not contrato:
            raise ValueError(f"Contrato con ID {contrato_id} no encontrado")
        
        pagos_pendientes = db.query(Pago).filter(
            Pago.contrato_id == contrato_id,
            Pago.estado.in_([EstadoPago.PENDIENTE, EstadoPago.PARCIAL, EstadoPago.VENCIDO])
        ).all()
        
        for pago in pagos_pendientes:
            mora_data = MoraCalculator.calcular_mora(pago, contrato, fecha_calculo)
            pago.dias_atraso = mora_data["dias_atraso"]
            pago.mora_calculada = mora_data["mora_calculada"]
            
            # Actualizar estado
            if mora_data["monto_pendiente"] == 0:
                pago.estado = EstadoPago.PAGADO
            elif mora_data["dias_atraso"] > 0:
                pago.estado = EstadoPago.VENCIDO
        
        db.commit()
        return len(pagos_pendientes)
    
    @staticmethod
    def calcular_mora_total_contrato(
        db: Session,
        contrato_id: int,
        fecha_calculo: date = None
    ) -> Dict[str, float]:
        """
        Calcula el total de mora acumulada en un contrato.
        
        Args:
            db: Sesión de base de datos
            contrato_id: ID del contrato
            fecha_calculo: Fecha hasta la cual calcular (default: hoy)
            
        Returns:
            Dict con: mora_total, monto_pendiente_total, numero_pagos_atrasados
        """
        contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
        if not contrato:
            raise ValueError(f"Contrato con ID {contrato_id} no encontrado")
        
        pagos_pendientes = db.query(Pago).filter(
            Pago.contrato_id == contrato_id,
            Pago.estado.in_([EstadoPago.PENDIENTE, EstadoPago.PARCIAL, EstadoPago.VENCIDO])
        ).all()
        
        mora_total = 0
        monto_pendiente_total = 0
        
        for pago in pagos_pendientes:
            mora_data = MoraCalculator.calcular_mora(pago, contrato, fecha_calculo)
            mora_total += mora_data["mora_calculada"]
            monto_pendiente_total += mora_data["monto_pendiente"]
        
        return {
            "mora_total": round(mora_total, 2),
            "monto_pendiente_total": round(monto_pendiente_total, 2),
            "numero_pagos_atrasados": len(pagos_pendientes)
        }
