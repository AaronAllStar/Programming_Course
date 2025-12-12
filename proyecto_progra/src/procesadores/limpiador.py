"""
Módulo: limpiador.py
Descripción: Clase para limpiar y validar datos del dataset
"""

import sys
import os

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.modelos.dataset import Dataset
from src.modelos.registro import Registro


class Limpiador:
    """
    Clase para limpiar y validar datos.
    
    Proporciona métodos para eliminar duplicados, manejar valores nulos,
    validar tipos de datos y normalizar formatos.
    
    Esta clase implementa el principio de responsabilidad única (SRP):
    se encarga únicamente de la limpieza de datos.
    """
    
    def __init__(self, dataset: Dataset):
        """
        Inicializa el limpiador con un dataset.
        
        Args:
            dataset: Dataset a limpiar
        """
        self._dataset = dataset
    
    def eliminar_duplicados(self) -> int:
        """
        Elimina registros duplicados del dataset.
        
        Returns:
            Número de duplicados eliminados
        """
        registros_unicos = []
        duplicados = 0
        
        for registro in self._dataset.obtener_registros():
            if registro not in registros_unicos:
                registros_unicos.append(registro)
            else:
                duplicados += 1
        
        # Limpiar y volver a llenar el dataset
        self._dataset.limpiar()
        self._dataset.agregar_registros(registros_unicos)
        
        if duplicados > 0:
            print(f"✓ Se eliminaron {duplicados} registros duplicados")
        
        return duplicados
    
    def eliminar_registros_vacios(self) -> int:
        """
        Elimina registros que no tienen ningún dato válido.
        
        Returns:
            Número de registros vacíos eliminados
        """
        registros_validos = []
        eliminados = 0
        
        for registro in self._dataset.obtener_registros():
            if registro.es_valido():
                # Verificar que al menos un campo no esté vacío
                tiene_datos = False
                for campo, valor in registro.obtener_todos_campos().items():
                    if valor is not None and valor != '' and valor != 'NULL':
                        tiene_datos = True
                        break
                
                if tiene_datos:
                    registros_validos.append(registro)
                else:
                    eliminados += 1
            else:
                eliminados += 1
        
        # Actualizar dataset
        self._dataset.limpiar()
        self._dataset.agregar_registros(registros_validos)
        
        if eliminados > 0:
            print(f"✓ Se eliminaron {eliminados} registros vacíos")
        
        return eliminados
    
    def limpiar_valores_nulos(self, campos: list = None, valor_reemplazo: str = "0") -> int:
        """
        Reemplaza valores nulos/vacíos con un valor por defecto.
        
        Args:
            campos: Lista de campos a limpiar (None = todos)
            valor_reemplazo: Valor con el que reemplazar nulos
            
        Returns:
            Número de valores nulos reemplazados
        """
        reemplazos = 0
        
        for registro in self._dataset.obtener_registros():
            datos = registro.obtener_todos_campos()
            
            # Determinar qué campos limpiar
            campos_a_limpiar = campos if campos else datos.keys()
            
            for campo in campos_a_limpiar:
                if campo in datos:
                    valor = datos[campo]
                    if valor is None or valor == '' or valor == 'NULL':
                        registro.establecer_campo(campo, valor_reemplazo)
                        reemplazos += 1
        
        if reemplazos > 0:
            print(f"✓ Se reemplazaron {reemplazos} valores nulos")
        
        return reemplazos
    
    def normalizar_texto(self, campos: list = None, mayusculas: bool = False) -> int:
        """
        Normaliza campos de texto (elimina espacios extra, unifica mayúsculas/minúsculas).
        
        Args:
            campos: Lista de campos a normalizar (None = todos los que sean texto)
            mayusculas: Si True, convierte a mayúsculas; si False, a minúsculas
            
        Returns:
            Número de campos normalizados
        """
        normalizados = 0
        
        for registro in self._dataset.obtener_registros():
            datos = registro.obtener_todos_campos()
            
            # Determinar qué campos normalizar
            campos_a_normalizar = campos if campos else datos.keys()
            
            for campo in campos_a_normalizar:
                if campo in datos:
                    valor = datos[campo]
                    if isinstance(valor, str):
                        # Eliminar espacios extra
                        valor_limpio = ' '.join(valor.split())
                        
                        # Convertir a mayúsculas o minúsculas
                        if mayusculas:
                            valor_limpio = valor_limpio.upper()
                        else:
                            valor_limpio = valor_limpio.lower()
                        
                        if valor != valor_limpio:
                            registro.establecer_campo(campo, valor_limpio)
                            normalizados += 1
        
        if normalizados > 0:
            print(f"✓ Se normalizaron {normalizados} valores de texto")
        
        return normalizados
    
    def validar_tipos_numericos(self, campos: list) -> dict:
        """
        Valida que los campos especificados contengan valores numéricos.
        
        Args:
            campos: Lista de campos que deben ser numéricos
            
        Returns:
            Diccionario con estadísticas de validación
        """
        resultado = {
            'total_registros': self._dataset.cantidad_registros(),
            'campos_validados': len(campos),
            'errores_por_campo': {}
        }
        
        for campo in campos:
            errores = 0
            for registro in self._dataset.obtener_registros():
                valor = registro.obtener_campo(campo)
                if valor is not None and valor != '':
                    try:
                        # Intentar convertir a float
                        float(valor)
                    except ValueError:
                        errores += 1
            
            resultado['errores_por_campo'][campo] = errores
        
        return resultado
    
    def limpiar_completo(self) -> dict:
        """
        Ejecuta un proceso completo de limpieza de datos.
        
        Realiza las siguientes operaciones:
        1. Elimina registros duplicados
        2. Elimina registros completamente vacíos
        3. Normaliza campos de texto
        
        Returns:
            Diccionario con estadísticas de la limpieza
        """
        print("\n" + "="*50)
        print("INICIANDO LIMPIEZA DE DATOS")
        print("="*50)
        
        duplicados = self.eliminar_duplicados()
        vacios = self.eliminar_registros_vacios()
        
        print(f"\n✓ Limpieza completada")
        print(f"  - Registros duplicados eliminados: {duplicados}")
        print(f"  - Registros vacíos eliminados: {vacios}")
        print(f"  - Total de registros restantes: {self._dataset.cantidad_registros()}")
        
        return {
            'duplicados_eliminados': duplicados,
            'vacios_eliminados': vacios,
            'registros_finales': self._dataset.cantidad_registros()
        }
    
    def obtener_reporte_calidad(self) -> dict:
        """
        Genera un reporte de calidad de los datos.
        
        Returns:
            Diccionario con métricas de calidad
        """
        total_registros = self._dataset.cantidad_registros()
        if total_registros == 0:
            return {'error': 'Dataset vacío'}
        
        campos = self._dataset.obtener_campos()
        reporte = {
            'total_registros': total_registros,
            'total_campos': len(campos),
            'campos_con_nulos': {},
            'porcentaje_completitud': {}
        }
        
        for campo in campos:
            nulos = 0
            for registro in self._dataset.obtener_registros():
                valor = registro.obtener_campo(campo)
                if valor is None or valor == '' or valor == 'NULL':
                    nulos += 1
            
            reporte['campos_con_nulos'][campo] = nulos
            completitud = ((total_registros - nulos) / total_registros) * 100
            reporte['porcentaje_completitud'][campo] = round(completitud, 2)
        
        return reporte
