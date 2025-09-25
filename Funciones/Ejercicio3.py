def imprimir_max_min(lista_numeros):
    # Imprime el número máximo y mínimo de una lista.
    if len(lista_numeros) == 0:
        print("La lista está vacía.")
        return
    maximo = max(lista_numeros)
    minimo = min(lista_numeros)
    print("El número más grande es:", maximo)
    print("El número más pequeño es:", minimo)
