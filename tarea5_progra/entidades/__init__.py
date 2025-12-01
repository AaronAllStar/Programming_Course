"""
Paquete de entidades del sistema de ajedrez.

Contiene la clase abstracta Pieza y todas las implementaciones concretas
de las piezas de ajedrez.
"""

from .pieza import Pieza
from .rey import Rey
from .reina import Reina
from .torre import Torre
from .alfil import Alfil
from .caballo import Caballo
from .peon import Peon

__all__ = ['Pieza', 'Rey', 'Reina', 'Torre', 'Alfil', 'Caballo', 'Peon']
