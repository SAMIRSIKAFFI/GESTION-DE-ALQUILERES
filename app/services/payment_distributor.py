"""
Servicio para distribuir pagos entre copropietarios
"""

from datetime import datetime
from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.pago import Pago
from app.models.propiedad import Propiedad
from app.models.copropietario import Copropietario
from app.models.distribucion_pago import DistribucionPago, EstadoDistribucion


class PaymentDistributor:
    """
    Distribuye pagos entre copropietarios según porcentaje de participación.
    """
    
    @staticmethod
    def validar_porcentajes(db: Session, propiedad_id: int) -> bool:
        """
        Valida que los porcentajes de copropietarios sumen 100%.
        
        Args:
            db: Sesión de base de datos
            propiedad_id: ID de la propiedad
            
        Returns:
            True si es válido, False si no
        """
        copropietarios = db.query(Copropietario).filter(
            Copropietario.propiedad_id == propiedad_id,
            Copropietario.deleted_at == None
        ).all()
        
        if not copropietarios:
            return False
        
        total_porcentaje = sum(c.porcentaje_participacion for c in copropietarios)
        
        # Permitir una tolerancia de 0.01% por redondeo
        return abs(total_porcentaje - 100) <= 0.01
    
    @staticmethod
    def distribuir_pago(db: Session, pago_id: int) -> Dict:
        """
        Distribuye el pago entre los copropietarios de una propiedad.
        
        Args:
            db: Sesión de base de datos
            pago_id: ID del pago a distribuir
            
        Returns:
            Dict con información de la distribución
        """
        pago = db.query(Pago).filter(Pago.id == pago_id).first()
        if not pago:
            raise ValueError(f"Pago con ID {pago_id} no encontrado")
        
        contrato = pago.contrato
        propiedad = contrato.propiedad
        
        # Si no es copropiedad, no hay nada que distribuir
        if propiedad.tipo != TipoPropiedad.COPROPIEDAD:
            return {
                "tipo": "propiedad_propia",
                "monto_total": pago.monto_pagado,
                "distribuciones": [],
                "mensaje": "No requiere distribución (propiedad propia)"
            }
        
        # Verificar si ya existe una distribución para este pago
        distribuciones_existentes = db.query(DistribucionPago).filter(
            DistribucionPago.pago_id == pago.id
        ).first()
        
        if distribuciones_existentes:
            raise ValueError(f"El pago {pago_id} ya tiene distribuciones creadas")
        
        # Obtener copropietarios activos
        copropietarios = db.query(Copropietario).filter(
            Copropietario.propiedad_id == propiedad.id,
            Copropietario.deleted_at == None
        ).all()
        
        if not copropietarios:
            raise ValueError(f"No hay copropietarios registrados para la propiedad {propiedad.id}")
        
        # Validar que los porcentajes sumen 100%
        total_porcentaje = sum(c.porcentaje_participacion for c in copropietarios)
        if abs(total_porcentaje - 100) > 0.01:
            raise ValueError(
                f"Los porcentajes no suman 100% (suma actual: {total_porcentaje}%). "
                f"Debe ajustar los porcentajes de participación."
            )
        
        # Crear distribuciones
        distribuciones = []
        suma_distribuciones = 0
        
        for i, coprop in enumerate(copropietarios):
            # Para el último copropietario, ajustar el monto para evitar errores de redondeo
            if i == len(copropietarios) - 1:
                monto_asignado = pago.monto_pagado - suma_distribuciones
            else:
                monto_asignado = (pago.monto_pagado * coprop.porcentaje_participacion) / 100
                suma_distribuciones += monto_asignado
            
            distribucion = DistribucionPago(
                pago_id=pago.id,
                copropietario_id=coprop.id,
                monto_asignado=round(monto_asignado, 2),
                porcentaje_aplicado=coprop.porcentaje_participacion,
                fecha_distribucion=datetime.now().date(),
                estado=EstadoDistribucion.PENDIENTE
            )
            db.add(distribucion)
            
            distribuciones.append({
                "copropietario_id": coprop.id,
                "copropietario": coprop.nombre,
                "porcentaje": coprop.porcentaje_participacion,
                "monto": round(monto_asignado, 2),
                "cuenta_bancaria": coprop.cuenta_bancaria,
                "banco": coprop.banco
            })
        
        db.commit()
        
        return {
            "tipo": "copropiedad",
            "pago_id": pago.id,
            "periodo": pago.periodo,
            "monto_total": pago.monto_pagado,
            "numero_copropietarios": len(copropietarios),
            "distribuciones": distribuciones,
            "mensaje": "Distribución creada exitosamente"
        }
    
    @staticmethod
    def obtener_reporte_copropietario(
        db: Session,
        copropietario_id: int,
        anio: int = None
    ) -> Dict:
        """
        Genera reporte de ingresos de un copropietario.
        
        Args:
            db: Sesión de base de datos
            copropietario_id: ID del copropietario
            anio: Año del reporte (default: año actual)
            
        Returns:
            Dict con información del reporte
        """
        if anio is None:
            anio = datetime.now().year
        
        copropietario = db.query(Copropietario).filter(
            Copropietario.id == copropietario_id
        ).first()
        
        if not copropietario:
            raise ValueError(f"Copropietario con ID {copropietario_id} no encontrado")
        
        # Obtener todas las distribuciones del año
        distribuciones = db.query(DistribucionPago).join(
            Pago
        ).filter(
            DistribucionPago.copropietario_id == copropietario_id,
            Pago.anio == anio
        ).all()
        
        # Calcular totales
        total_recibido = sum(d.monto_asignado for d in distribuciones if d.estado == EstadoDistribucion.PAGADO)
        total_pendiente = sum(d.monto_asignado for d in distribuciones if d.estado == EstadoDistribucion.PENDIENTE)
        total_anual = sum(d.monto_asignado for d in distribuciones)
        
        # Desglose por mes
        ingresos_mensuales = {}
        for d in distribuciones:
            mes = d.pago.mes
            if mes not in ingresos_mensuales:
                ingresos_mensuales[mes] = {
                    "monto": 0,
                    "estado": []
                }
            ingresos_mensuales[mes]["monto"] += d.monto_asignado
            ingresos_mensuales[mes]["estado"].append(d.estado.value)
        
        return {
            "copropietario": {
                "id": copropietario.id,
                "nombre": copropietario.nombre,
                "porcentaje_participacion": copropietario.porcentaje_participacion,
                "cuenta_bancaria": copropietario.cuenta_bancaria,
                "banco": copropietario.banco
            },
            "propiedad": {
                "id": copropietario.propiedad.id,
                "direccion": copropietario.propiedad.direccion
            },
            "anio": anio,
            "resumen": {
                "total_recibido": round(total_recibido, 2),
                "total_pendiente": round(total_pendiente, 2),
                "total_anual": round(total_anual, 2),
                "numero_distribuciones": len(distribuciones)
            },
            "ingresos_mensuales": ingresos_mensuales
        }
    
    @staticmethod
    def marcar_distribucion_pagada(
        db: Session,
        distribucion_id: int,
        numero_transferencia: str = None,
        fecha_pago: datetime = None
    ) -> DistribucionPago:
        """
        Marca una distribución como pagada.
        
        Args:
            db: Sesión de base de datos
            distribucion_id: ID de la distribución
            numero_transferencia: Número de comprobante/transferencia
            fecha_pago: Fecha efectiva del pago
            
        Returns:
            DistribucionPago actualizada
        """
        distribucion = db.query(DistribucionPago).filter(
            DistribucionPago.id == distribucion_id
        ).first()
        
        if not distribucion:
            raise ValueError(f"Distribución con ID {distribucion_id} no encontrada")
        
        distribucion.estado = EstadoDistribucion.PAGADO
        distribucion.numero_transferencia = numero_transferencia
        distribucion.fecha_pago_efectivo = fecha_pago or datetime.now().date()
        
        db.commit()
        db.refresh(distribucion)
        
        return distribucion
