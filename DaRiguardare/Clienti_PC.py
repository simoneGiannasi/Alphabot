import socket
from pynput import keyboard

# Impostazioni del client
server_ip = "192.168.1.124"
server_port = 12345
server_address = (server_ip, server_port)

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
is_connected = False
current_command = None
keys_pressed = set()  # Tasti attualmente premuti

def connect():
    global tcp_client_socket, is_connected
    try:
        tcp_client_socket.connect(server_address)
        print(f"Connesso al server {server_ip}:{server_port}")
        is_connected = True
    except Exception as e:
        print(f"Errore di connessione al server: {e}")
        is_connected = False

def send(command):
    """Invia il comando solo se è cambiato rispetto al comando precedente."""
    global is_connected, current_command
    if not is_connected:
        print("Non connesso al server")
        return
    
    try:
        tcp_client_socket.send(command.encode())
        print(f"Inviato comando: {command}")
        current_command = command
    except Exception as e:
        print(f"Errore nell'invio del comando: {e}")
        tcp_client_socket.close()
        is_connected = False

def determine_command():
    """Determina il comando in base ai tasti attualmente premuti."""
    if 'w' in keys_pressed and 'd' in keys_pressed:
        return 'FORWARD_RIGHT'
    elif 'w' in keys_pressed and 'a' in keys_pressed:
        return 'FORWARD_LEFT'
    elif 's' in keys_pressed and 'd' in keys_pressed:
        return 'BACKWARD_RIGHT'
    elif 's' in keys_pressed and 'a' in keys_pressed:
        return 'BACKWARD_LEFT'
    elif 'w' in keys_pressed:
        return 'FORWARD'
    elif 's' in keys_pressed:
        return 'BACKWARD'
    elif 'a' in keys_pressed:
        return 'LEFT'
    elif 'd' in keys_pressed:
        return 'RIGHT'
    else:
        return 'STOP'

def on_press(key):
    try:
        if key.char in ['w', 'a', 's', 'd']:
            keys_pressed.add(key.char)
            command = determine_command()
            if command != current_command:
                send(command)
    except AttributeError:
        pass

def on_release(key):
    try:
        if key.char in ['w', 'a', 's', 'd']:
            keys_pressed.discard(key.char)
            command = determine_command()
            if command != current_command:
                send(command)

        if key == keyboard.Key.esc:
            print("Chiusura del client...")
            return False  # Interrompe l'ascolto della tastiera
    except AttributeError:
        pass

def main():
    connect()
    
    if is_connected:
        # Ascolta gli eventi della tastiera
        try:
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        except Exception as e:
            print(f"Errore nel listener della tastiera: {e}")
    else:
        print("Connessione al server non riuscita.")

    tcp_client_socket.close()
    print("Connessione chiusa")

if __name__ == "__main__":
    main()
