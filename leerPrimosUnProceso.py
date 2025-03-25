import csv
import math
import time  # Importamos el módulo time para medir el tiempo
import matplotlib.pyplot as plt  # Para graficar los tiempos de ejecución

# Función para verificar si un número es primo
def es_primo(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Función principal para leer el archivo CSV y contar los números primos
def contar_primos_csv(archivo_csv):
    primos = 0
    try:
        with open(archivo_csv, newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                # Convertir cada elemento de la fila en un número
                for valor in fila:
                    try:
                        numero = int(valor)
                        if es_primo(numero):
                            primos += 1
                    except ValueError:
                        # Si el valor no es un número, lo ignoramos
                        continue
    except FileNotFoundError:
        print(f"El archivo {archivo_csv} no fue encontrado.")
        return 0

    return primos

# Uso del programa
archivo_csv = 'numeros_aleatorios.csv'  # Cambia esta ruta por la del archivo que desees usar

# Lista para almacenar los tiempos de ejecución
tiempos_ejecucion = []

# Repetir el proceso 10 veces
for i in range(10):
    # Medir el tiempo de ejecución
    inicio = time.time()  # Tiempo de inicio

    # Contar los números primos
    numero_primos = contar_primos_csv(archivo_csv)

    # Medir el tiempo de finalización
    fin = time.time()  # Tiempo de finalización

    # Calcular el tiempo total que ha tardado en contar los primos
    tiempo_total = fin - inicio
    tiempos_ejecucion.append(tiempo_total)

    print(f"Iteración {i + 1}: El número de números primos en el archivo es: {numero_primos}")
    print(f"Iteración {i + 1}: Tiempo total de ejecución: {tiempo_total:.4f} segundos")

# Graficar los tiempos de ejecución
plt.plot(range(1, 11), tiempos_ejecucion, marker='o', linestyle='-', color='b', label='Tiempo de ejecución (s)')
plt.axhline(y=sum(tiempos_ejecucion) / len(tiempos_ejecucion), color='r', linestyle='--', label=f'Media: {sum(tiempos_ejecucion)/len(tiempos_ejecucion):.4f} s')
plt.xlabel("Iteración")
plt.ylabel("Tiempo (segundos)")
plt.title("Tiempo de ejecución por iteración")
plt.legend()
plt.grid(True)
plt.show()

