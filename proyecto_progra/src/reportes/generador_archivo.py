"""
Módulo: generador_archivo.py
Descripción: Implementa generador de reportes para archivos (TXT, JSON, XML)
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.reportes.generador_base import GeneradorReporteBase


class GeneradorReporteArchivo(GeneradorReporteBase):
    """
    Generador de reportes para archivos.
    
    Puede exportar reportes en formatos TXT, JSON y XML.
    Todos los archivos JSON y XML se guardan en la carpeta /data
    
    Hereda de GeneradorReporteBase.
    """
    
    def __init__(self, titulo: str = "Reporte", formato: str = "txt"):
        """
        Inicializa el generador de reportes para archivo.
        
        Args:
            titulo: Título del reporte
            formato: Formato del archivo ('txt', 'json', 'xml')
        """
        super().__init__(titulo)
        self._formato = formato.lower()
        self._ruta_salida = None
    
    def generar(self, nombre_archivo: str = None) -> str:
        """
        Genera y guarda el reporte en un archivo.
        
        Args:
            nombre_archivo: Nombre del archivo (sin extensión)
            
        Returns:
            Ruta del archivo generado
        """
        # Generar nombre de archivo si no se proporciona
        if nombre_archivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_{timestamp}"
        
        # Determinar ruta de salida en la carpeta data
        ruta_data = Path(__file__).parent.parent.parent / "data"
        ruta_data.mkdir(exist_ok=True)  # Crear carpeta si no existe
        
        # Agregar extensión según formato
        archivo_completo = f"{nombre_archivo}.{self._formato}"
        self._ruta_salida = ruta_data / archivo_completo
        
        # Generar según el formato
        if self._formato == 'txt':
            self._generar_txt()
        elif self._formato == 'json':
            self._generar_json()
        elif self._formato == 'xml':
            self._generar_xml()
        else:
            raise ValueError(f"Formato no soportado: {self._formato}")
        
        print(f"\n✓ Reporte generado: {self._ruta_salida}")
        return str(self._ruta_salida)
    
    def _generar_txt(self) -> None:
        """
        Genera reporte en formato TXT.
        """
        with open(self._ruta_salida, 'w', encoding='utf-8') as archivo:
            # Encabezado
            archivo.write(self._crear_linea_separadora(60, "=") + "\n")
            archivo.write(f"{self._titulo.upper():^60}\n")
            archivo.write(f"{'Generado: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^60}\n")
            archivo.write(self._crear_linea_separadora(60, "=") + "\n\n")
            
            # Contenido
            if not self._datos:
                archivo.write("No hay datos para mostrar\n")
            else:
                self._escribir_datos_txt(archivo, self._datos)
            
            archivo.write("\n" + self._crear_linea_separadora(60, "=") + "\n")
    
    def _escribir_datos_txt(self, archivo, datos: dict, nivel: int = 0) -> None:
        """
        Escribe datos en formato texto de forma recursiva.
        
        Args:
            archivo: Handle del archivo
            datos: Datos a escribir
            nivel: Nivel de indentación
        """
        indentacion = "  " * nivel
        
        for clave, valor in datos.items():
            if isinstance(valor, dict):
                archivo.write(f"\n{indentacion}{clave.upper().replace('_', ' ')}:\n")
                self._escribir_datos_txt(archivo, valor, nivel + 1)
            elif isinstance(valor, list):
                archivo.write(f"\n{indentacion}{clave.upper().replace('_', ' ')}:\n")
                self._escribir_lista_txt(archivo, valor, nivel + 1)
            else:
                clave_formateada = clave.replace('_', ' ').title()
                
                if isinstance(valor, (int, float)):
                    valor_formateado = self._formatear_numero(valor)
                else:
                    valor_formateado = str(valor)
                
                archivo.write(f"{indentacion}  • {clave_formateada}: {valor_formateado}\n")
    
    def _escribir_lista_txt(self, archivo, lista: list, nivel: int = 0) -> None:
        """
        Escribe una lista en formato texto.
        
        Args:
            archivo: Handle del archivo
            lista: Lista a escribir
            nivel: Nivel de indentación
        """
        indentacion = "  " * nivel
        
        for i, elemento in enumerate(lista, 1):
            if isinstance(elemento, (tuple, list)) and len(elemento) == 2:
                clave, valor = elemento
                if isinstance(valor, (int, float)):
                    valor_formateado = self._formatear_numero(valor)
                else:
                    valor_formateado = str(valor)
                archivo.write(f"{indentacion}  {i}. {clave}: {valor_formateado}\n")
            elif isinstance(elemento, dict):
                archivo.write(f"{indentacion}  {i}.\n")
                self._escribir_datos_txt(archivo, elemento, nivel + 1)
            else:
                archivo.write(f"{indentacion}  {i}. {elemento}\n")
    
    def _generar_json(self) -> None:
        """
        Genera reporte en formato JSON.
        """
        reporte_completo = {
            'titulo': self._titulo,
            'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'datos': self._datos
        }
        
        with open(self._ruta_salida, 'w', encoding='utf-8') as archivo:
            json.dump(reporte_completo, archivo, indent=2, ensure_ascii=False)
    
    def _generar_xml(self) -> None:
        """
        Genera reporte en formato XML.
        """
        with open(self._ruta_salida, 'w', encoding='utf-8') as archivo:
            # Cabecera XML
            archivo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            archivo.write('<reporte>\n')
            archivo.write(f'  <titulo>{self._escapar_xml(self._titulo)}</titulo>\n')
            archivo.write(f'  <fecha_generacion>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</fecha_generacion>\n')
            archivo.write('  <datos>\n')
            
            # Contenido
            if self._datos:
                self._escribir_datos_xml(archivo, self._datos, nivel=2)
            
            archivo.write('  </datos>\n')
            archivo.write('</reporte>\n')
    
    def _escribir_datos_xml(self, archivo, datos: dict, nivel: int = 1) -> None:
        """
        Escribe datos en formato XML de forma recursiva.
        
        Args:
            archivo: Handle del archivo
            datos: Datos a escribir
            nivel: Nivel de indentación
        """
        indentacion = "  " * nivel
        
        for clave, valor in datos.items():
            # Limpiar nombre de etiqueta
            etiqueta = clave.replace(' ', '_').replace('-', '_').lower()
            
            if isinstance(valor, dict):
                archivo.write(f"{indentacion}<{etiqueta}>\n")
                self._escribir_datos_xml(archivo, valor, nivel + 1)
                archivo.write(f"{indentacion}</{etiqueta}>\n")
            elif isinstance(valor, list):
                archivo.write(f"{indentacion}<{etiqueta}>\n")
                self._escribir_lista_xml(archivo, valor, nivel + 1)
                archivo.write(f"{indentacion}</{etiqueta}>\n")
            else:
                valor_escapado = self._escapar_xml(str(valor))
                archivo.write(f"{indentacion}<{etiqueta}>{valor_escapado}</{etiqueta}>\n")
    
    def _escribir_lista_xml(self, archivo, lista: list, nivel: int = 1) -> None:
        """
        Escribe una lista en formato XML.
        
        Args:
            archivo: Handle del archivo
            lista: Lista a escribir
            nivel: Nivel de indentación
        """
        indentacion = "  " * nivel
        
        for i, elemento in enumerate(lista):
            if isinstance(elemento, (tuple, list)) and len(elemento) == 2:
                clave, valor = elemento
                etiqueta_clave = str(clave).replace(' ', '_').replace('-', '_').lower()
                valor_escapado = self._escapar_xml(str(valor))
                archivo.write(f"{indentacion}<item>\n")
                archivo.write(f"{indentacion}  <clave>{self._escapar_xml(str(clave))}</clave>\n")
                archivo.write(f"{indentacion}  <valor>{valor_escapado}</valor>\n")
                archivo.write(f"{indentacion}</item>\n")
            elif isinstance(elemento, dict):
                archivo.write(f"{indentacion}<item>\n")
                self._escribir_datos_xml(archivo, elemento, nivel + 1)
                archivo.write(f"{indentacion}</item>\n")
            else:
                archivo.write(f"{indentacion}<item>{self._escapar_xml(str(elemento))}</item>\n")
    
    def _escapar_xml(self, texto: str) -> str:
        """
        Escapa caracteres especiales para XML.
        
        Args:
            texto: Texto a escapar
            
        Returns:
            Texto escapado
        """
        texto = str(texto)
        texto = texto.replace('&', '&amp;')
        texto = texto.replace('<', '&lt;')
        texto = texto.replace('>', '&gt;')
        texto = texto.replace('"', '&quot;')
        texto = texto.replace("'", '&apos;')
        return texto
    
    def obtener_ruta_salida(self) -> str:
        """
        Obtiene la ruta del archivo generado.
        
        Returns:
            Ruta del archivo
        """
        return str(self._ruta_salida) if self._ruta_salida else None
