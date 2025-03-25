import socket
import csv
import time

def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Configuración del servidor
HOST = '0.0.0.0'  # Escucha en todas las interfaces de red
PORT = 65432

# Leer el CSV sin imprimir los números
numeros = []
with open('numeros_aleatorios.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        for item in row:
            try:
                numeros.append(int(item.strip()))  # Convertir a entero y limpiar espacios
            except ValueError:
                pass  # Ignorar valores no numéricos sin imprimir nada

# Dividir los números en dos partes
mitad = len(numeros) // 2
numeros_servidor = numeros[:mitad]
numeros_cliente = numeros[mitad:]

# Iniciar conteo en el servidor
inicio = time.time()
primos_servidor = [num for num in numeros_servidor if es_primo(num)]

# Configurar el socket y enviar datos al cliente
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print("Esperando conexión del cliente...")
    conn, addr = s.accept()
    with conn:
        print(f"Cliente conectado desde {addr}")

        try:
            # Enviar la lista de números al cliente
            conn.sendall(','.join(map(str, numeros_cliente)).encode())
            print("Datos enviados al cliente...")

            # Recibir la respuesta del cliente en fragmentos
            datos_cliente = b""
            while True:
                parte = conn.recv(4096)  # Leer fragmentos de 4096 bytes
                if not parte:
                    break
                datos_cliente += parte
            print("Datos recibidos del cliente")

            # Convertir los datos a la lista de primos
            if datos_cliente.strip():
                primos_cliente = list(map(int, datos_cliente.decode().split(',')))
            else:
                primos_cliente = []

            # Mostrar resultados
            total_primos = primos_servidor + primos_cliente
            print(f"Cantidad total de primos: {len(total_primos)}")
            print(f"Tiempo total: {time.time() - inicio:.4f} segundos")

        except Exception as e:
            print(f"Error en la comunicación con el cliente: {e}")

