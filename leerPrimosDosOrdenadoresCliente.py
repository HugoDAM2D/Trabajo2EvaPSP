import socket
import pickle
import time

SERVER_IP = '10.20.20.100'  # Dirección IP del servidor
SERVER_PORT = 65432         # Puerto del servidor

# Función que verifica si un número es primo
def es_un_primo(numero):
    if numero <= 1:
        return False
    for divisor in range(2, int(numero ** 0.5) + 1):
        if numero % divisor == 0:
            return False
    return True

# Función para procesar los números y contar los primos
def procesar_numeros(numeros_lista):
    primos = 0
    for num in numeros_lista:
        if es_un_primo(num):
            primos += 1
    return primos

# Función que gestiona la comunicación con el servidor
def ejecutar_cliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        cliente_socket.connect((SERVER_IP, SERVER_PORT))
        print("Conexión con el servidor establecida")

        # Recepción del tamaño de los datos del servidor
        longitud_de_datos = int.from_bytes(cliente_socket.recv(4), 'big')

        # Recepción de los datos en fragmentos
        datos_completos = b""
        while len(datos_completos) < longitud_de_datos:
            fragmento = cliente_socket.recv(4096)  # Leer los fragmentos
            if not fragmento:
                break
            datos_completos += fragmento

        # Deserializar los datos recibidos
        numeros_a_procesar = pickle.loads(datos_completos)

        # Procesar los números
        cantidad_repeticiones = 10
        tiempos_ejecucion = []
        for i in range(cantidad_repeticiones):
            inicio_tiempo = time.time()
            primos_encontrados = procesar_numeros(numeros_a_procesar)  # Contar primos
            fin_tiempo = time.time()
            tiempos_ejecucion.append(fin_tiempo - inicio_tiempo)
            print(f"Repetición {i + 1}: Se hallaron {primos_encontrados} números primos")
            print(f"Tiempo de ejecución para repetición {i + 1}: {fin_tiempo - inicio_tiempo:.5f} segundos")

        # Enviar el total de primos encontrados al servidor
        total_primos = primos_encontrados
        cliente_socket.sendall(str(total_primos).encode())

if __name__ == "__main__":
    ejecutar_cliente()

