total_pares = 0  # Inicializa acumulador para suma de pares

while True:
    num = int(input("Introduce un número (-1 para terminar): "))  # Lee número por teclado
    if num == -1:  # Condición para terminar la lectura
        break
    if num % 2 == 0:  # Comprueba si número es par
        total_pares += num  # Acumula el número par 

print("Suma total de números pares:", total_pares)  # Muestra la
