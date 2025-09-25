numeros = []  # Lista para almacenar números

for i in range(5):
    num = int(input(f"Introduce número {i+1}: "))  # Lee número
    numeros.append(num)  # Lo agrega a la lista

print("Número mayor:", max(numeros))  # Imprime el mayor
print("Número menor:", min(numeros))  # Imprime el menor
