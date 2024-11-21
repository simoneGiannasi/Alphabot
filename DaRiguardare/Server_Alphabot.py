import AlphaBot
import socket
import threading

alphabot = AlphaBot.AlphaBot()

# Impostazioni del server
server_ip = "192.168.1.124"
server_port = 12345
buffer_size = 1024
server_address = (server_ip, server_port)

tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind(server_address)
tcp_server_socket.listen(5)

def handle_command(command):
    """Esegue il comando ricevuto dal client."""
    if command == 'FORWARD':
        alphabot.forward()
    elif command == 'BACKWARD':
        alphabot.backward()
    elif command == 'LEFT':
        alphabot.left()
    elif command == 'RIGHT':
        alphabot.right()
    elif command == 'FORWARD_RIGHT':
        alphabot.forward_right()  # Deve essere definito in AlphaBot
    elif command == 'FORWARD_LEFT':
        alphabot.forward_left()
    elif command == 'BACKWARD_RIGHT':
        alphabot.backward_right()
    elif command == 'BACKWARD_LEFT':
        alphabot.backward_left()
    elif command == 'STOP':
        alphabot.stop()
    print(f"Comando eseguito: {command}")

def connection_listener(conn, client_address):
    """Gestisce la connessione con il client."""
    try:
        while True:
            data = conn.recv(buffer_size)
            if not data:
                break
            command = data.decode().strip()
            handle_command(command)
    except Exception as e:
        print(f"Errore nel listener per {client_address}: {e}")
    finally:
        alphabot.stop()
        conn.close()
        print(f"Connessione chiusa per {client_address}")

def main():
    print(f"Server in ascolto su {server_ip}:{server_port}")
    
    try:
        while True:
            conn, client_address = tcp_server_socket.accept()
            print(f"Connessione accettata da {client_address}")
            connection_listener(conn, client_address)
    except KeyboardInterrupt:
        print("\nServer interrotto manualmente.")
    finally:
        tcp_server_socket.close()
        print("Socket del server chiusa.")

if __name__ == "__main__":
    main()
