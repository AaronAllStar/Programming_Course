"""
Módulo que define la clase abstracta base Pieza.

Esta clase abstracta define la interfaz común para todas las piezas de ajedrez.
Todas las piezas concretas deben heredar de esta clase e implementar los métodos abstractos.
"""

from abc import ABC, abstractmethod


class Pieza(ABC):
    """
    Clase base abstracta para todas las piezas de ajedrez.
    
    Define los métodos abstractos que todas las piezas deben implementar:
    - listar_movimientos_posibles: retorna todos los movimientos válidos desde una posición
    - es_movimiento_valido: verifica si un movimiento específico es válido
    """
    
    @abstractmethod
    def listar_movimientos_posibles(self, posicion):
        """
        Lista todos los movimientos posibles desde una posición dada.
        
        Args:
            posicion (str): Posición actual en notación de ajedrez (ej: 'e4')
            
        Returns:
            list: Lista de posiciones válidas como strings (ej: ['e5', 'e6', 'f4'])
        """
        pass
    
    @abstractmethod
    def es_movimiento_valido(self, posicion_actual, posicion_destino):
        """
        Verifica si un movimiento desde posicion_actual a posicion_destino es válido.
        
        Args:
            posicion_actual (str): Posición de origen en notación de ajedrez (ej: 'e4')
            posicion_destino (str): Posición destino en notación de ajedrez (ej: 'e5')
            
        Returns:
            bool: True si el movimiento es válido, False en caso contrario
        """
        pass
    
    @staticmethod
    def posicion_a_coordenadas(posicion):
        """
        Convierte una posición en notación de ajedrez a coordenadas numéricas.
        
        Args:
            posicion (str): Posición en notación de ajedrez (ej: 'e4')
            
        Returns:
            tuple: (columna, fila) donde columna es 0-7 y fila es 0-7
            None: si la posición es inválida
        """
        if len(posicion) != 2:
            return None
        
        columna = posicion[0].lower()
        fila = posicion[1]
        
        if columna < 'a' or columna > 'h':
            return None
        if fila < '1' or fila > '8':
            return None
        
        col_num = ord(columna) - ord('a')  # 0-7
        fila_num = int(fila) - 1  # 0-7
        
        return (col_num, fila_num)
    
    @staticmethod
    def coordenadas_a_posicion(columna, fila):
        """
        Convierte coordenadas numéricas a notación de ajedrez.
        
        Args:
            columna (int): Número de columna (0-7)
            fila (int): Número de fila (0-7)
            
        Returns:
            str: Posición en notación de ajedrez (ej: 'e4')
            None: si las coordenadas son inválidas
        """
        if columna < 0 or columna > 7 or fila < 0 or fila > 7:
            return None
        
        col_letra = chr(ord('a') + columna)
        fila_num = str(fila + 1)
        
        return col_letra + fila_num
    
    @staticmethod
    def esta_en_tablero(columna, fila):
        """
        Verifica si las coordenadas están dentro del tablero.
        
        Args:
            columna (int): Número de columna
            fila (int): Número de fila
            
        Returns:
            bool: True si está en el tablero, False en caso contrario
        """
        return 0 <= columna <= 7 and 0 <= fila <= 7
