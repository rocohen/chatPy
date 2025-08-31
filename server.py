import socket
import threading
from datetime import datetime
from database import init_database, save_message, check_database_access

# Configuración del servidor
HOST = '127.0.0.1'  # localhost
PORT = 5000

def initialize_socket():
    """Inicializamos el socket del servidor con manejo de errores"""
    try:
        # Configuración del socket TCP/IP
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reusar el puerto
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"Servidor escuchando en {HOST}:{PORT}")
        return server
    except OSError as e:
        if e.errno == 98 or "La dirección ya está en uso" in str(e):
            print(f"Error: Puerto {PORT} ocupado. Intente con otro puerto o cierre el proceso que lo está usando.")
        else:
            print(f"Error inicializando socket: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado inicializando socket: {e}")
        return None

def handle_client_connection(client_socket, client_address):
    """Aceptamos las conexiones y recibimos los mensajes de un cliente específico"""
    print(f"Nueva conexión desde {client_address}")
    
    try:
        while True:
            # Recibir mensaje del cliente
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message:
                break
                
            print(f"Mensaje recibido de {client_address}: {message}")
            
            # Guardamos el mensaje en la base de datos
            ip_cliente = client_address[0]
            if save_message(message, ip_cliente):
                # Respondemos al cliente con un timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                response = f"Mensaje recibido: {timestamp}"
                client_socket.send(response.encode('utf-8'))
            else:
                # Error guardando en BD
                error_msg = "Error: No se pudo guardar el mensaje"
                client_socket.send(error_msg.encode('utf-8'))
                
    except ConnectionResetError:
        print(f"Cliente {client_address} desconectado abruptamente")
    except Exception as e:
        print(f"Error manejando cliente {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Conexión con {client_address} cerrada")

def accept_connections(server_socket):
    """Aceptamos nuevas conexiones de clientes"""
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            
            # Creamos un hilo separado para manejar cada cliente
            client_thread = threading.Thread(
                target=handle_client_connection, 
                args=(client_socket, client_address)
            )
            client_thread.daemon = True  # El hilo se cierra cuando el programa principal termine
            client_thread.start()
            
        except Exception as e:
            print(f"Error aceptando conexión: {e}")
            break

def main():
    """Función principal del servidor"""
    # Verificamos el acceso a la base de datos
    if not check_database_access():
        print("Error: Base de datos no accesible")
        return
    
    # Verificamos la inicialización de la base de datos
    if not init_database():
        print("Error: No se pudo inicializar la base de datos")
        return
    
    # Inicializamos el socket del servidor
    server_socket = initialize_socket()
    if server_socket is None:
        return
    
    print("Servidor iniciado correctamente. Esperando conexiones...")
    
    try:
        # Llamamos a la función para aceptar conexiones
        accept_connections(server_socket)
    except KeyboardInterrupt:
        print("\nCerrando servidor...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()