"""
Módulo que define la clase Reina (Queen).
"""

from .pieza import Pieza


class Reina(Pieza):
    """
    Clase que representa una Reina en el ajedrez.
    
    La Reina combina los movimientos de la Torre y el Alfil:
    puede moverse horizontal, vertical o diagonalmente cualquier número de casillas.
    """
    
    def listar_movimientos_posibles(self, posicion):
        """
        Lista todos los movimientos posibles de la Reina desde una posición dada.
        
        Args:
            posicion (str): Posición actual en notación de ajedrez (ej: 'd4')
            
        Returns:
            list: Lista de posiciones válidas
        """
        coordenadas = self.posicion_a_coordenadas(posicion)
        if coordenadas is None:
            return []
        
        col, fila = coordenadas
        movimientos = []
        
        # Movimientos horizontales (como Torre)
        for nueva_col in range(8):
            if nueva_col != col:
                nueva_pos = self.coordenadas_a_posicion(nueva_col, fila)
                if nueva_pos:
                    movimientos.append(nueva_pos)
        
        # Movimientos verticales (como Torre)
        for nueva_fila in range(8):
            if nueva_fila != fila:
                nueva_pos = self.coordenadas_a_posicion(col, nueva_fila)
                if nueva_pos:
                    movimientos.append(nueva_pos)
        
        # Movimientos diagonales (como Alfil)
        direcciones = [
            (1, 1),    # diagonal arriba-derecha
            (1, -1),   # diagonal abajo-derecha
            (-1, 1),   # diagonal arriba-izquierda
            (-1, -1)   # diagonal abajo-izquierda
        ]
        
        for dc, df in direcciones:
            for distancia in range(1, 8):
                nueva_col = col + (dc * distancia)
                nueva_fila = fila + (df * distancia)
                
                if self.esta_en_tablero(nueva_col, nueva_fila):
                    nueva_pos = self.coordenadas_a_posicion(nueva_col, nueva_fila)
                    if nueva_pos:
                        movimientos.append(nueva_pos)
                else:
                    break
        
        return movimientos
    
    def es_movimiento_valido(self, posicion_actual, posicion_destino):
        """
        Verifica si un movimiento de la Reina es válido.
        
        Args:
            posicion_actual (str): Posición de origen
            posicion_destino (str): Posición destino
            
        Returns:
            bool: True si el movimiento es válido, False en caso contrario
        """
        movimientos_posibles = self.listar_movimientos_posibles(posicion_actual)
        return posicion_destino in movimientos_posibles
