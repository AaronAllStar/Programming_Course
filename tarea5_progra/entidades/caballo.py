"""
Módulo que define la clase Caballo (Knight).
"""

from .pieza import Pieza


class Caballo(Pieza):
    """
    Clase que representa un Caballo en el ajedrez.
    
    El Caballo se mueve en forma de 'L': 2 casillas en una dirección y 1 en perpendicular.
    """
    
    def listar_movimientos_posibles(self, posicion):
        """
        Lista todos los movimientos posibles del Caballo desde una posición dada.
        
        Args:
            posicion (str): Posición actual en notación de ajedrez (ej: 'e4')
            
        Returns:
            list: Lista de posiciones válidas
        """
        coordenadas = self.posicion_a_coordenadas(posicion)
        if coordenadas is None:
            return []
        
        col, fila = coordenadas
        movimientos = []
        
        # Los 8 movimientos posibles del Caballo en forma de 'L'
        movimientos_caballo = [
            (2, 1),   # 2 derecha, 1 arriba
            (2, -1),  # 2 derecha, 1 abajo
            (-2, 1),  # 2 izquierda, 1 arriba
            (-2, -1), # 2 izquierda, 1 abajo
            (1, 2),   # 1 derecha, 2 arriba
            (1, -2),  # 1 derecha, 2 abajo
            (-1, 2),  # 1 izquierda, 2 arriba
            (-1, -2)  # 1 izquierda, 2 abajo
        ]
        
        for dc, df in movimientos_caballo:
            nueva_col = col + dc
            nueva_fila = fila + df
            
            if self.esta_en_tablero(nueva_col, nueva_fila):
                nueva_pos = self.coordenadas_a_posicion(nueva_col, nueva_fila)
                if nueva_pos:
                    movimientos.append(nueva_pos)
        
        return movimientos
    
    def es_movimiento_valido(self, posicion_actual, posicion_destino):
        """
        Verifica si un movimiento del Caballo es válido.
        
        Args:
            posicion_actual (str): Posición de origen
            posicion_destino (str): Posición destino
            
        Returns:
            bool: True si el movimiento es válido, False en caso contrario
        """
        movimientos_posibles = self.listar_movimientos_posibles(posicion_actual)
        return posicion_destino in movimientos_posibles
