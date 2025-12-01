"""
Sistema de Consulta de Movimientos de Ajedrez

Programa principal que permite consultar movimientos de piezas de ajedrez.

Autor: Sistema de Ajedrez
Fecha: Diciembre 2025
"""

from presentacion.menu import Menu


def main():
    """
    Función principal del programa.
    
    Crea e inicia el menú interactivo del sistema de ajedrez.
    """
    menu = Menu()
    menu.ejecutar()


if __name__ == "__main__":
    main()
