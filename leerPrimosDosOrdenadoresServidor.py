import socket
import pickle
import time
import matplotlib.pyplot as plt

# Dirección IP y puerto del servidor
IP_SERVIDOR = '10.20.20.100'
PUERTO_SERVIDOR = 65432

def servidor_calculos():
    """Función principal del servidor que maneja la conexión y procesamiento de datos."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        # Configuración del servidor
        servidor_socket.bind((IP_SERVIDOR, PUERTO_SERVIDOR))
        servidor_socket.listen(1)
        print(f"Esperando conexión en {IP_SERVIDOR}:{PUERTO_SERVIDOR}...")

        # Esperando que el cliente se conecte
        cliente_conn, cliente_addr = servidor_socket.accept()
        with cliente_conn:
            print(f"Conexión establecida con {cliente_addr}")

            # Cargar los números aleatorios desde un archivo CSV
            with open('numeros_aleatorios.csv', 'r') as archivo_numeros:
                numeros_lista = [int(numero) for numero in archivo_numeros.read().split(',')]

            print(f"Primeros 10 números cargados: {numeros_lista[:10]}...")

            # Serialización de los datos y envío
            datos_serializados = pickle.dumps(numeros_lista)
            cliente_conn.sendall(len(datos_serializados).to_bytes(4, 'big'))  # Enviar el tamaño de los datos
            cliente_conn.sendall(datos_serializados)  # Enviar los datos serializados

            # Lista para almacenar los tiempos de cada iteración
            tiempos_respuesta = []
            for iteracion in range(10):
                tiempo_inicio_iteracion = time.time()  # Iniciar el conteo de tiempo para esta iteración

                # Recibir respuesta del cliente (número de primos encontrados)
                respuesta_cliente = cliente_conn.recv(1024).decode().strip()

                # Si no se recibió respuesta, asignar "0"
                if not respuesta_cliente:
                    respuesta_cliente = "0"

                primos_encontrados = int(respuesta_cliente)
                tiempo_total_iteracion = time.time() - tiempo_inicio_iteracion  # Calcular el tiempo de la iteración

                # Almacenar el tiempo de esta iteración
                tiempos_respuesta.append(tiempo_total_iteracion)

                print(f"Iteración {iteracion + 1}: {primos_encontrados} primos encontrados en {tiempo_total_iteracion:.5f} segundos")

            # Crear y mostrar la gráfica con los tiempos de cada iteración
            plt.plot(range(1, 11), tiempos_respuesta, marker='x', linestyle='-', color='purple', label='Tiempo de cálculo por iteración (segundos)')
            plt.axhline(y=sum(tiempos_respuesta) / len(tiempos_respuesta), color='orange', linestyle='--', label=f'Media: {sum(tiempos_respuesta)/len(tiempos_respuesta):.5f} s')
            plt.xlabel("Iteración")
            plt.ylabel("Tiempo (segundos)")
            plt.title("Tiempo de ejecución por iteración")
            plt.legend()
            plt.grid(True)
            plt.show()

if __name__ == "__main__":
    servidor_calculos()

