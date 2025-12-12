"""
Módulo: registro.py
Descripción: Define la clase Registro que representa una fila individual del dataset
"""

from datetime import datetime
from typing import Any, Dict


class Registro:
    """
    Representa un registro individual del dataset.
    
    Cada registro es una fila de datos con campos específicos.
    Esta clase encapsula los datos y proporciona métodos para acceder y validar.
    
    Atributos:
        datos (dict): Diccionario con los campos y valores del registro
    """
    
    def __init__(self, datos: Dict[str, Any]):
        """
        Inicializa un nuevo registro.
        
        Args:
            datos (dict): Diccionario con los campos del registro
        """
        self._datos = datos
    
    def obtener_campo(self, nombre_campo: str) -> Any:
        """
        Obtiene el valor de un campo específico.
        
        Args:
            nombre_campo: Nombre del campo a obtener
            
        Returns:
            Valor del campo o None si no existe
        """
        return self._datos.get(nombre_campo)
    
    def establecer_campo(self, nombre_campo: str, valor: Any) -> None:
        """
        Establece el valor de un campo.
        
        Args:
            nombre_campo: Nombre del campo
            valor: Nuevo valor para el campo
        """
        self._datos[nombre_campo] = valor
    
    def obtener_todos_campos(self) -> Dict[str, Any]:
        """
        Obtiene todos los campos del registro.
        
        Returns:
            Diccionario con todos los campos
        """
        return self._datos.copy()
    
    def tiene_campo(self, nombre_campo: str) -> bool:
        """
        Verifica si el registro tiene un campo específico.
        
        Args:
            nombre_campo: Nombre del campo a verificar
            
        Returns:
            True si el campo existe, False en caso contrario
        """
        return nombre_campo in self._datos
    
    def es_valido(self) -> bool:
        """
        Verifica si el registro es válido (tiene al menos un campo).
        
        Returns:
            True si el registro es válido, False en caso contrario
        """
        return len(self._datos) > 0
    
    def obtener_campos_vacios(self) -> list:
        """
        Obtiene la lista de campos que tienen valores nulos o vacíos.
        
        Returns:
            Lista de nombres de campos vacíos
        """
        campos_vacios = []
        for campo, valor in self._datos.items():
            if valor is None or valor == '' or valor == 'NULL':
                campos_vacios.append(campo)
        return campos_vacios
    
    def __str__(self) -> str:
        """
        Representación en string del registro.
        
        Returns:
            String con los datos del registro
        """
        return str(self._datos)
    
    def __repr__(self) -> str:
        """
        Representación técnica del registro.
        
        Returns:
            String representando el objeto
        """
        return f"Registro({self._datos})"
    
    def __eq__(self, otro) -> bool:
        """
        Compara dos registros para ver si son iguales.
        
        Args:
            otro: Otro registro a comparar
            
        Returns:
            True si son iguales, False en caso contrario
        """
        if not isinstance(otro, Registro):
            return False
        return self._datos == otro._datos
