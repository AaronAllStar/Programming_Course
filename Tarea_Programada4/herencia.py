# ==========================================
# PROYECTO: SISTEMA DE CONSULTA DE MOVIMIENTOS DE AJEDREZ
# ARQUITECTURA: 3 CAPAS + POO + HERENCIA + POLIMORFISMO
# CURSO: Programación
# ==========================================

# ==========================================
# CAPA DE ENTIDADES (Clases con Herencia)
# ==========================================

class Pieza:
    """
    SUPERCLASE: Representa una pieza genérica de ajedrez
    Implementa herencia y polimorfismo para todas las piezas
    """
    
    def __init__(self, nombre, posicion):
        """
        Constructor de la superclase
        :param nombre: Nombre de la pieza (ej: "Torre", "Caballo")
        :param posicion: Tupla (columna, fila) donde columna es 'a'-'h' y fila es 1-8
        """
        self.nombre = nombre
        self.columna = posicion[0]
        self.fila = posicion[1]
    
    def obtener_posicion(self):
        """Retorna la posición actual como tupla"""
        return (self.columna, self.fila)
    
    def calcular_movimientos_posibles(self):
        """
        MÉTODO POLIMÓRFICO: Cada subclase implementará su propia lógica
        Este método debe ser sobrescrito por las clases hijas
        """
        raise NotImplementedError("Este método debe ser implementado por las subclases")
    
    def es_posicion_valida(self, columna, fila):
        """
        Valida que una posición esté dentro del tablero
        :param columna: Letra entre 'a' y 'h'
        :param fila: Número entre 1 y 8
        :return: True si es válida, False si no
        """
        return 'a' <= columna <= 'h' and 1 <= fila <= 8


class Torre(Pieza):
    """
    SUBCLASE: Torre - Se mueve en líneas rectas (horizontal y vertical)
    """
    
    def __init__(self, posicion):
        super().__init__("Torre", posicion)
    
    def calcular_movimientos_posibles(self):
        """
        POLIMORFISMO: Implementación específica para Torre
        La torre se mueve en líneas rectas: horizontal y vertical
        """
        movimientos = []
        
        # Movimientos verticales (misma columna, diferentes filas)
        for fila in range(1, 9):
            if fila != self.fila:
                movimientos.append((self.columna, fila))
        
        # Movimientos horizontales (misma fila, diferentes columnas)
        for columna_ord in range(ord('a'), ord('h') + 1):
            columna = chr(columna_ord)
            if columna != self.columna:
                movimientos.append((columna, self.fila))
        
        return movimientos


class Alfil(Pieza):
    """
    SUBCLASE: Alfil - Se mueve en diagonales
    """
    
    def __init__(self, posicion):
        super().__init__("Alfil", posicion)
    
    def calcular_movimientos_posibles(self):
        """
        POLIMORFISMO: Implementación específica para Alfil
        El alfil se mueve en diagonales
        """
        movimientos = []
        
        # Diagonal superior derecha
        for i in range(1, 8):
            nueva_columna = chr(ord(self.columna) + i)
            nueva_fila = self.fila + i
            if self.es_posicion_valida(nueva_columna, nueva_fila):
                movimientos.append((nueva_columna, nueva_fila))
        
        # Diagonal superior izquierda
        for i in range(1, 8):
            nueva_columna = chr(ord(self.columna) - i)
            nueva_fila = self.fila + i
            if self.es_posicion_valida(nueva_columna, nueva_fila):
                movimientos.append((nueva_columna, nueva_fila))
        
        # Diagonal inferior derecha
        for i in range(1, 8):
            nueva_columna = chr(ord(self.columna) + i)
            nueva_fila = self.fila - i
            if self.es_posicion_valida(nueva_columna, nueva_fila):
                movimientos.append((nueva_columna, nueva_fila))
        
        # Diagonal inferior izquierda
        for i in range(1, 8):
            nueva_columna = chr(ord(self.columna) - i)
            nueva_fila = self.fila - i
            if self.es_posicion_valida(nueva_columna, nueva_fila):
                movimientos.append((nueva_columna, nueva_fila))
        
        return movimientos


class Caballo(Pieza):
    """
    SUBCLASE: Caballo - Se mueve en forma de "L"
    """
    
    def __init__(self, posicion):
        super().__init__("Caballo", posicion)
    
    def calcular_movimientos_posibles(self):
        """
        POLIMORFISMO: Implementación específica para Caballo
        El caballo se mueve en forma de L (2 casillas en una dirección, 1 en perpendicular)
        """
        movimientos = []
        
        # Los 8 movimientos posibles del caballo en forma de L
        movimientos_l = [
            (2, 1), (2, -1),   # 2 derecha, 1 arriba/abajo
            (-2, 1), (-2, -1), # 2 izquierda, 1 arriba/abajo
            (1, 2), (1, -2),   # 1 derecha, 2 arriba/abajo
            (-1, 2), (-1, -2)  # 1 izquierda, 2 arriba/abajo
        ]
        
        for delta_col, delta_fila in movimientos_l:
            nueva_columna = chr(ord(self.columna) + delta_col)
            nueva_fila = self.fila + delta_fila
            
            if self.es_posicion_valida(nueva_columna, nueva_fila):
                movimientos.append((nueva_columna, nueva_fila))
        
        return movimientos


class Reina(Pieza):
    """
    SUBCLASE: Reina - Se mueve como Torre + Alfil (horizontal, vertical y diagonal)
    """
    
    def __init__(self, posicion):
        super().__init__("Reina", posicion)
    
    def calcular_movimientos_posibles(self):
        """
        POLIMORFISMO: Implementación específica para Reina
        La reina combina movimientos de Torre y Alfil
        """
        movimientos = []
        
        # Movimientos de Torre (horizontal y vertical)
        for fila in range(1, 9):
            if fila != self.fila:
                movimientos.append((self.columna, fila))
        
        for columna_ord in range(ord('a'), ord('h') + 1):
            columna = chr(columna_ord)
            if columna != self.columna:
                movimientos.append((columna, self.fila))
        
        # Movimientos de Alfil (diagonales)
        for i in range(1, 8):
            # Diagonal superior derecha
            nueva_columna = chr(ord(self.columna) + i)
            nueva_fila = self.fila + i
            if self.es_posicion_valida(nueva_columna, nueva_fila):
                movimientos.append((nueva_columna, nueva_fila))
            
            # Diagonal superior izquierda
            nueva_columna = chr(ord(self.columna) - i)
            nueva_fila = self.fila + i
            if self.es_posicion_valida(nueva_columna, nueva_fila):
                movimientos.append((nueva_columna, nueva_fila))
            
            # Diagonal inferior derecha
            nueva_columna = chr(ord(self.columna) + i)
            nueva_fila = self.fila - i
            if self.es_posicion_valida(nueva_columna, nueva_fila):
                movimientos.append((nueva_columna, nueva_fila))
            
            # Diagonal inferior izquierda
            nueva_columna = chr(ord(self.columna) - i)
            nueva_fila = self.fila - i
            if self.es_posicion_valida(nueva_columna, nueva_fila):
                movimientos.append((nueva_columna, nueva_fila))
        
        return movimientos


class Rey(Pieza):
    """
    SUBCLASE: Rey - Se mueve una casilla en cualquier dirección
    """
    
    def __init__(self, posicion):
        super().__init__("Rey", posicion)
    
    def calcular_movimientos_posibles(self):
        """
        POLIMORFISMO: Implementación específica para Rey
        El rey se mueve una casilla en cualquier dirección
        """
        movimientos = []
        
        # Las 8 direcciones posibles (horizontal, vertical y diagonal)
        direcciones = [
            (0, 1), (0, -1),     # Vertical arriba/abajo
            (1, 0), (-1, 0),     # Horizontal derecha/izquierda
            (1, 1), (1, -1),     # Diagonal derecha arriba/abajo
            (-1, 1), (-1, -1)    # Diagonal izquierda arriba/abajo
        ]
        
        for delta_col, delta_fila in direcciones:
            nueva_columna = chr(ord(self.columna) + delta_col)
            nueva_fila = self.fila + delta_fila
            
            if self.es_posicion_valida(nueva_columna, nueva_fila):
                movimientos.append((nueva_columna, nueva_fila))
        
        return movimientos


class Peon(Pieza):
    """
    SUBCLASE: Peón - Se mueve hacia adelante (simplificado sin capturas diagonales)
    """
    
    def __init__(self, posicion, color='blanco'):
        super().__init__("Peón", posicion)
        self.color = color  # 'blanco' o 'negro'
        # Determinar posición inicial según color
        self.posicion_inicial = 2 if color == 'blanco' else 7
    
    def calcular_movimientos_posibles(self):
        """
        POLIMORFISMO: Implementación específica para Peón
        El peón se mueve hacia adelante (1 o 2 casillas desde posición inicial)
        """
        movimientos = []
        
        # Dirección según el color
        direccion = 1 if self.color == 'blanco' else -1
        
        # Movimiento de 1 casilla hacia adelante
        nueva_fila = self.fila + direccion
        if self.es_posicion_valida(self.columna, nueva_fila):
            movimientos.append((self.columna, nueva_fila))
        
        # Movimiento de 2 casillas si está en posición inicial
        if self.fila == self.posicion_inicial:
            nueva_fila = self.fila + (2 * direccion)
            if self.es_posicion_valida(self.columna, nueva_fila):
                movimientos.append((self.columna, nueva_fila))
        
        return movimientos


print("✅ CAPA DE ENTIDADES DEFINIDA")
print("   • Superclase: Pieza")
print("   • Subclases: Torre, Alfil, Caballo, Reina, Rey, Peón")
print("   • Herencia y Polimorfismo implementados")