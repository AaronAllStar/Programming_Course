n = int(input("Cantidad de palabras: "))  # Pide cantidad de palabras a leer
palabras = []  # Lista para almacenar palabras

for _ in range(n):
    palabra = input("Introduce una palabra: ")  # Lee palabra
    palabras.append(palabra)  # Agrega a la lista

palabra_mas_larga = max(palabras, key=len)  # Busca palabra con longitud máxima
print("La palabra más larga es:", palabra_mas_larga)  # Imprime la palabra más larga
