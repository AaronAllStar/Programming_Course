"""
Módulo que define la clase Alfil (Bishop).
"""

from .pieza import Pieza


class Alfil(Pieza):
    """
    Clase que representa un Alfil en el ajedrez.
    
    El Alfil se mueve diagonalmente cualquier número de casillas.
    """
    
    def listar_movimientos_posibles(self, posicion):
        """
        Lista todos los movimientos posibles del Alfil desde una posición dada.
        
        Args:
            posicion (str): Posición actual en notación de ajedrez (ej: 'c1')
            
        Returns:
            list: Lista de posiciones válidas
        """
        coordenadas = self.posicion_a_coordenadas(posicion)
        if coordenadas is None:
            return []
        
        col, fila = coordenadas
        movimientos = []
        
        # Cuatro direcciones diagonales
        direcciones = [
            (1, 1),    # diagonal arriba-derecha
            (1, -1),   # diagonal abajo-derecha
            (-1, 1),   # diagonal arriba-izquierda
            (-1, -1)   # diagonal abajo-izquierda
        ]
        
        for dc, df in direcciones:
            # Avanzar en cada dirección hasta el borde del tablero
            for distancia in range(1, 8):
                nueva_col = col + (dc * distancia)
                nueva_fila = fila + (df * distancia)
                
                if self.esta_en_tablero(nueva_col, nueva_fila):
                    nueva_pos = self.coordenadas_a_posicion(nueva_col, nueva_fila)
                    if nueva_pos:
                        movimientos.append(nueva_pos)
                else:
                    break  # Salir del tablero en esta dirección
        
        return movimientos
    
    def es_movimiento_valido(self, posicion_actual, posicion_destino):
        """
        Verifica si un movimiento del Alfil es válido.
        
        Args:
            posicion_actual (str): Posición de origen
            posicion_destino (str): Posición destino
            
        Returns:
            bool: True si el movimiento es válido, False en caso contrario
        """
        movimientos_posibles = self.listar_movimientos_posibles(posicion_actual)
        return posicion_destino in movimientos_posibles
