import socket

# Configuración del cliente
HOST = '127.0.0.1'  # localhost
PORT = 5000

def connect_to_server():
    """Establecemos conexión con el servidor"""
    try:
        # Configuración del socket TCP/IP del cliente
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print(f"Conectado al servidor {HOST}:{PORT}")
        return client_socket
    except ConnectionRefusedError:
        print("Error: No se pudo conectar al servidor. Verifique que esté ejecutándose.")
        return None
    except Exception as e:
        print(f"Error conectando al servidor: {e}")
        return None

def send_messages(client_socket):
    """Envía múltiples mensajes al servidor hasta que el usuario escriba 'exit'"""
    print("Escribí tus mensajes (escribí 'exit' para salir):")
    
    try:
        while True:
            # Solicitamos un mensaje al usuario
            message = input("Mensaje: ")
            
            # Verificar condición de salida
            if message.lower() == 'exit':
                print("Desconectando del servidor...")
                break
            
            # Enviamos el mensaje al servidor
            client_socket.send(message.encode('utf-8'))
            
            # Recibimos y mostramos la respuesta del servidor
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Respuesta del servidor: {response}")
            
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario")
    except Exception as e:
        print(f"Error enviando mensajes: {e}")

def main():
    """Función principal del cliente"""
    # Conectamos al servidor
    client_socket = connect_to_server()
    if client_socket is None:
        return
    
    try:
        # Lllamos a la función para enviar mensajes
        send_messages(client_socket)
    finally:
        # Cerramos la conexión
        client_socket.close()
        print("Conexión cerrada")

if __name__ == "__main__":
    main()