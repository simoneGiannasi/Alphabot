import socket
from pynput import keyboard
import time
import threading

# Definizione dei tasti consentiti
tastiConcessi = ["w", "a", "s", "d"]
tasti_speciali = ["i", "o", "p"]
tastiPremuti = []
left = 0
right = 0
BUFFER_SIZE = 4092
is_connected = True



def main():
    # Indirizzo del server
    global is_connected
    server_tcp_address = ("localhost", 12345)
    try:
        # Creazione del socket TCP del client
        client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_tcp.connect(server_tcp_address)
        print("Connected to Alphabot")

        # Thread per il heartbeat   
        heartbeat_thread = threading.Thread(target=send_heartbeat, args=(client_tcp,))
        heartbeat_thread.start()

        # Listener per la tastiera
        with keyboard.Listener(on_press=lambda key: on_press(key, client_tcp),
                               on_release=lambda key: on_release(key, client_tcp)) as listener:
            listener.join()  # Mantiene il listener attivo finché non viene fermato
    except ConnectionRefusedError:
        print("Connection to Alphabot refused")
    
    
    #finally:
    #   if 'client_tcp' in locals(): # verifico che la variabile client_tcp sia tra le variabili definite
    #       client_tcp.close() 
    #       print("Connection closed.")

    except (socket.error, ConnectionResetError, KeyboardInterrupt):
        print("Chiusura client")
    finally:
        is_connected = False  # Imposta il flag a False per fermare il thread di heartbeat
        heartbeat_thread.join()
        client_tcp.close()
        print("Socket chiuso.")

def send_heartbeat(client_tcp_socket):
    """Invia l'heartbeat al server a intervalli regolari."""
    global is_connected
    while is_connected:
        try:
            client_tcp_socket.send("HEARTBEAT".encode("utf-8"))
            time.sleep(1)
        except (socket.error, ConnectionResetError):
            print("Connessione persa con il server.")
            is_connected = False  # Imposta il flag a False in caso di errore
            break


def on_press(key,tcp_client):
    try:
        if key.char in tastiConcessi and key.char not in tastiPremuti:
            tastiPremuti.append(key.char)
            global left, right
            if key.char == "w":
                right += 50
                left -= 50
            elif key.char == "s":
                right -= 50
                left += 50
            elif key.char == "a":
                if "s" in tastiPremuti:
                    left += 30
                else:
                    left -= 30
            elif key.char == "d":
                if "s" in tastiPremuti:
                    right -= 30
                else:
                    right += 30
            tcp_client.send(f"{left},{right}".encode("utf-8"))

        elif key.char == "n" and key.char not in tastiPremuti: # N è nitro (come easter egg)
            tastiPremuti.append(key.char)
            tcp_client.send("-100,100".encode("utf-8"))

        elif key.char in tasti_speciali and key.char not in tastiPremuti:
            tastiPremuti.append(key.char)
            tcp_client.send((key.char).encode("utf-8"))

    except AttributeError:
        if key == keyboard.Key.esc:
            tcp_client.send("end".encode("utf-8"))
            tcp_client.recv(BUFFER_SIZE)
            return False
        print("Invalid")



def on_release(key,tcp_client):
    try:
        if key.char in tastiConcessi and key.char in tastiPremuti:
            tastiPremuti.remove(key.char)
            global left, right
            if key.char == "w":
                right -= 50
                left += 50
            elif key.char == "s":
                right += 50
                left -= 50
            elif key.char == "a":
                if "s" in tastiPremuti:
                    left -= 30
                else:
                    left += 30
            elif key.char == "d":
                if "s" in tastiPremuti:
                    right += 30
                else:
                    right -= 30
            tcp_client.send(f"{left},{right}".encode("utf-8"))

        elif key.char == "n" and key.char in tastiPremuti:
            tastiPremuti.remove(key.char)
            tcp_client.send("0,0".encode("utf-8"))

        elif key.char in tasti_speciali and key.char in tastiPremuti:
            tastiPremuti.remove(key.char)
            tcp_client.send("0,0".encode("utf-8"))
            
    except AttributeError:
        print("Invalid")
        


if __name__ == '__main__':
    main()