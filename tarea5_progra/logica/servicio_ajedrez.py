"""
Módulo de servicio para operaciones de ajedrez.

Proporciona funcionalidad de alto nivel para trabajar con piezas de ajedrez,
incluyendo creación de piezas, validación de movimientos y listado de posiciones.
"""

from entidades import Rey, Reina, Torre, Alfil, Caballo, Peon


class ServicioAjedrez:
    """
    Servicio que proporciona operaciones de lógica de negocio para el ajedrez.
    """
    
    # Mapeo de nombres de piezas a sus clases
    PIEZAS_DISPONIBLES = {
        'rey': Rey,
        'reina': Reina,
        'torre': Torre,
        'alfil': Alfil,
        'caballo': Caballo,
        'peon': Peon
    }
    
    @staticmethod
    def obtener_pieza(nombre_pieza):
        """
        Crea una instancia de pieza basada en el nombre.
        
        Args:
            nombre_pieza (str): Nombre de la pieza (ej: 'rey', 'reina')
            
        Returns:
            Pieza: Instancia de la pieza correspondiente
            None: Si el nombre no es válido
        """
        nombre_normalizado = nombre_pieza.lower().strip()
        clase_pieza = ServicioAjedrez.PIEZAS_DISPONIBLES.get(nombre_normalizado)
        
        if clase_pieza:
            return clase_pieza()
        return None
    
    @staticmethod
    def listar_piezas_disponibles():
        """
        Retorna la lista de nombres de piezas disponibles.
        
        Returns:
            list: Lista de nombres de piezas
        """
        return list(ServicioAjedrez.PIEZAS_DISPONIBLES.keys())
    
    @staticmethod
    def consultar_movimientos(nombre_pieza, posicion):
        """
        Consulta los movimientos posibles de una pieza desde una posición.
        
        Args:
            nombre_pieza (str): Nombre de la pieza
            posicion (str): Posición actual en notación de ajedrez
            
        Returns:
            list: Lista de movimientos posibles
            None: Si la pieza o posición no son válidas
        """
        pieza = ServicioAjedrez.obtener_pieza(nombre_pieza)
        if pieza is None:
            return None
        
        if not ServicioAjedrez.validar_posicion(posicion):
            return None
        
        return pieza.listar_movimientos_posibles(posicion)
    
    @staticmethod
    def verificar_movimiento(nombre_pieza, posicion_actual, posicion_destino):
        """
        Verifica si un movimiento específico es válido para una pieza.
        
        Args:
            nombre_pieza (str): Nombre de la pieza
            posicion_actual (str): Posición de origen
            posicion_destino (str): Posición destino
            
        Returns:
            bool: True si el movimiento es válido
            None: Si la pieza o posiciones no son válidas
        """
        pieza = ServicioAjedrez.obtener_pieza(nombre_pieza)
        if pieza is None:
            return None
        
        if not ServicioAjedrez.validar_posicion(posicion_actual):
            return None
        
        if not ServicioAjedrez.validar_posicion(posicion_destino):
            return None
        
        return pieza.es_movimiento_valido(posicion_actual, posicion_destino)
    
    @staticmethod
    def validar_posicion(posicion):
        """
        Valida que una posición tenga el formato correcto.
        
        Args:
            posicion (str): Posición a validar (ej: 'e4')
            
        Returns:
            bool: True si la posición es válida, False en caso contrario
        """
        if not posicion or len(posicion) != 2:
            return False
        
        columna = posicion[0].lower()
        fila = posicion[1]
        
        return 'a' <= columna <= 'h' and '1' <= fila <= '8'
