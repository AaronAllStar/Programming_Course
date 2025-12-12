"""
Módulo: dataset.py
Descripción: Define la clase Dataset que representa un conjunto de registros
"""

from typing import List, Callable, Any, Dict
from .registro import Registro


class Dataset:
    """
    Representa un conjunto de registros (dataset completo).
    
    Esta clase actúa como contenedor de múltiples registros y proporciona
    operaciones para manipular el conjunto de datos (filtrado, ordenamiento, etc.)
    
    Atributos:
        registros (list): Lista de objetos Registro
        nombre (str): Nombre descriptivo del dataset
    """
    
    def __init__(self, nombre: str = "Dataset"):
        """
        Inicializa un nuevo dataset vacío.
        
        Args:
            nombre: Nombre descriptivo del dataset
        """
        self._registros: List[Registro] = []
        self._nombre = nombre
    
    def agregar_registro(self, registro: Registro) -> None:
        """
        Agrega un registro al dataset.
        
        Args:
            registro: Objeto Registro a agregar
        """
        if isinstance(registro, Registro):
            self._registros.append(registro)
    
    def agregar_registros(self, registros: List[Registro]) -> None:
        """
        Agrega múltiples registros al dataset.
        
        Args:
            registros: Lista de objetos Registro
        """
        for registro in registros:
            self.agregar_registro(registro)
    
    def obtener_registros(self) -> List[Registro]:
        """
        Obtiene todos los registros del dataset.
        
        Returns:
            Lista de registros
        """
        return self._registros.copy()
    
    def cantidad_registros(self) -> int:
        """
        Obtiene la cantidad de registros en el dataset.
        
        Returns:
            Número de registros
        """
        return len(self._registros)
    
    def obtener_registro(self, indice: int) -> Registro:
        """
        Obtiene un registro específico por su índice.
        
        Args:
            indice: Índice del registro (empezando en 0)
            
        Returns:
            Registro en la posición indicada
            
        Raises:
            IndexError: Si el índice está fuera de rango
        """
        return self._registros[indice]
    
    def esta_vacio(self) -> bool:
        """
        Verifica si el dataset está vacío.
        
        Returns:
            True si no hay registros, False en caso contrario
        """
        return len(self._registros) == 0
    
    def limpiar(self) -> None:
        """
        Elimina todos los registros del dataset.
        """
        self._registros.clear()
    
    def filtrar(self, condicion: Callable[[Registro], bool]) -> 'Dataset':
        """
        Filtra registros según una condición.
        
        Args:
            condicion: Función que toma un Registro y retorna bool
            
        Returns:
            Nuevo Dataset con los registros que cumplen la condición
        """
        dataset_filtrado = Dataset(f"{self._nombre}_filtrado")
        for registro in self._registros:
            if condicion(registro):
                dataset_filtrado.agregar_registro(registro)
        return dataset_filtrado
    
    def ordenar(self, campo: str, reverso: bool = False) -> None:
        """
        Ordena los registros según un campo específico.
        
        Args:
            campo: Nombre del campo por el cual ordenar
            reverso: Si True, ordena de forma descendente
        """
        self._registros.sort(
            key=lambda r: r.obtener_campo(campo) or "",
            reverse=reverso
        )
    
    def obtener_campos(self) -> List[str]:
        """
        Obtiene la lista de campos disponibles en el dataset.
        
        Returns:
            Lista de nombres de campos (del primer registro)
        """
        if self.esta_vacio():
            return []
        return list(self._registros[0].obtener_todos_campos().keys())
    
    def obtener_valores_campo(self, nombre_campo: str) -> List[Any]:
        """
        Obtiene todos los valores de un campo específico.
        
        Args:
            nombre_campo: Nombre del campo
            
        Returns:
            Lista con los valores del campo en todos los registros
        """
        valores = []
        for registro in self._registros:
            valor = registro.obtener_campo(nombre_campo)
            if valor is not None:
                valores.append(valor)
        return valores
    
    def obtener_valores_unicos(self, nombre_campo: str) -> List[Any]:
        """
        Obtiene los valores únicos de un campo.
        
        Args:
            nombre_campo: Nombre del campo
            
        Returns:
            Lista de valores únicos
        """
        valores = self.obtener_valores_campo(nombre_campo)
        return list(set(valores))
    
    def obtener_nombre(self) -> str:
        """
        Obtiene el nombre del dataset.
        
        Returns:
            Nombre del dataset
        """
        return self._nombre
    
    def establecer_nombre(self, nombre: str) -> None:
        """
        Establece un nuevo nombre para el dataset.
        
        Args:
            nombre: Nuevo nombre
        """
        self._nombre = nombre
    
    def __len__(self) -> int:
        """
        Retorna la cantidad de registros.
        
        Returns:
            Número de registros
        """
        return len(self._registros)
    
    def __str__(self) -> str:
        """
        Representación en string del dataset.
        
        Returns:
            String describiendo el dataset
        """
        return f"Dataset '{self._nombre}' con {len(self._registros)} registros"
    
    def __repr__(self) -> str:
        """
        Representación técnica del dataset.
        
        Returns:
            String representando el objeto
        """
        return f"Dataset(nombre='{self._nombre}', registros={len(self._registros)})"
