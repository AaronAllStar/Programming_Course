"""
Módulo: analizador_ventas.py
Descripción: Implementa análisis específicos para datos de ventas
"""

import sys
import os
from collections import defaultdict

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.analizadores.analizador_base import AnalizadorBase
from src.modelos.dataset import Dataset


class AnalizadorVentas(AnalizadorBase):
    """
    Analizador específico para datos de ventas.
    
    Realiza análisis de negocio como ventas por región, por producto,
    vendedores top, tendencias, etc.
    
    Hereda de AnalizadorBase e implementa análisis de ventas.
    """
    
    def __init__(self, dataset: Dataset):
        """
        Inicializa el analizador de ventas.
        
        Args:
            dataset: Dataset de ventas a analizar
        """
        super().__init__(dataset)
    
    def analizar(self) -> dict:
        """
        Realiza análisis completo de ventas.
        
        Returns:
            Diccionario con análisis de ventas
        """
        print("\n" + "="*50)
        print("ANÁLISIS DE VENTAS")
        print("="*50)
        
        resultados = {
            'total_registros': self._dataset.cantidad_registros(),
            'ventas_totales': 0,
            'por_region': {},
            'por_producto': {},
            'por_categoria': {},
            'por_vendedor': {},
            'top_productos': [],
            'top_vendedores': []
        }
        
        if self._dataset.esta_vacio():
            print("⚠ El dataset está vacío")
            return resultados
        
        # Calcular ventas totales y por categorías
        resultados['ventas_totales'] = self._calcular_ventas_totales()
        resultados['por_region'] = self._analizar_por_campo('region', 'total')
        resultados['por_producto'] = self._analizar_por_campo('producto', 'total')
        resultados['por_categoria'] = self._analizar_por_campo('categoria', 'total')
        resultados['por_vendedor'] = self._analizar_por_campo('vendedor', 'total')
        
        # Obtener tops
        resultados['top_productos'] = self._obtener_top_n('producto', 'total', 5)
        resultados['top_vendedores'] = self._obtener_top_n('vendedor', 'total', 5)
        
        # Guardar resultados
        self._guardar_resultados(resultados)
        
        print(f"\n✓ Análisis de ventas completado")
        print(f"  - Total de ventas: ${resultados['ventas_totales']:,.2f}")
        print(f"  - Regiones analizadas: {len(resultados['por_region'])}")
        print(f"  - Productos analizados: {len(resultados['por_producto'])}")
        
        return resultados
    
    def _calcular_ventas_totales(self) -> float:
        """
        Calcula el total de ventas en el dataset.
        
        Returns:
            Suma total de ventas
        """
        total = 0
        for registro in self._dataset.obtener_registros():
            valor_total = registro.obtener_campo('total')
            if valor_total:
                try:
                    total += float(valor_total)
                except ValueError:
                    pass
        return round(total, 2)
    
    def _analizar_por_campo(self, campo_agrupacion: str, campo_suma: str) -> dict:
        """
        Agrupa y suma ventas por un campo específico.
        
        Args:
            campo_agrupacion: Campo por el que agrupar
            campo_suma: Campo numérico a sumar
            
        Returns:
            Diccionario con totales por grupo
        """
        agrupacion = defaultdict(float)
        
        for registro in self._dataset.obtener_registros():
            clave = registro.obtener_campo(campo_agrupacion)
            valor = registro.obtener_campo(campo_suma)
            
            if clave and valor:
                try:
                    agrupacion[str(clave)] += float(valor)
                except ValueError:
                    pass
        
        # Redondear valores
        return {k: round(v, 2) for k, v in agrupacion.items()}
    
    def _obtener_top_n(self, campo_agrupacion: str, campo_suma: str, n: int = 5) -> list:
        """
        Obtiene los top N elementos según ventas.
        
        Args:
            campo_agrupacion: Campo por el que agrupar
            campo_suma: Campo numérico a sumar
            n: Cantidad de elementos top a retornar
            
        Returns:
            Lista de tuplas (elemento, total) ordenadas por total
        """
        agrupacion = self._analizar_por_campo(campo_agrupacion, campo_suma)
        
        # Ordenar por valor descendente
        ordenados = sorted(agrupacion.items(), key=lambda x: x[1], reverse=True)
        
        # Retornar top N
        return ordenados[:n]
    
    def analizar_producto_especifico(self, nombre_producto: str) -> dict:
        """
        Analiza las ventas de un producto específico.
        
        Args:
            nombre_producto: Nombre del producto a analizar
            
        Returns:
            Diccionario con análisis del producto
        """
        analisis = {
            'producto': nombre_producto,
            'cantidad_ventas': 0,
            'total_vendido': 0,
            'promedio_por_venta': 0,
            'por_region': {}
        }
        
        cantidad_ventas = 0
        total_vendido = 0
        ventas_por_region = defaultdict(float)
        
        for registro in self._dataset.obtener_registros():
            producto = registro.obtener_campo('producto')
            
            if producto and str(producto).lower() == nombre_producto.lower():
                cantidad_ventas += 1
                
                # Sumar total
                total = registro.obtener_campo('total')
                if total:
                    try:
                        valor = float(total)
                        total_vendido += valor
                        
                        # Acumular por región
                        region = registro.obtener_campo('region')
                        if region:
                            ventas_por_region[str(region)] += valor
                    except ValueError:
                        pass
        
        analisis['cantidad_ventas'] = cantidad_ventas
        analisis['total_vendido'] = round(total_vendido, 2)
        analisis['promedio_por_venta'] = round(total_vendido / cantidad_ventas, 2) if cantidad_ventas > 0 else 0
        analisis['por_region'] = {k: round(v, 2) for k, v in ventas_por_region.items()}
        
        return analisis
    
    def comparar_periodos(self, campo_fecha: str = 'fecha') -> dict:
        """
        Compara ventas entre diferentes periodos (si hay campo de fecha).
        
        Args:
            campo_fecha: Nombre del campo que contiene la fecha
            
        Returns:
            Diccionario con comparación de periodos
        """
        # Esta es una versión simplificada que agrupa por fecha
        ventas_por_fecha = self._analizar_por_campo(campo_fecha, 'total')
        
        return {
            'ventas_por_periodo': ventas_por_fecha,
            'total_periodos': len(ventas_por_fecha)
        }
