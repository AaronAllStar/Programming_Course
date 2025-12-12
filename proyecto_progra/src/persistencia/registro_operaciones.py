"""
Módulo: registro_operaciones.py
Descripción: Clase para registrar y persistir operaciones del sistema en una base de datos local
"""

import pickle
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any


class Operacion:
    """
    Clase que representa una operación realizada en el sistema.
    
    Atributos:
        timestamp (str): Fecha y hora de la operación
        dataset (str): Nombre del dataset utilizado
        operacion (str): Tipo de operación realizada
        parametros (dict): Parámetros utilizados en la operación
        resultado (str): Resultado de la operación
    """
    
    def __init__(self, dataset: str, operacion: str, parametros: Dict[str, Any] = None, resultado: str = ""):
        """
        Inicializa una operación.
        
        Args:
            dataset: Nombre del dataset utilizado
            operacion: Tipo de operación realizada
            parametros: Diccionario con los parámetros de la operación
            resultado: Resultado o estado de la operación
        """
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dataset = dataset
        self.operacion = operacion
        self.parametros = parametros if parametros else {}
        self.resultado = resultado
    
    def __str__(self) -> str:
        """
        Representación en string de la operación.
        
        Returns:
            String describiendo la operación
        """
        params_str = ", ".join(f"{k}={v}" for k, v in self.parametros.items()) if self.parametros else "ninguno"
        return (f"[{self.timestamp}] Dataset: {self.dataset} | "
                f"Operación: {self.operacion} | Parámetros: {params_str}")
    
    def to_dict(self) -> dict:
        """
        Convierte la operación a diccionario.
        
        Returns:
            Diccionario con los datos de la operación
        """
        return {
            'timestamp': self.timestamp,
            'dataset': self.dataset,
            'operacion': self.operacion,
            'parametros': self.parametros,
            'resultado': self.resultado
        }


class RegistroOperaciones:
    """
    Clase para gestionar el registro de operaciones en una base de datos local.
    
    Utiliza el módulo pickle para persistir las operaciones en el archivo
    'operaciones.dat' en la carpeta raíz del proyecto.
    
    Atributos:
        ruta_bd (Path): Ruta al archivo de base de datos
        operaciones (list): Lista de operaciones registradas
    """
    
    def __init__(self, ruta_bd: str = None):
        """
        Inicializa el registro de operaciones.
        
        Args:
            ruta_bd: Ruta al archivo de base de datos (por defecto: raíz del proyecto)
        """
        if ruta_bd is None:
            # Por defecto, guardar en la raíz del proyecto
            ruta_proyecto = Path(__file__).parent.parent.parent
            self.ruta_bd = ruta_proyecto / "operaciones.dat"
        else:
            self.ruta_bd = Path(ruta_bd)
        
        # Cargar operaciones existentes
        self.operaciones: List[Operacion] = self._cargar_operaciones()
    
    def _cargar_operaciones(self) -> List[Operacion]:
        """
        Carga las operaciones desde el archivo.
        
        Returns:
            Lista de operaciones cargadas
        """
        if not self.ruta_bd.exists():
            return []
        
        try:
            with open(self.ruta_bd, 'rb') as archivo:
                operaciones = pickle.load(archivo)
                return operaciones
        except (pickle.PickleError, EOFError, FileNotFoundError):
            # Si hay error al cargar, retornar lista vacía
            return []
    
    def _guardar_operaciones(self) -> bool:
        """
        Guarda las operaciones en el archivo.
        
        Returns:
            True si se guardó exitosamente, False en caso contrario
        """
        try:
            with open(self.ruta_bd, 'wb') as archivo:
                pickle.dump(self.operaciones, archivo)
            return True
        except Exception as e:
            print(f"❌ Error al guardar operaciones: {str(e)}")
            return False
    
    def registrar_operacion(self, dataset: str, operacion: str, 
                           parametros: Dict[str, Any] = None, 
                           resultado: str = "Exitoso") -> None:
        """
        Registra una nueva operación en la base de datos.
        
        Args:
            dataset: Nombre del dataset utilizado
            operacion: Tipo de operación realizada
            parametros: Diccionario con los parámetros de la operación
            resultado: Resultado de la operación
        """
        # Crear nueva operación
        nueva_operacion = Operacion(dataset, operacion, parametros, resultado)
        
        # Agregar a la lista
        self.operaciones.append(nueva_operacion)
        
        # Guardar en disco
        if self._guardar_operaciones():
            # Mensaje opcional para debug (comentado en producción)
            # print(f"✓ Operación registrada en BD: {operacion}")
            pass
    
    def obtener_todas_operaciones(self) -> List[Operacion]:
        """
        Obtiene todas las operaciones registradas.
        
        Returns:
            Lista de operaciones
        """
        return self.operaciones.copy()
    
    def obtener_operaciones_por_dataset(self, nombre_dataset: str) -> List[Operacion]:
        """
        Obtiene operaciones filtradas por dataset.
        
        Args:
            nombre_dataset: Nombre del dataset a filtrar
            
        Returns:
            Lista de operaciones del dataset especificado
        """
        return [op for op in self.operaciones if op.dataset == nombre_dataset]
    
    def obtener_operaciones_por_tipo(self, tipo_operacion: str) -> List[Operacion]:
        """
        Obtiene operaciones filtradas por tipo.
        
        Args:
            tipo_operacion: Tipo de operación a filtrar
            
        Returns:
            Lista de operaciones del tipo especificado
        """
        return [op for op in self.operaciones if op.operacion == tipo_operacion]
    
    def obtener_ultimas_n_operaciones(self, n: int = 10) -> List[Operacion]:
        """
        Obtiene las últimas N operaciones.
        
        Args:
            n: Número de operaciones a obtener
            
        Returns:
            Lista con las últimas N operaciones
        """
        return self.operaciones[-n:] if len(self.operaciones) >= n else self.operaciones
    
    def contar_operaciones(self) -> int:
        """
        Cuenta el total de operaciones registradas.
        
        Returns:
            Número de operaciones
        """
        return len(self.operaciones)
    
    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas del registro de operaciones.
        
        Returns:
            Diccionario con estadísticas
        """
        if not self.operaciones:
            return {
                'total_operaciones': 0,
                'datasets_usados': [],
                'tipos_operaciones': {},
                'primera_operacion': None,
                'ultima_operacion': None
            }
        
        # Contar operaciones por tipo
        tipos = {}
        datasets = set()
        
        for op in self.operaciones:
            tipos[op.operacion] = tipos.get(op.operacion, 0) + 1
            datasets.add(op.dataset)
        
        return {
            'total_operaciones': len(self.operaciones),
            'datasets_usados': list(datasets),
            'tipos_operaciones': tipos,
            'primera_operacion': self.operaciones[0].timestamp if self.operaciones else None,
            'ultima_operacion': self.operaciones[-1].timestamp if self.operaciones else None
        }
    
    def limpiar_historial(self) -> bool:
        """
        Elimina todas las operaciones del historial.
        
        Returns:
            True si se limpió exitosamente
        """
        self.operaciones.clear()
        return self._guardar_operaciones()
    
    def exportar_historial_texto(self, ruta_salida: str = None) -> str:
        """
        Exporta el historial de operaciones a un archivo de texto.
        
        Args:
            ruta_salida: Ruta del archivo de salida (opcional)
            
        Returns:
            Ruta del archivo creado
        """
        if ruta_salida is None:
            ruta_proyecto = Path(__file__).parent.parent.parent
            ruta_salida = ruta_proyecto / "data" / "historial_operaciones.txt"
        else:
            ruta_salida = Path(ruta_salida)
        
        # Crear directorio si no existe
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        
        with open(ruta_salida, 'w', encoding='utf-8') as archivo:
            archivo.write("="*70 + "\n")
            archivo.write("HISTORIAL DE OPERACIONES\n")
            archivo.write("="*70 + "\n\n")
            
            if not self.operaciones:
                archivo.write("No hay operaciones registradas.\n")
            else:
                for i, op in enumerate(self.operaciones, 1):
                    archivo.write(f"\n{i}. {op}\n")
                    if op.resultado:
                        archivo.write(f"   Resultado: {op.resultado}\n")
            
            archivo.write("\n" + "="*70 + "\n")
            archivo.write(f"Total de operaciones: {len(self.operaciones)}\n")
        
        return str(ruta_salida)
    
    def obtener_ruta_bd(self) -> str:
        """
        Obtiene la ruta del archivo de base de datos.
        
        Returns:
            Ruta del archivo operaciones.dat
        """
        return str(self.ruta_bd)
