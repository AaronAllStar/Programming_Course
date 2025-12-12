"""
Módulo de Cargadores de Datos
Contiene clases para cargar datos desde diferentes fuentes
"""

from .cargador_base import CargadorBase
from .cargador_csv import CargadorCSV

__all__ = ['CargadorBase', 'CargadorCSV']
