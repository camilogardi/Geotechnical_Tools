"""
Módulo de utilidades para cálculos geotécnicos
"""

from .geotechnical_calcs import (
    calcular_factores_capacidad_portante,
    calcular_factores_forma,
    calcular_asentamiento_consolidacion,
    calcular_asentamiento_elastico,
    clasificar_sucs
)

__all__ = [
    'calcular_factores_capacidad_portante',
    'calcular_factores_forma',
    'calcular_asentamiento_consolidacion',
    'calcular_asentamiento_elastico',
    'clasificar_sucs'
]
