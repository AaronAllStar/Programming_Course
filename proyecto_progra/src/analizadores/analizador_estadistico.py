"""
Módulo: analizador_estadistico.py
Descripción: Implementa análisis estadísticos generales
"""

import sys
import os
import statistics

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.analizadores.analizador_base import AnalizadorBase
from src.modelos.dataset import Dataset


class AnalizadorEstadistico(AnalizadorBase):
    """
    Analizador de estadísticas descriptivas generales.
    
    Calcula medidas estadísticas como media, mediana, moda, desviación estándar,
    valores máximos y mínimos para campos numéricos.
    
    Hereda de AnalizadorBase e implementa análisis estadísticos.
    """
    
    def __init__(self, dataset: Dataset):
        """
        Inicializa el analizador estadístico.
        
        Args:
            dataset: Dataset a analizar
        """
        super().__init__(dataset)
    
    def analizar(self) -> dict:
        """
        Realiza análisis estadístico completo del dataset.
        
        Returns:
            Diccionario con estadísticas por campo numérico
        """
        print("\n" + "="*50)
        print("ANÁLISIS ESTADÍSTICO")
        print("="*50)
        
        resultados = {
            'total_registros': self._dataset.cantidad_registros(),
            'campos': {},
            'resumen_general': {}
        }
        
        if self._dataset.esta_vacio():
            print("⚠ El dataset está vacío")
            return resultados
        
        # Obtener todos los campos
        campos = self._dataset.obtener_campos()
        
        # Analizar cada campo
        for campo in campos:
            estadisticas = self._analizar_campo(campo)
            if estadisticas:
                resultados['campos'][campo] = estadisticas
        
        # Guardar resultados internamente
        self._guardar_resultados(resultados)
        
        print(f"\n✓ Análisis completado para {len(resultados['campos'])} campos")
        
        return resultados
    
    def _analizar_campo(self, nombre_campo: str) -> dict:
        """
        Analiza un campo específico del dataset.
        
        Args:
            nombre_campo: Nombre del campo a analizar
            
        Returns:
            Diccionario con estadísticas del campo
        """
        valores = self._dataset.obtener_valores_campo(nombre_campo)
        
        if not valores:
            return None
        
        # Intentar análisis numérico
        valores_numericos = []
        for valor in valores:
            try:
                valores_numericos.append(float(valor))
            except (ValueError, TypeError):
                pass
        
        # Si hay suficientes valores numéricos, hacer análisis estadístico
        if len(valores_numericos) >= 2:
            return self._estadisticas_numericas(valores_numericos)
        else:
            # Análisis de texto/categórico
            return self._estadisticas_categoricas(valores)
    
    def _estadisticas_numericas(self, valores: list) -> dict:
        """
        Calcula estadísticas para valores numéricos.
        
        Args:
            valores: Lista de valores numéricos
            
        Returns:
            Diccionario con estadísticas
        """
        estadisticas = {
            'tipo': 'numérico',
            'total_valores': len(valores),
            'suma': round(sum(valores), 2),
            'promedio': round(statistics.mean(valores), 2),
            'mediana': round(statistics.median(valores), 2),
            'minimo': round(min(valores), 2),
            'maximo': round(max(valores), 2),
        }
        
        # Calcular desviación estándar si hay más de 1 valor
        if len(valores) > 1:
            estadisticas['desviacion_estandar'] = round(statistics.stdev(valores), 2)
            estadisticas['varianza'] = round(statistics.variance(valores), 2)
        
        # Calcular moda si es posible
        try:
            estadisticas['moda'] = round(statistics.mode(valores), 2)
        except statistics.StatisticsError:
            # No hay moda única
            estadisticas['moda'] = None
        
        return estadisticas
    
    def _estadisticas_categoricas(self, valores: list) -> dict:
        """
        Calcula estadísticas para valores categóricos/texto.
        
        Args:
            valores: Lista de valores
            
        Returns:
            Diccionario con estadísticas
        """
        # Contar frecuencias
        frecuencias = {}
        for valor in valores:
            valor_str = str(valor)
            frecuencias[valor_str] = frecuencias.get(valor_str, 0) + 1
        
        # Encontrar el valor más común
        valor_mas_comun = max(frecuencias, key=frecuencias.get) if frecuencias else None
        
        estadisticas = {
            'tipo': 'categórico',
            'total_valores': len(valores),
            'valores_unicos': len(set(valores)),
            'valor_mas_comun': valor_mas_comun,
            'frecuencia_mas_comun': frecuencias.get(valor_mas_comun, 0) if valor_mas_comun else 0,
            'distribucion': frecuencias
        }
        
        return estadisticas
    
    def obtener_resumen_campo(self, nombre_campo: str) -> dict:
        """
        Obtiene un resumen estadístico de un campo específico.
        
        Args:
            nombre_campo: Nombre del campo
            
        Returns:
            Diccionario con estadísticas del campo
        """
        if not self._resultados:
            self.analizar()
        
        return self._resultados.get('campos', {}).get(nombre_campo, {})
    
    def obtener_campos_numericos(self) -> list:
        """
        Obtiene la lista de campos que son numéricos.
        
        Returns:
            Lista de nombres de campos numéricos
        """
        if not self._resultados:
            self.analizar()
        
        campos_numericos = []
        for campo, stats in self._resultados.get('campos', {}).items():
            if stats.get('tipo') == 'numérico':
                campos_numericos.append(campo)
        
        return campos_numericos
