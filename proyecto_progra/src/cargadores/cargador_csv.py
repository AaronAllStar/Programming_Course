"""
Módulo: cargador_csv.py
Descripción: Implementa el cargador de archivos CSV
"""

import csv
import sys
import os

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.cargadores.cargador_base import CargadorBase
from src.modelos.dataset import Dataset
from src.modelos.registro import Registro


class CargadorCSV(CargadorBase):
    """
    Cargador de archivos CSV.
    
    Implementa la interfaz CargadorBase para leer archivos en formato CSV.
    Hereda de CargadorBase y proporciona implementación específica.
    
    Atributos:
        delimitador (str): Carácter delimitador del CSV (por defecto ',')
        encoding (str): Codificación del archivo (por defecto 'utf-8')
    """
    
    def __init__(self, ruta_archivo: str, delimitador: str = ',', encoding: str = 'utf-8'):
        """
        Inicializa el cargador CSV.
        
        Args:
            ruta_archivo: Ruta del archivo CSV
            delimitador: Carácter separador de columnas
            encoding: Codificación del archivo
        """
        super().__init__(ruta_archivo)
        self._delimitador = delimitador
        self._encoding = encoding
    
    def cargar(self) -> Dataset:
        """
        Carga los datos desde el archivo CSV.
        
        Lee el archivo CSV y convierte cada fila en un objeto Registro,
        creando un Dataset completo.
        
        Returns:
            Dataset con los registros cargados
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el archivo está vacío o mal formateado
        """
        # Validar que el archivo existe
        if not self.validar_archivo_existe():
            raise FileNotFoundError(f"El archivo {self._ruta_archivo} no existe")
        
        # Crear dataset para almacenar los datos
        dataset = Dataset(nombre=self._ruta_archivo.stem)
        
        try:
            # Abrir y leer el archivo CSV
            with open(self._ruta_archivo, 'r', encoding=self._encoding, newline='') as archivo:
                # Crear lector CSV
                lector = csv.DictReader(archivo, delimiter=self._delimitador)
                
                # Verificar que hay encabezados
                if lector.fieldnames is None:
                    raise ValueError("El archivo CSV no tiene encabezados")
                
                # Leer cada fila y crear registros
                contador = 0
                for fila in lector:
                    # Convertir la fila en un diccionario limpio
                    datos = {campo: valor.strip() if valor else None 
                            for campo, valor in fila.items()}
                    
                    # Crear registro y agregarlo al dataset
                    registro = Registro(datos)
                    dataset.agregar_registro(registro)
                    contador += 1
                
                # Validar que se cargaron datos
                if contador == 0:
                    raise ValueError("El archivo CSV está vacío")
                
                print(f"✓ Se cargaron {contador} registros exitosamente")
                
        except UnicodeDecodeError:
            # Intentar con otra codificación si falla UTF-8
            try:
                with open(self._ruta_archivo, 'r', encoding='latin-1', newline='') as archivo:
                    lector = csv.DictReader(archivo, delimiter=self._delimitador)
                    contador = 0
                    for fila in lector:
                        datos = {campo: valor.strip() if valor else None 
                                for campo, valor in fila.items()}
                        registro = Registro(datos)
                        dataset.agregar_registro(registro)
                        contador += 1
                    print(f"✓ Se cargaron {contador} registros (codificación latin-1)")
            except Exception as e:
                raise ValueError(f"Error al leer el archivo CSV: {str(e)}")
        
        except Exception as e:
            raise ValueError(f"Error al cargar el archivo CSV: {str(e)}")
        
        return dataset
    
    def obtener_encabezados(self) -> list:
        """
        Obtiene solo los encabezados del archivo CSV sin cargar todos los datos.
        
        Returns:
            Lista con los nombres de las columnas
        """
        if not self.validar_archivo_existe():
            return []
        
        try:
            with open(self._ruta_archivo, 'r', encoding=self._encoding, newline='') as archivo:
                lector = csv.reader(archivo, delimiter=self._delimitador)
                encabezados = next(lector)
                return [encabezado.strip() for encabezado in encabezados]
        except Exception:
            return []
    
    def contar_filas(self) -> int:
        """
        Cuenta el número de filas en el CSV (sin contar encabezados).
        
        Returns:
            Número de filas de datos
        """
        if not self.validar_archivo_existe():
            return 0
        
        try:
            with open(self._ruta_archivo, 'r', encoding=self._encoding, newline='') as archivo:
                lector = csv.reader(archivo, delimiter=self._delimitador)
                next(lector)  # Saltar encabezados
                return sum(1 for _ in lector)
        except Exception:
            return 0
