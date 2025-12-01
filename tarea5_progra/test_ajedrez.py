"""
Script de prueba para verificar el sistema de ajedrez.

Este script prueba las diferentes piezas y sus movimientos.
"""

from logica.servicio_ajedrez import ServicioAjedrez


def test_rey():
    """Prueba el Rey."""
    print("\n=== PRUEBA: REY ===")
    servicio = ServicioAjedrez()
    
    # Test movimientos posibles
    movimientos = servicio.consultar_movimientos('rey', 'e4')
    print(f"Rey en e4 - Movimientos posibles: {sorted(movimientos)}")
    print(f"Total: {len(movimientos)} movimientos")
    
    # Test validación de movimientos
    print(f"Rey e4 → e5: {servicio.verificar_movimiento('rey', 'e4', 'e5')}")
    print(f"Rey e4 → e6: {servicio.verificar_movimiento('rey', 'e4', 'e6')}")


def test_reina():
    """Prueba la Reina."""
    print("\n=== PRUEBA: REINA ===")
    servicio = ServicioAjedrez()
    
    movimientos = servicio.consultar_movimientos('reina', 'd4')
    print(f"Reina en d4 - Total movimientos: {len(movimientos)}")
    print(f"Primeros 10: {sorted(movimientos)[:10]}")
    
    print(f"Reina d4 → d8: {servicio.verificar_movimiento('reina', 'd4', 'd8')}")
    print(f"Reina d4 → h8: {servicio.verificar_movimiento('reina', 'd4', 'h8')}")


def test_torre():
    """Prueba la Torre."""
    print("\n=== PRUEBA: TORRE ===")
    servicio = ServicioAjedrez()
    
    movimientos = servicio.consultar_movimientos('torre', 'a1')
    print(f"Torre en a1 - Movimientos posibles: {sorted(movimientos)}")
    print(f"Total: {len(movimientos)} movimientos")
    
    print(f"Torre a1 → a8: {servicio.verificar_movimiento('torre', 'a1', 'a8')}")
    print(f"Torre a1 → b2: {servicio.verificar_movimiento('torre', 'a1', 'b2')}")


def test_alfil():
    """Prueba el Alfil."""
    print("\n=== PRUEBA: ALFIL ===")
    servicio = ServicioAjedrez()
    
    movimientos = servicio.consultar_movimientos('alfil', 'c1')
    print(f"Alfil en c1 - Movimientos posibles: {sorted(movimientos)}")
    print(f"Total: {len(movimientos)} movimientos")
    
    print(f"Alfil c1 → f4: {servicio.verificar_movimiento('alfil', 'c1', 'f4')}")
    print(f"Alfil c1 → c4: {servicio.verificar_movimiento('alfil', 'c1', 'c4')}")


def test_caballo():
    """Prueba el Caballo."""
    print("\n=== PRUEBA: CABALLO ===")
    servicio = ServicioAjedrez()
    
    movimientos = servicio.consultar_movimientos('caballo', 'e4')
    print(f"Caballo en e4 - Movimientos posibles: {sorted(movimientos)}")
    print(f"Total: {len(movimientos)} movimientos")
    
    print(f"Caballo e4 → f6: {servicio.verificar_movimiento('caballo', 'e4', 'f6')}")
    print(f"Caballo e4 → e5: {servicio.verificar_movimiento('caballo', 'e4', 'e5')}")


def test_peon():
    """Prueba el Peón."""
    print("\n=== PRUEBA: PEÓN ===")
    servicio = ServicioAjedrez()
    
    # Peón en posición inicial
    movimientos = servicio.consultar_movimientos('peon', 'e2')
    print(f"Peón en e2 (inicio) - Movimientos posibles: {sorted(movimientos)}")
    
    # Peón en otra posición
    movimientos = servicio.consultar_movimientos('peon', 'e4')
    print(f"Peón en e4 - Movimientos posibles: {sorted(movimientos)}")
    
    print(f"Peón e2 → e4: {servicio.verificar_movimiento('peon', 'e2', 'e4')}")
    print(f"Peón e2 → e5: {servicio.verificar_movimiento('peon', 'e2', 'e5')}")


def test_casos_borde():
    """Prueba casos en los bordes del tablero."""
    print("\n=== PRUEBA: CASOS BORDE ===")
    servicio = ServicioAjedrez()
    
    # Rey en esquina
    movimientos = servicio.consultar_movimientos('rey', 'a1')
    print(f"Rey en a1 (esquina) - Movimientos: {sorted(movimientos)}")
    
    # Caballo en esquina
    movimientos = servicio.consultar_movimientos('caballo', 'h8')
    print(f"Caballo en h8 (esquina) - Movimientos: {sorted(movimientos)}")


def test_validacion():
    """Prueba la validación de entradas."""
    print("\n=== PRUEBA: VALIDACIÓN ===")
    servicio = ServicioAjedrez()
    
    # Posición inválida
    result = servicio.consultar_movimientos('rey', 'z9')
    print(f"Rey en posición inválida 'z9': {result}")
    
    # Pieza inválida
    result = servicio.consultar_movimientos('dragon', 'e4')
    print(f"Pieza inválida 'dragon': {result}")


def main():
    """Ejecuta todas las pruebas."""
    print("="*60)
    print("  PRUEBAS DEL SISTEMA DE MOVIMIENTOS DE AJEDREZ")
    print("="*60)
    
    test_rey()
    test_reina()
    test_torre()
    test_alfil()
    test_caballo()
    test_peon()
    test_casos_borde()
    test_validacion()
    
    print("\n" + "="*60)
    print("  TODAS LAS PRUEBAS COMPLETADAS")
    print("="*60)


if __name__ == "__main__":
    main()
