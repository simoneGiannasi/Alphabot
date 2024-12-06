import socket
from pynput import keyboard

# Definizione dei tasti consentiti
tastiConcessi = ["w", "a", "s", "d"]
tasti_speciali = ["i", "o", "p"]
tastiPremuti = []
left = 0
right = 0



def main():
    # Indirizzo del server
    server_tcp_address = ("localhost", 12345)
    try:
        # Creazione del socket TCP del client
        client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_tcp.connect(server_tcp_address)
        print("Connected to Alphabot")
        # Listener per la tastiera
        with keyboard.Listener(on_press=lambda key: on_press(key, client_tcp),
                               on_release=lambda key: on_release(key, client_tcp)) as listener:
            listener.join()  # Mantiene il listener attivo finché non viene fermato
    except ConnectionRefusedError:
        print("Connection to Alphabot refused")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'client_tcp' in locals(): # verifico che la variabile client_tcp sia tra le variabili definite
            client_tcp.close() 
            print("Connection closed.")



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
            tcp_client.recv()
            return False



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
        pass  # Ignora tasti speciali come Ctrl, Alt, ecc.



if __name__ == '__main__':
    main()