def imprimir_promedio(lista_numeros):
    # Calcula e imprime el promedio de una lista de números.
    if len(lista_numeros) == 0:
        print("La lista está vacía.")
        return
    promedio = sum(lista_numeros) / len(lista_numeros)
    print("El promedio es:", promedio)
