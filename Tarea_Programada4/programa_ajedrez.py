# ==========================================
# PROGRAMA PRINCIPAL: SISTEMA DE AJEDREZ
# IMPORTA: herencia.py (Capa de Entidades)
# ==========================================

from herencia import Torre, Alfil, Caballo, Reina, Rey, Peon

# ==========================================
# CAPA DE LÓGICA DE NEGOCIO
# ==========================================

class ServicioAjedrez:
    """
    Clase de servicio que gestiona la lógica de negocio
    Actúa como intermediario entre la interfaz y las entidades
    """
    
    def crear_pieza(self, tipo_pieza, posicion, color='blanco'):
        """
        Factory method para crear instancias de piezas
        :param tipo_pieza: Nombre de la pieza (Torre, Alfil, etc.)
        :param posicion: Tupla (columna, fila)
        :param color: Color para el peón ('blanco' o 'negro')
        :return: Instancia de la pieza o None si el tipo no existe
        """
        tipo_pieza = tipo_pieza.lower().strip()
        
        if tipo_pieza == 'torre':
            return Torre(posicion)
        elif tipo_pieza == 'alfil':
            return Alfil(posicion)
        elif tipo_pieza == 'caballo':
            return Caballo(posicion)
        elif tipo_pieza == 'reina' or tipo_pieza == 'dama':
            return Reina(posicion)
        elif tipo_pieza == 'rey':
            return Rey(posicion)
        elif tipo_pieza == 'peon' or tipo_pieza == 'peón':
            return Peon(posicion, color)
        else:
            return None
    
    def consultar_movimientos(self, pieza):
        """
        Obtiene todos los movimientos posibles de una pieza
        :param pieza: Instancia de una pieza
        :return: Lista de tuplas (columna, fila) con movimientos posibles
        """
        if pieza is None:
            return []
        return pieza.calcular_movimientos_posibles()
    
    def verificar_movimiento(self, pieza, casilla_destino):
        """
        Verifica si un movimiento específico es válido
        :param pieza: Instancia de una pieza
        :param casilla_destino: Tupla (columna, fila) destino
        :return: True si el movimiento es posible, False si no
        """
        if pieza is None:
            return False
        
        movimientos_posibles = self.consultar_movimientos(pieza)
        return casilla_destino in movimientos_posibles


# ==========================================
# CAPA DE PRESENTACIÓN/INTERFAZ
# ==========================================

class MenuAjedrez:
    """
    Clase que maneja la interfaz de usuario
    Presenta menús y gestiona la interacción con el usuario
    """
    
    def __init__(self):
        self.servicio = ServicioAjedrez()
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal del programa"""
        print("\n" + "="*60)
        print("    SISTEMA DE CONSULTA DE MOVIMIENTOS DE AJEDREZ")
        print("="*60)
        print("1. Consultar movimientos posibles de una pieza")
        print("2. Verificar si un movimiento específico es posible")
        print("3. Salir")
        print("="*60)
    
    def solicitar_pieza(self):
        """
        Solicita al usuario el tipo de pieza
        :return: Nombre de la pieza en minúsculas
        """
        print("\n📋 Tipos de piezas disponibles:")
        print("   • Torre")
        print("   • Alfil")
        print("   • Caballo")
        print("   • Reina (o Dama)")
        print("   • Rey")
        print("   • Peón")
        
        pieza = input("\n¿Qué pieza deseas consultar? ").strip()
        return pieza
    
    def solicitar_posicion(self, mensaje="¿En qué posición está la pieza?"):
        """
        Solicita y valida una posición del tablero
        :param mensaje: Mensaje a mostrar al usuario
        :return: Tupla (columna, fila) o None si es inválida
        """
        print(f"\n{mensaje}")
        print("   Formato: columna (a-h) y fila (1-8)")
        print("   Ejemplo: e4 → columna 'e', fila 4")
        
        entrada = input("\nPosición: ").strip().lower()
        
        # Validar longitud
        if len(entrada) < 2:
            print("❌ Error: Entrada muy corta. Usa formato como 'e4'")
            return None
        
        # Extraer columna y fila
        columna = entrada[0]
        
        try:
            # Intentar convertir el resto a número
            fila = int(entrada[1:])
        except ValueError:
            print("❌ Error: La fila debe ser un número entre 1 y 8")
            return None
        
        # Validar rangos
        if not ('a' <= columna <= 'h'):
            print(f"❌ Error: La columna '{columna}' no es válida. Debe ser entre 'a' y 'h'")
            return None
        
        if not (1 <= fila <= 8):
            print(f"❌ Error: La fila {fila} no es válida. Debe ser entre 1 y 8")
            return None
        
        return (columna, fila)
    
    def solicitar_color_peon(self):
        """Solicita el color del peón si es necesario"""
        while True:
            color = input("\n¿Color del peón? (blanco/negro): ").strip().lower()
            if color in ['blanco', 'negro']:
                return color
            print("❌ Error: Debes elegir 'blanco' o 'negro'")
    
    def formatear_movimientos(self, movimientos):
        """
        Formatea la lista de movimientos para mostrarla de forma legible
        :param movimientos: Lista de tuplas (columna, fila)
        :return: String formateado
        """
        if not movimientos:
            return "   (No hay movimientos posibles)"
        
        # Agrupar en filas de 8 movimientos
        resultado = []
        for i in range(0, len(movimientos), 8):
            grupo = movimientos[i:i+8]
            linea = "   " + ", ".join([f"{col}{fila}" for col, fila in grupo])
            resultado.append(linea)
        
        return "\n".join(resultado)
    
    def opcion_consultar_movimientos(self):
        """
        OPCIÓN 1: Consulta todos los movimientos posibles de una pieza
        """
        print("\n" + "─"*60)
        print("  OPCIÓN 1: CONSULTAR MOVIMIENTOS POSIBLES")
        print("─"*60)
        
        # Solicitar tipo de pieza
        tipo_pieza = self.solicitar_pieza()
        
        # Solicitar posición
        posicion = self.solicitar_posicion()
        if posicion is None:
            return
        
        # Determinar si es peón para solicitar color
        color = 'blanco'
        if tipo_pieza.lower() in ['peon', 'peón']:
            color = self.solicitar_color_peon()
        
        # Crear la pieza
        pieza = self.servicio.crear_pieza(tipo_pieza, posicion, color)
        
        if pieza is None:
            print(f"\n❌ Error: '{tipo_pieza}' no es una pieza válida")
            return
        
        # Obtener movimientos
        movimientos = self.servicio.consultar_movimientos(pieza)
        
        # Mostrar resultados
        print(f"\n✅ {pieza.nombre} en {posicion[0]}{posicion[1]}")
        print(f"\n📍 Movimientos posibles ({len(movimientos)} casillas):")
        print(self.formatear_movimientos(movimientos))
    
    def opcion_verificar_movimiento(self):
        """
        OPCIÓN 2: Verifica si un movimiento específico es válido
        """
        print("\n" + "─"*60)
        print("  OPCIÓN 2: VERIFICAR MOVIMIENTO ESPECÍFICO")
        print("─"*60)
        
        # Solicitar tipo de pieza
        tipo_pieza = self.solicitar_pieza()
        
        # Solicitar posición actual
        posicion_actual = self.solicitar_posicion("¿En qué posición está la pieza?")
        if posicion_actual is None:
            return
        
        # Determinar si es peón para solicitar color
        color = 'blanco'
        if tipo_pieza.lower() in ['peon', 'peón']:
            color = self.solicitar_color_peon()
        
        # Crear la pieza
        pieza = self.servicio.crear_pieza(tipo_pieza, posicion_actual, color)
        
        if pieza is None:
            print(f"\n❌ Error: '{tipo_pieza}' no es una pieza válida")
            return
        
        # Solicitar casilla destino
        casilla_destino = self.solicitar_posicion("¿A qué casilla quieres mover?")
        if casilla_destino is None:
            return
        
        # Verificar el movimiento
        es_posible = self.servicio.verificar_movimiento(pieza, casilla_destino)
        
        # Mostrar resultado
        print(f"\n{pieza.nombre} en {posicion_actual[0]}{posicion_actual[1]} " 
              f"→ {casilla_destino[0]}{casilla_destino[1]}")
        
        if es_posible:
            print("✅ El movimiento ES POSIBLE")
        else:
            print("❌ El movimiento NO es posible")
    
    def ejecutar(self):
        """
        Loop principal del programa
        Muestra el menú y ejecuta las opciones hasta que el usuario salga
        """
        print("\n🎯 Bienvenido al Sistema de Consulta de Ajedrez")
        
        while True:
            self.mostrar_menu_principal()
            
            opcion = input("\nSelecciona una opción (1-3): ").strip()
            
            if opcion == '1':
                self.opcion_consultar_movimientos()
            
            elif opcion == '2':
                self.opcion_verificar_movimiento()
            
            elif opcion == '3':
                print("\n👋 ¡Gracias por usar el sistema! Hasta pronto.")
                print("="*60)
                break
            
            else:
                print(f"\n❌ Error: '{opcion}' no es una opción válida")
                print("   Por favor elige 1, 2 o 3")


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":
    menu = MenuAjedrez()
    menu.ejecutar()
