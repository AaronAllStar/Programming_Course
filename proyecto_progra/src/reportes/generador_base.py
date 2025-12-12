"""
Módulo: generador_base.py
Descripción: Define la clase abstracta base para generadores de reportes
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
import sys
import os

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class GeneradorReporteBase(ABC):
    """
    Clase abstracta base para generadores de reportes.
    
    Define la interfaz que todos los generadores de reportes deben implementar.
    Aplica el patrón Template Method.
    
    Atributos:
        datos (dict): Datos a incluir en el reporte
        titulo (str): Título del reporte
    """
    
    def __init__(self, titulo: str = "Reporte"):
        """
        Inicializa el generador de reportes.
        
        Args:
            titulo: Título del reporte
        """
        self._titulo = titulo
        self._datos = {}
    
    def establecer_datos(self, datos: Dict[str, Any]) -> None:
        """
        Establece los datos para el reporte.
        
        Args:
            datos: Diccionario con los datos del reporte
        """
        self._datos = datos
    
    @abstractmethod
    def generar(self) -> None:
        """
        Método abstracto para generar el reporte.
        
        Cada subclase debe implementar cómo se genera y presenta el reporte.
        
        Raises:
            NotImplementedError: Si no se implementa en la subclase
        """
        pass
    
    def obtener_titulo(self) -> str:
        """
        Obtiene el título del reporte.
        
        Returns:
            Título del reporte
        """
        return self._titulo
    
    def establecer_titulo(self, titulo: str) -> None:
        """
        Establece un nuevo título para el reporte.
        
        Args:
            titulo: Nuevo título
        """
        self._titulo = titulo
    
    def _formatear_numero(self, numero: float, decimales: int = 2) -> str:
        """
        Formatea un número con separadores de miles y decimales.
        
        Args:
            numero: Número a formatear
            decimales: Cantidad de decimales
            
        Returns:
            Número formateado como string
        """
        return f"{numero:,.{decimales}f}"
    
    def _crear_linea_separadora(self, longitud: int = 50, caracter: str = "=") -> str:
        """
        Crea una línea separadora.
        
        Args:
            longitud: Longitud de la línea
            caracter: Carácter a usar
            
        Returns:
            Línea separadora
        """
        return caracter * longitud
