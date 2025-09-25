def imprimir_vocales_por_palabra(lista_palabras):
    # Para cada palabra, imprime las vocales que contiene.
    vocales = "aeiouAEIOU"
    for palabra in lista_palabras:
        vocales_encontradas = []
        for letra in palabra:
            if letra in vocales and letra not in vocales_encontradas:
                vocales_encontradas.append(letra)
        print("Palabra:", palabra, "Vocales:", ", ".join(vocales_encontradas))
