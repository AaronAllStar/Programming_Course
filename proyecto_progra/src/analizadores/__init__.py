"""
Módulo de Analizadores de Datos
Contiene clases para realizar análisis estadísticos
"""

from .analizador_base import AnalizadorBase
from .analizador_estadistico import AnalizadorEstadistico
from .analizador_ventas import AnalizadorVentas

__all__ = ['AnalizadorBase', 'AnalizadorEstadistico', 'AnalizadorVentas']
