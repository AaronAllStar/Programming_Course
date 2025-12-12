"""
Módulo: cargador_base.py
Descripción: Define la clase abstracta base para todos los cargadores de datos
"""

from abc import ABC, abstractmethod
from pathlib import Path
import sys
import os

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.modelos.dataset import Dataset


class CargadorBase(ABC):
    """
    Clase abstracta base para cargadores de datos.
    
    Esta clase define la interfaz que todos los cargadores deben implementar.
    Aplica el principio de abstracción y permite polimorfismo.
    
    Atributos:
        ruta_archivo (Path): Ruta al archivo a cargar
    """
    
    def __init__(self, ruta_archivo: str):
        """
        Inicializa el cargador con la ruta del archivo.
        
        Args:
            ruta_archivo: Ruta del archivo a cargar
        """
        self._ruta_archivo = Path(ruta_archivo)
    
    @abstractmethod
    def cargar(self) -> Dataset:
        """
        Método abstracto para cargar datos.
        
        Cada subclase debe implementar este método según su formato específico.
        
        Returns:
            Dataset con los datos cargados
            
        Raises:
            NotImplementedError: Si no se implementa en la subclase
        """
        pass
    
    def validar_archivo_existe(self) -> bool:
        """
        Verifica si el archivo existe.
        
        Returns:
            True si el archivo existe, False en caso contrario
        """
        return self._ruta_archivo.exists() and self._ruta_archivo.is_file()
    
    def obtener_ruta(self) -> Path:
        """
        Obtiene la ruta del archivo.
        
        Returns:
            Objeto Path con la ruta del archivo
        """
        return self._ruta_archivo
    
    def obtener_extension(self) -> str:
        """
        Obtiene la extensión del archivo.
        
        Returns:
            Extensión del archivo (ej: '.csv')
        """
        return self._ruta_archivo.suffix
