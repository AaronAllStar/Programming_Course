"""
Módulo: generador_consola.py
Descripción: Implementa generador de reportes para consola
"""

import sys
import os

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.reportes.generador_base import GeneradorReporteBase


class GeneradorReporteConsola(GeneradorReporteBase):
    """
    Generador de reportes para visualización en consola.
    
    Formatea los datos y los presenta de forma legible en la consola.
    Hereda de GeneradorReporteBase.
    """
    
    def __init__(self, titulo: str = "Reporte"):
        """
        Inicializa el generador de reportes para consola.
        
        Args:
            titulo: Título del reporte
        """
        super().__init__(titulo)
    
    def generar(self) -> None:
        """
        Genera y muestra el reporte en consola.
        """
        print("\n" + self._crear_linea_separadora(60, "="))
        print(f"{self._titulo.upper():^60}")
        print(self._crear_linea_separadora(60, "="))
        
        if not self._datos:
            print("\n⚠ No hay datos para mostrar")
            return
        
        self._imprimir_datos(self._datos)
        print("\n" + self._crear_linea_separadora(60, "="))
    
    def _imprimir_datos(self, datos: dict, nivel: int = 0) -> None:
        """
        Imprime datos de forma recursiva y formateada.
        
        Args:
            datos: Diccionario con los datos a imprimir
            nivel: Nivel de indentación (para datos anidados)
        """
        indentacion = "  " * nivel
        
        for clave, valor in datos.items():
            if isinstance(valor, dict):
                # Si es un diccionario, imprimir clave y recursión
                print(f"\n{indentacion}{clave.upper().replace('_', ' ')}:")
                self._imprimir_datos(valor, nivel + 1)
            elif isinstance(valor, list):
                # Si es una lista, imprimir cada elemento
                print(f"\n{indentacion}{clave.upper().replace('_', ' ')}:")
                self._imprimir_lista(valor, nivel + 1)
            else:
                # Valor simple
                clave_formateada = clave.replace('_', ' ').title()
                
                # Formatear valores numéricos
                if isinstance(valor, (int, float)):
                    valor_formateado = self._formatear_numero(valor)
                else:
                    valor_formateado = str(valor)
                
                print(f"{indentacion}  • {clave_formateada}: {valor_formateado}")
    
    def _imprimir_lista(self, lista: list, nivel: int = 0) -> None:
        """
        Imprime una lista de forma formateada.
        
        Args:
            lista: Lista a imprimir
            nivel: Nivel de indentación
        """
        indentacion = "  " * nivel
        
        if not lista:
            print(f"{indentacion}  (vacío)")
            return
        
        for i, elemento in enumerate(lista, 1):
            if isinstance(elemento, (tuple, list)) and len(elemento) == 2:
                # Formato para tuplas (clave, valor)
                clave, valor = elemento
                if isinstance(valor, (int, float)):
                    valor_formateado = self._formatear_numero(valor)
                else:
                    valor_formateado = str(valor)
                print(f"{indentacion}  {i}. {clave}: {valor_formateado}")
            elif isinstance(elemento, dict):
                # Formato para diccionarios
                print(f"{indentacion}  {i}.")
                self._imprimir_datos(elemento, nivel + 1)
            else:
                # Elemento simple
                print(f"{indentacion}  {i}. {elemento}")
    
    def generar_tabla(self, datos: list, columnas: list = None) -> None:
        """
        Genera una tabla formateada en consola.
        
        Args:
            datos: Lista de diccionarios con los datos
            columnas: Lista de columnas a mostrar (None = todas)
        """
        if not datos:
            print("\n⚠ No hay datos para mostrar en la tabla")
            return
        
        # Determinar columnas
        if columnas is None:
            columnas = list(datos[0].keys()) if datos else []
        
        # Calcular anchos de columnas
        anchos = {}
        for col in columnas:
            ancho_max = len(str(col))
            for fila in datos:
                valor = str(fila.get(col, ''))
                ancho_max = max(ancho_max, len(valor))
            anchos[col] = min(ancho_max + 2, 30)  # Máximo 30 caracteres
        
        # Imprimir encabezados
        print("\n" + self._crear_linea_separadora(60, "-"))
        encabezado = " | ".join(str(col).ljust(anchos[col]) for col in columnas)
        print(encabezado)
        print(self._crear_linea_separadora(60, "-"))
        
        # Imprimir filas
        for fila in datos[:20]:  # Limitar a 20 filas
            fila_texto = " | ".join(
                str(fila.get(col, '')).ljust(anchos[col])[:anchos[col]] 
                for col in columnas
            )
            print(fila_texto)
        
        if len(datos) > 20:
            print(f"\n... y {len(datos) - 20} filas más")
        
        print(self._crear_linea_separadora(60, "-"))
