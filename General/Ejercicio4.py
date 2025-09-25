n = int(input("Cantidad de palabras: "))  # Pide cantidad de palabras
palabras = []  # Lista para almacenar las palabras

for _ in range(n):
    palabra = input("Introduce una palabra: ")  # Lee palabra
    palabras.append(palabra)  # Agrega a la lista

tupla_palabras = tuple(palabras)  # Convierte la lista en una tupla inmutable

pos = int(input(f"Introduce una posición entre 0 y {n-1}: "))  # Pide índice para mostrar
if 0 <= pos < n:  # Valida rango del índice introducido
    print("Palabra en la posición", pos, "es:", tupla_palabras[pos])  # Imprime palabra en la posición
else:
    print("Posición fuera de rango")  # Mensaje si el índice es inválido
