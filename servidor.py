import socket
import sqlite3
from datetime import datetime

# -----------------------------------------
# Función para inicializar el socket TCP/IP
# -----------------------------------------
def inicializar_servidor(host='localhost', puerto=5000):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reutilizar el puerto si el servidor se reinicia rápido
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        servidor.bind((host, puerto))  # Asocia el socket a la IP y puerto
        servidor.listen()  # Se pone en modo escucha
        print(f"Servidor escuchando en {host}:{puerto}")
        return servidor
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
        exit(1)

# -------------------------------------------------------------------
# Función para guardar el mensaje en la base de datos SQLite local
# -------------------------------------------------------------------
def guardar_mensaje(contenido, ip_cliente):
    try:
        # Conexión a la base de datos (se crea si no existe) en el entorno actual
        # Se usa 'mensajes.db' como nombre de archivo para la base de datos
        conexion = sqlite3.connect('mensajes.db')
        cursor = conexion.cursor()

        # Crea la tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT,
                fecha_envio TEXT,
                ip_cliente TEXT
            )
        ''')

        # Insertar el mensaje con fecha actual
        fecha = datetime.now().isoformat()
        cursor.execute("INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
                       (contenido, fecha, ip_cliente))

        # Guardar cambios y cerrar conexión
        conexion.commit()
        conexion.close()
        return fecha
    except Exception as e:
        print(f"Error al guardar mensaje en la DB: {e}")
        return None

# -----------------------------------------------------
# Función que acepta conexiones y procesa los mensajes
# -----------------------------------------------------
def aceptar_conexiones(servidor):
    while True:
        # Espera a que se conecte un cliente
        cliente, direccion = servidor.accept()
        print(f"Conexión recibida de {direccion}")
        while True:
            try:
                # Recibe mensaje del cliente
                mensaje = cliente.recv(1024).decode()
                if not mensaje:
                    break
                print(f"Mensaje recibido: {mensaje}")

                # Guarda el mensaje y obtiene timestamp
                timestamp = guardar_mensaje(mensaje, direccion[0])

                # Responde al cliente con confirmación
                if timestamp:
                    respuesta = f"Mensaje recibido: {timestamp}"
                else:
                    respuesta = "Error al guardar mensaje"

                cliente.send(respuesta.encode())
            except Exception as e:
                print(f"Error durante la conexión: {e}")
                break
        cliente.close()

# --------------------------
# Punto de entrada principal
# --------------------------
if __name__ == '__main__':
    servidor = inicializar_servidor()
    aceptar_conexiones(servidor)
