"""
Módulo de presentación - Interfaz de usuario del sistema de ajedrez.

Proporciona el menú interactivo y la comunicación con el usuario.
"""

from logica.servicio_ajedrez import ServicioAjedrez


class Menu:
    """
    Clase que gestiona la interfaz de usuario y el menú principal.
    """
    
    def __init__(self):
        """Inicializa el menú."""
        self.servicio = ServicioAjedrez()
    
    def mostrar_menu_principal(self):
        """Muestra las opciones del menú principal."""
        print("\n" + "="*50)
        print("  SISTEMA DE CONSULTA DE MOVIMIENTOS DE AJEDREZ")
        print("="*50)
        print("\n1. Consultar movimientos posibles de una pieza")
        print("2. Verificar si un movimiento es válido")
        print("3. Salir")
        print("-"*50)
    
    def solicitar_pieza(self):
        """
        Solicita al usuario que ingrese el nombre de una pieza.
        
        Returns:
            str: Nombre de la pieza ingresado por el usuario
        """
        print(f"\nPiezas disponibles: {', '.join(self.servicio.listar_piezas_disponibles())}")
        pieza = input("Ingrese el nombre de la pieza: ").strip()
        return pieza
    
    def solicitar_posicion(self, mensaje="Ingrese la posición (ej: e4): "):
        """
        Solicita al usuario que ingrese una posición.
        
        Args:
            mensaje (str): Mensaje a mostrar al usuario
            
        Returns:
            str: Posición ingresada por el usuario
        """
        posicion = input(mensaje).strip().lower()
        return posicion
    
    def opcion_consultar_movimientos(self):
        """Ejecuta la opción 1: Consultar movimientos posibles."""
        print("\n--- CONSULTAR MOVIMIENTOS POSIBLES ---")
        
        # Solicitar pieza
        nombre_pieza = self.solicitar_pieza()
        
        # Validar que la pieza existe
        if self.servicio.obtener_pieza(nombre_pieza) is None:
            print(f"\n❌ Error: '{nombre_pieza}' no es una pieza válida.")
            return
        
        # Solicitar posición
        posicion = self.solicitar_posicion("Ingrese la posición actual (ej: e4): ")
        
        # Validar posición
        if not self.servicio.validar_posicion(posicion):
            print(f"\n❌ Error: '{posicion}' no es una posición válida.")
            print("   La posición debe ser una letra (a-h) seguida de un número (1-8).")
            return
        
        # Obtener movimientos
        movimientos = self.servicio.consultar_movimientos(nombre_pieza, posicion)
        
        # Mostrar resultados
        if movimientos:
            print(f"\n✓ Movimientos posibles del {nombre_pieza} desde {posicion}:")
            print(f"  {', '.join(sorted(movimientos))}")
            print(f"  Total: {len(movimientos)} movimientos")
        else:
            print(f"\n⚠ El {nombre_pieza} en {posicion} no tiene movimientos posibles.")
    
    def opcion_verificar_movimiento(self):
        """Ejecuta la opción 2: Verificar si un movimiento es válido."""
        print("\n--- VERIFICAR MOVIMIENTO ---")
        
        # Solicitar pieza
        nombre_pieza = self.solicitar_pieza()
        
        # Validar que la pieza existe
        if self.servicio.obtener_pieza(nombre_pieza) is None:
            print(f"\n❌ Error: '{nombre_pieza}' no es una pieza válida.")
            return
        
        # Solicitar posición actual
        posicion_actual = self.solicitar_posicion("Ingrese la posición actual (ej: e4): ")
        
        # Validar posición actual
        if not self.servicio.validar_posicion(posicion_actual):
            print(f"\n❌ Error: '{posicion_actual}' no es una posición válida.")
            print("   La posición debe ser una letra (a-h) seguida de un número (1-8).")
            return
        
        # Solicitar posición destino
        posicion_destino = self.solicitar_posicion("Ingrese la posición destino (ej: e5): ")
        
        # Validar posición destino
        if not self.servicio.validar_posicion(posicion_destino):
            print(f"\n❌ Error: '{posicion_destino}' no es una posición válida.")
            print("   La posición debe ser una letra (a-h) seguida de un número (1-8).")
            return
        
        # Verificar movimiento
        es_valido = self.servicio.verificar_movimiento(
            nombre_pieza, 
            posicion_actual, 
            posicion_destino
        )
        
        # Mostrar resultado
        if es_valido:
            print(f"\n✓ El movimiento {posicion_actual} → {posicion_destino} es VÁLIDO para el {nombre_pieza}.")
        else:
            print(f"\n✗ El movimiento {posicion_actual} → {posicion_destino} NO es válido para el {nombre_pieza}.")
    
    def ejecutar(self):
        """Ejecuta el bucle principal del menú."""
        print("\n¡Bienvenido al Sistema de Consulta de Movimientos de Ajedrez!")
        
        while True:
            self.mostrar_menu_principal()
            
            try:
                opcion = input("\nSeleccione una opción (1-3): ").strip()
                
                if opcion == '1':
                    self.opcion_consultar_movimientos()
                elif opcion == '2':
                    self.opcion_verificar_movimiento()
                elif opcion == '3':
                    print("\n¡Gracias por usar el sistema! Hasta pronto.")
                    break
                else:
                    print("\n❌ Opción no válida. Por favor, seleccione 1, 2 o 3.")
            
            except KeyboardInterrupt:
                print("\n\n¡Programa interrumpido! Hasta pronto.")
                break
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                print("   Por favor, intente nuevamente.")
