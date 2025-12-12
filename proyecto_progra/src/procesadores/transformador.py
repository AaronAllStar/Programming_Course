"""
Módulo: transformador.py
Descripción: Clase para transformar y filtrar datos del dataset
"""

import sys
import os
from typing import Callable, Any, Dict

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.modelos.dataset import Dataset
from src.modelos.registro import Registro


class Transformador:
    """
    Clase para transformar y filtrar datos.
    
    Proporciona métodos para filtrar registros, ordenar, agrupar y calcular
    valores derivados.
    
    Esta clase implementa el principio de responsabilidad única (SRP):
    se encarga únicamente de transformar datos.
    """
    
    def __init__(self, dataset: Dataset):
        """
        Inicializa el transformador con un dataset.
        
        Args:
            dataset: Dataset a transformar
        """
        self._dataset = dataset
    
    def filtrar_por_campo(self, nombre_campo: str, valor: Any) -> Dataset:
        """
        Filtra registros donde un campo específico tiene un valor determinado.
        
        Args:
            nombre_campo: Nombre del campo a filtrar
            valor: Valor que debe tener el campo
            
        Returns:
            Nuevo dataset con los registros filtrados
        """
        def condicion(registro: Registro) -> bool:
            return registro.obtener_campo(nombre_campo) == valor
        
        dataset_filtrado = self._dataset.filtrar(condicion)
        print(f"✓ Filtrado completado: {dataset_filtrado.cantidad_registros()} registros encontrados")
        return dataset_filtrado
    
    def filtrar_por_rango_numerico(self, nombre_campo: str, minimo: float, maximo: float) -> Dataset:
        """
        Filtra registros donde un campo numérico está en un rango.
        
        Args:
            nombre_campo: Nombre del campo numérico
            minimo: Valor mínimo (inclusivo)
            maximo: Valor máximo (inclusivo)
            
        Returns:
            Nuevo dataset con los registros filtrados
        """
        def condicion(registro: Registro) -> bool:
            valor = registro.obtener_campo(nombre_campo)
            if valor is None:
                return False
            try:
                valor_num = float(valor)
                return minimo <= valor_num <= maximo
            except ValueError:
                return False
        
        dataset_filtrado = self._dataset.filtrar(condicion)
        print(f"✓ Filtrado por rango: {dataset_filtrado.cantidad_registros()} registros")
        return dataset_filtrado
    
    def filtrar_por_condicion_personalizada(self, condicion: Callable[[Registro], bool]) -> Dataset:
        """
        Filtra registros usando una función de condición personalizada.
        
        Args:
            condicion: Función que toma un Registro y retorna bool
            
        Returns:
            Nuevo dataset con los registros filtrados
        """
        dataset_filtrado = self._dataset.filtrar(condicion)
        print(f"✓ Filtrado personalizado: {dataset_filtrado.cantidad_registros()} registros")
        return dataset_filtrado
    
    def ordenar_por_campo(self, nombre_campo: str, descendente: bool = False) -> None:
        """
        Ordena el dataset por un campo específico.
        
        Args:
            nombre_campo: Nombre del campo por el que ordenar
            descendente: Si True, ordena de mayor a menor
        """
        self._dataset.ordenar(nombre_campo, reverso=descendente)
        orden = "descendente" if descendente else "ascendente"
        print(f"✓ Dataset ordenado por '{nombre_campo}' ({orden})")
    
    def agregar_campo_calculado(self, nombre_nuevo_campo: str, 
                                funcion_calculo: Callable[[Registro], Any]) -> None:
        """
        Agrega un nuevo campo calculado a todos los registros.
        
        Args:
            nombre_nuevo_campo: Nombre del campo a crear
            funcion_calculo: Función que calcula el valor del nuevo campo
        """
        for registro in self._dataset.obtener_registros():
            valor_calculado = funcion_calculo(registro)
            registro.establecer_campo(nombre_nuevo_campo, valor_calculado)
        
        print(f"✓ Campo calculado '{nombre_nuevo_campo}' agregado a todos los registros")
    
    def agrupar_por_campo(self, nombre_campo: str) -> Dict[Any, Dataset]:
        """
        Agrupa registros por los valores únicos de un campo.
        
        Args:
            nombre_campo: Nombre del campo por el que agrupar
            
        Returns:
            Diccionario donde las claves son valores únicos y los valores son Datasets
        """
        grupos = {}
        valores_unicos = self._dataset.obtener_valores_unicos(nombre_campo)
        
        for valor in valores_unicos:
            # Filtrar registros para este valor
            dataset_grupo = self.filtrar_por_campo(nombre_campo, valor)
            grupos[valor] = dataset_grupo
        
        print(f"✓ Datos agrupados en {len(grupos)} grupos por '{nombre_campo}'")
        return grupos
    
    def calcular_totales_por_grupo(self, campo_agrupacion: str, 
                                   campo_suma: str) -> Dict[Any, float]:
        """
        Calcula totales de un campo numérico agrupado por otro campo.
        
        Args:
            campo_agrupacion: Campo por el que agrupar
            campo_suma: Campo numérico a sumar
            
        Returns:
            Diccionario con los totales por grupo
        """
        grupos = self.agrupar_por_campo(campo_agrupacion)
        totales = {}
        
        for valor, dataset_grupo in grupos.items():
            total = 0
            for registro in dataset_grupo.obtener_registros():
                valor_campo = registro.obtener_campo(campo_suma)
                if valor_campo is not None:
                    try:
                        total += float(valor_campo)
                    except ValueError:
                        pass
            totales[valor] = round(total, 2)
        
        return totales
    
    def seleccionar_campos(self, campos: list) -> Dataset:
        """
        Crea un nuevo dataset con solo los campos especificados.
        
        Args:
            campos: Lista de nombres de campos a mantener
            
        Returns:
            Nuevo dataset con solo los campos seleccionados
        """
        dataset_nuevo = Dataset(f"{self._dataset.obtener_nombre()}_proyectado")
        
        for registro in self._dataset.obtener_registros():
            datos_filtrados = {}
            for campo in campos:
                if registro.tiene_campo(campo):
                    datos_filtrados[campo] = registro.obtener_campo(campo)
            
            nuevo_registro = Registro(datos_filtrados)
            dataset_nuevo.agregar_registro(nuevo_registro)
        
        print(f"✓ Proyección creada con {len(campos)} campos")
        return dataset_nuevo
    
    def obtener_primeros_n(self, n: int) -> Dataset:
        """
        Obtiene los primeros N registros del dataset.
        
        Args:
            n: Número de registros a obtener
            
        Returns:
            Nuevo dataset con los primeros N registros
        """
        dataset_limitado = Dataset(f"{self._dataset.obtener_nombre()}_top{n}")
        registros = self._dataset.obtener_registros()[:n]
        dataset_limitado.agregar_registros(registros)
        
        print(f"✓ Se obtuvieron los primeros {n} registros")
        return dataset_limitado
    
    def obtener_dataset(self) -> Dataset:
        """
        Obtiene el dataset actual.
        
        Returns:
            Dataset actual
        """
        return self._dataset
