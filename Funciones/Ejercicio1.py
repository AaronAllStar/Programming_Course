def calcular_pendiente(x1, y1, x2, y2):
    # Calcula la pendiente entre dos puntos (x1,y1) y (x2,y2).
    if x2 == x1:
        print("No se puede calcular la pendiente porque la recta es vertical.")
        return None
    pendiente = (y2 - y1) / (x2 - x1)
    print("La pendiente es:", pendiente)
    return pendiente
