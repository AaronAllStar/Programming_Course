"""
Módulo que define la clase Rey (King).
"""

from .pieza import Pieza


class Rey(Pieza):
    """
    Clase que representa un Rey en el ajedrez.
    
    El Rey se mueve una casilla en cualquier dirección (horizontal, vertical o diagonal).
    """
    
    def listar_movimientos_posibles(self, posicion):
        """
        Lista todos los movimientos posibles del Rey desde una posición dada.
        
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
        
        # El Rey se mueve una casilla en todas las direcciones
        direcciones = [
            (-1, -1), (-1, 0), (-1, 1),  # arriba-izq, arriba, arriba-der
            (0, -1),           (0, 1),    # izquierda, derecha
            (1, -1),  (1, 0),  (1, 1)     # abajo-izq, abajo, abajo-der
        ]
        
        for dc, df in direcciones:
            nueva_col = col + dc
            nueva_fila = fila + df
            
            if self.esta_en_tablero(nueva_col, nueva_fila):
                nueva_pos = self.coordenadas_a_posicion(nueva_col, nueva_fila)
                if nueva_pos:
                    movimientos.append(nueva_pos)
        
        return movimientos
    
    def es_movimiento_valido(self, posicion_actual, posicion_destino):
        """
        Verifica si un movimiento del Rey es válido.
        
        Args:
            posicion_actual (str): Posición de origen
            posicion_destino (str): Posición destino
            
        Returns:
            bool: True si el movimiento es válido, False en caso contrario
        """
        movimientos_posibles = self.listar_movimientos_posibles(posicion_actual)
        return posicion_destino in movimientos_posibles
