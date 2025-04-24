import socket

# -----------------------------------------
# Función para iniciar el cliente TCP/IP
# -----------------------------------------
def iniciar_cliente(host='localhost', puerto=5000):
    # Crear el socket del cliente
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Intentar conectarse al servidor
        cliente.connect((host, puerto))
        print("Conectado al servidor.")
    except Exception as e:
        print(f"No se pudo conectar: {e}")
        return

    # Bucle para enviar múltiples mensajes hasta escribir "éxito"
    while True:
        mensaje = input("Ingresá un mensaje (o escribí 'éxito' para salir): ")
        #Forzar que exito exista en minusculas y que puede no tener tilde!
        if mensaje.lower() in ['éxito', 'exito']:
            break

        # Enviar mensaje al servidor
        cliente.send(mensaje.encode())

        # Recibir y mostrar respuesta del servidor
        respuesta = cliente.recv(1024).decode()
        print(f"Respuesta del servidor: {respuesta}")

    # Cerrar conexión con el servidor
    cliente.close()

# --------------------------
# Punto de entrada principal
# --------------------------
if __name__ == '__main__':
    iniciar_cliente()
