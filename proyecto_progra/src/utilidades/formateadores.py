"""
Módulo: formateadores.py
Descripción: Funciones para formatear datos de salida
"""


class Formateador:
    """
    Clase con métodos estáticos para formatear datos.
    
    Proporciona formateo consistente de números, textos y tablas.
    """
    
    @staticmethod
    def formatear_moneda(valor: float, simbolo: str = "$") -> str:
        """
        Formatea un valor como moneda.
        
        Args:
            valor: Valor numérico
            simbolo: Símbolo de moneda
            
        Returns:
            String formateado como moneda
        """
        try:
            return f"{simbolo}{valor:,.2f}"
        except (ValueError, TypeError):
            return f"{simbolo}0.00"
    
    @staticmethod
    def formatear_porcentaje(valor: float, decimales: int = 2) -> str:
        """
        Formatea un valor como porcentaje.
        
        Args:
            valor: Valor numérico (0-100)
            decimales: Cantidad de decimales
            
        Returns:
            String formateado como porcentaje
        """
        try:
            return f"{valor:.{decimales}f}%"
        except (ValueError, TypeError):
            return "0.00%"
    
    @staticmethod
    def formatear_numero(valor: float, decimales: int = 2, separador_miles: bool = True) -> str:
        """
        Formatea un número con decimales y separadores.
        
        Args:
            valor: Valor numérico
            decimales: Cantidad de decimales
            separador_miles: Si se deben usar separadores de miles
            
        Returns:
            String formateado
        """
        try:
            if separador_miles:
                return f"{valor:,.{decimales}f}"
            else:
                return f"{valor:.{decimales}f}"
        except (ValueError, TypeError):
            return "0.00"
    
    @staticmethod
    def centrar_texto(texto: str, ancho: int = 50) -> str:
        """
        Centra un texto en un ancho específico.
        
        Args:
            texto: Texto a centrar
            ancho: Ancho total
            
        Returns:
            Texto centrado
        """
        return texto.center(ancho)
    
    @staticmethod
    def alinear_izquierda(texto: str, ancho: int = 50) -> str:
        """
        Alinea un texto a la izquierda.
        
        Args:
            texto: Texto a alinear
            ancho: Ancho total
            
        Returns:
            Texto alineado
        """
        return texto.ljust(ancho)
    
    @staticmethod
    def alinear_derecha(texto: str, ancho: int = 50) -> str:
        """
        Alinea un texto a la derecha.
        
        Args:
            texto: Texto a alinear
            ancho: Ancho total
            
        Returns:
            Texto alineado
        """
        return texto.rjust(ancho)
    
    @staticmethod
    def crear_barra_progreso(porcentaje: float, longitud: int = 20) -> str:
        """
        Crea una barra de progreso visual.
        
        Args:
            porcentaje: Porcentaje de completitud (0-100)
            longitud: Longitud de la barra en caracteres
            
        Returns:
            String con la barra de progreso
        """
        try:
            porcentaje = max(0, min(100, porcentaje))  # Limitar entre 0 y 100
            completado = int((porcentaje / 100) * longitud)
            barra = "█" * completado + "░" * (longitud - completado)
            return f"[{barra}] {porcentaje:.1f}%"
        except (ValueError, TypeError):
            return f"[{'░' * longitud}] 0.0%"
    
    @staticmethod
    def separador(longitud: int = 60, caracter: str = "-") -> str:
        """
        Crea una línea separadora.
        
        Args:
            longitud: Longitud de la línea
            caracter: Carácter a usar
            
        Returns:
            Línea separadora
        """
        return caracter * longitud
    
    @staticmethod
    def titulo(texto: str, longitud: int = 60) -> str:
        """
        Formatea un texto como título centrado con bordes.
        
        Args:
            texto: Texto del título
            longitud: Ancho total
            
        Returns:
            Título formateado
        """
        linea = "=" * longitud
        titulo_centro = texto.upper().center(longitud)
        return f"\n{linea}\n{titulo_centro}\n{linea}\n"
