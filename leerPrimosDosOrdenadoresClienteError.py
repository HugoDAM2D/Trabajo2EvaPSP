import socket

def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Configuración del cliente
HOST = '10.20.20.100'  # Dirección IP del servidor
PORT = 65432

# Conectar al servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Recibir los datos del servidor (números para procesar)
    datos = b""
    while True:
        parte = s.recv(4096)  # Usamos un buffer más grande
        datos += parte
        if len(parte) < 4096:  # Si recibimos menos de lo esperado, la conexión se cerró
            break

    print(f"Datos recibidos del servidor: {datos.decode()}")  # Para depuración

    # Convertir los datos a una lista de números
    if datos.strip():
        numeros = list(map(int, datos.decode().split(',')))  # Convertir la cadena en lista de números
    else:
        numeros = []

    # Encontrar los

