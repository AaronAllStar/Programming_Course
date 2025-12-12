"""
Módulo: validadores.py
Descripción: Funciones y clases para validar datos
"""


class Validador:
    """
    Clase con métodos estáticos para validar diferentes tipos de datos.
    
    Proporciona validaciones comunes reutilizables en todo el sistema.
    """
    
    @staticmethod
    def es_numero(valor: str) -> bool:
        """
        Valida si un valor es numérico.
        
        Args:
            valor: Valor a validar
            
        Returns:
            True si es numérico, False en caso contrario
        """
        if valor is None:
            return False
        try:
            float(valor)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def es_entero(valor: str) -> bool:
        """
        Valida si un valor es un número entero.
        
        Args:
            valor: Valor a validar
            
        Returns:
            True si es entero, False en caso contrario
        """
        if valor is None:
            return False
        try:
            int(valor)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def es_positivo(valor) -> bool:
        """
        Valida si un valor numérico es positivo.
        
        Args:
            valor: Valor a validar
            
        Returns:
            True si es positivo, False en caso contrario
        """
        if not Validador.es_numero(valor):
            return False
        return float(valor) > 0
    
    @staticmethod
    def esta_en_rango(valor, minimo, maximo) -> bool:
        """
        Valida si un valor está dentro de un rango.
        
        Args:
            valor: Valor a validar
            minimo: Valor mínimo del rango
            maximo: Valor máximo del rango
            
        Returns:
            True si está en rango, False en caso contrario
        """
        if not Validador.es_numero(valor):
            return False
        valor_num = float(valor)
        return minimo <= valor_num <= maximo
    
    @staticmethod
    def no_esta_vacio(valor: str) -> bool:
        """
        Valida que un valor no esté vacío.
        
        Args:
            valor: Valor a validar
            
        Returns:
            True si no está vacío, False en caso contrario
        """
        if valor is None:
            return False
        return str(valor).strip() != ''
    
    @staticmethod
    def validar_opcion_menu(opcion: str, opciones_validas: list) -> bool:
        """
        Valida que una opción esté en la lista de opciones válidas.
        
        Args:
            opcion: Opción seleccionada
            opciones_validas: Lista de opciones válidas
            
        Returns:
            True si es válida, False en caso contrario
        """
        return opcion in opciones_validas
    
    @staticmethod
    def validar_formato_fecha(fecha: str, formato: str = "%Y-%m-%d") -> bool:
        """
        Valida que una fecha tenga un formato específico.
        
        Args:
            fecha: Fecha a validar
            formato: Formato esperado (por defecto YYYY-MM-DD)
            
        Returns:
            True si el formato es correcto, False en caso contrario
        """
        from datetime import datetime
        
        try:
            datetime.strptime(fecha, formato)
            return True
        except (ValueError, TypeError):
            return False
