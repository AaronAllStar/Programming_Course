"""
Módulo que define la clase Torre (Rook).
"""

from .pieza import Pieza


class Torre(Pieza):
    """
    Clase que representa una Torre en el ajedrez.
    
    La Torre se mueve horizontal o verticalmente cualquier número de casillas.
    """
    
    def listar_movimientos_posibles(self, posicion):
        """
        Lista todos los movimientos posibles de la Torre desde una posición dada.
        
        Args:
            posicion (str): Posición actual en notación de ajedrez (ej: 'a1')
            
        Returns:
            list: Lista de posiciones válidas
        """
        coordenadas = self.posicion_a_coordenadas(posicion)
        if coordenadas is None:
            return []
        
        col, fila = coordenadas
        movimientos = []
        
        # Movimientos horizontales (misma fila, diferentes columnas)
        for nueva_col in range(8):
            if nueva_col != col:
                nueva_pos = self.coordenadas_a_posicion(nueva_col, fila)
                if nueva_pos:
                    movimientos.append(nueva_pos)
        
        # Movimientos verticales (misma columna, diferentes filas)
        for nueva_fila in range(8):
            if nueva_fila != fila:
                nueva_pos = self.coordenadas_a_posicion(col, nueva_fila)
                if nueva_pos:
                    movimientos.append(nueva_pos)
        
        return movimientos
    
    def es_movimiento_valido(self, posicion_actual, posicion_destino):
        """
        Verifica si un movimiento de la Torre es válido.
        
        Args:
            posicion_actual (str): Posición de origen
            posicion_destino (str): Posición destino
            
        Returns:
            bool: True si el movimiento es válido, False en caso contrario
        """
        movimientos_posibles = self.listar_movimientos_posibles(posicion_actual)
        return posicion_destino in movimientos_posibles
