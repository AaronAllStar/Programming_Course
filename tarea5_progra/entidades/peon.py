"""
Módulo que define la clase Peon (Pawn).
"""

from .pieza import Pieza


class Peon(Pieza):
    """
    Clase que representa un Peón en el ajedrez.
    
    El Peón se mueve hacia adelante (aumenta la fila):
    - 1 casilla hacia adelante desde cualquier posición
    - 2 casillas hacia adelante desde la fila inicial (fila 2)
    
    Nota: Esta es una versión simplificada que no incluye capturas diagonales.
    """
    
    def listar_movimientos_posibles(self, posicion):
        """
        Lista todos los movimientos posibles del Peón desde una posición dada.
        
        Args:
            posicion (str): Posición actual en notación de ajedrez (ej: 'e2')
            
        Returns:
            list: Lista de posiciones válidas
        """
        coordenadas = self.posicion_a_coordenadas(posicion)
        if coordenadas is None:
            return []
        
        col, fila = coordenadas
        movimientos = []
        
        # Movimiento de 1 casilla hacia adelante
        nueva_fila = fila + 1
        if self.esta_en_tablero(col, nueva_fila):
            nueva_pos = self.coordenadas_a_posicion(col, nueva_fila)
            if nueva_pos:
                movimientos.append(nueva_pos)
        
        # Movimiento de 2 casillas desde la posición inicial (fila 2 = índice 1)
        if fila == 1:  # Peón en su posición inicial (fila 2)
            nueva_fila = fila + 2
            if self.esta_en_tablero(col, nueva_fila):
                nueva_pos = self.coordenadas_a_posicion(col, nueva_fila)
                if nueva_pos:
                    movimientos.append(nueva_pos)
        
        return movimientos
    
    def es_movimiento_valido(self, posicion_actual, posicion_destino):
        """
        Verifica si un movimiento del Peón es válido.
        
        Args:
            posicion_actual (str): Posición de origen
            posicion_destino (str): Posición destino
            
        Returns:
            bool: True si el movimiento es válido, False en caso contrario
        """
        movimientos_posibles = self.listar_movimientos_posibles(posicion_actual)
        return posicion_destino in movimientos_posibles
