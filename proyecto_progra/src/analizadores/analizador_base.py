"""
Módulo: analizador_base.py
Descripción: Define la clase abstracta base para todos los analizadores
"""

from abc import ABC, abstractmethod
import sys
import os

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.modelos.dataset import Dataset


class AnalizadorBase(ABC):
    """
    Clase abstracta base para analizadores de datos.
    
    Define la interfaz que todos los analizadores deben implementar.
    Aplica el principio de abstracción y permite polimorfismo.
    
    Atributos:
        dataset (Dataset): Dataset a analizar
    """
    
    def __init__(self, dataset: Dataset):
        """
        Inicializa el analizador con un dataset.
        
        Args:
            dataset: Dataset a analizar
        """
        self._dataset = dataset
        self._resultados = {}
    
    @abstractmethod
    def analizar(self) -> dict:
        """
        Método abstracto para realizar el análisis.
        
        Cada subclase debe implementar su propio análisis específico.
        
        Returns:
            Diccionario con los resultados del análisis
            
        Raises:
            NotImplementedError: Si no se implementa en la subclase
        """
        pass
    
    def obtener_resultados(self) -> dict:
        """
        Obtiene los resultados del último análisis.
        
        Returns:
            Diccionario con los resultados
        """
        return self._resultados.copy()
    
    def obtener_dataset(self) -> Dataset:
        """
        Obtiene el dataset que se está analizando.
        
        Returns:
            Dataset
        """
        return self._dataset
    
    def _guardar_resultados(self, resultados: dict) -> None:
        """
        Guarda los resultados del análisis (método protegido).
        
        Args:
            resultados: Diccionario con los resultados
        """
        self._resultados = resultados
