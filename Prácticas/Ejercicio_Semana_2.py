def resolver_colision(asteroide_nuevo, asteroide_existente):
    """
    Resuelve la colisión entre dos asteroides.
    Retorna el asteroide que sobrevive, o None si ambos se destruyen.
    """
    # Si el nuevo asteroide es más grande, destruye al existente.
    # El nuevo asteroide sobrevive para seguir colisionando.
    if abs(asteroide_nuevo) > asteroide_existente:
        return asteroide_nuevo
    # Si ambos son del mismo tamaño, ambos se destruyen.
    elif abs(asteroide_nuevo) == asteroide_existente:
        return None
    # Si el nuevo asteroide es más pequeño, se destruye.
    # El asteroide existente sobrevive.
    else: # abs(asteroide_nuevo) < asteroide_existente
        return asteroide_existente

def asteroid_collision(asteroids):
    """
    Simula colisiones de asteroides de una forma más estructurada.

    Args:
        asteroids: Una lista de enteros donde el valor absoluto representa el tamaño
                   del asteroide y el signo su dirección (positivo para derecha,
                   negativo para izquierda).

    Returns:
        Una lista de enteros representando el estado final de los asteroides
        después de todas las colisiones.
    """
    resultado = []
    for asteroide_actual in asteroids:
        # Mientras haya un asteroide por procesar
        while asteroide_actual is not None:
            # No hay colisión si el resultado está vacío, si el último asteroide
            # va a la izquierda, o si el nuevo va a la derecha.
            if not resultado or resultado[-1] < 0 or asteroide_actual > 0:
                resultado.append(asteroide_actual)
                break # Pasamos al siguiente asteroide de la lista original

            # Si llegamos aquí, hay una posible colisión:
            # resultado[-1] > 0 (derecha) y asteroide_actual < 0 (izquierda)
            ultimo_asteroide = resultado.pop() # Sacamos el último para ver qué pasa
            
            sobreviviente = resolver_colision(asteroide_actual, ultimo_asteroide)

            if sobreviviente is None:
                # Ambos se destruyeron, no hacemos nada y pasamos al siguiente asteroide.
                break
            elif sobreviviente == ultimo_asteroide:
                # El nuevo se destruyó, el que estaba sobrevive. Lo devolvemos a la lista.
                resultado.append(ultimo_asteroide)
                break
            else: # sobreviviente == asteroide_actual
                # El que estaba se destruyó. El nuevo sobrevive y debe seguir
                # colisionando con los que queden en la lista de resultado.
                asteroide_actual = sobreviviente
                # El bucle 'while' se repetirá para comparar con el nuevo último asteroide.

    return resultado

# Ejemplos de prueba
print(f"Entrada: [5, 10, -5], Salida: {asteroid_collision([5, 10, -5])}")  # Esperado: [5, 10]
print(f"Entrada: [8, -8], Salida: {asteroid_collision([8, -8])}")      # Esperado: []
print(f"Entrada: [10, 2, -5], Salida: {asteroid_collision([10, 2, -5])}") # Esperado: [10]
print(f"Entrada: [-2, -1, 1, 2], Salida: {asteroid_collision([-2, -1, 1, 2])}") # Esperado: [-2, -1, 1, 2]
print(f"Entrada: [-2, 1, -1, 2], Salida: {asteroid_collision([-2, 1, -1, 2])}") # Esperado: [-2, 2]
