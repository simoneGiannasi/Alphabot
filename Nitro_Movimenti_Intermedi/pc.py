import socket
from pynput import keyboard

# Definizione dei tasti consentiti
tastiConcessi = ["w", "a", "s", "d"]
tastiPremuti = []

# Indirizzo del server
server_tcp_address = ("192.168.1.124", 12345)

# Creazione del socket TCP del client
client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_tcp.connect(server_tcp_address)

def invia_comando():
    if tastiPremuti:
        messaggio = ",".join(tastiPremuti)
    else:
        messaggio = "stop"
    client_tcp.send(messaggio.encode('utf-8'))

def on_press(key):
    try:
        if key.char in tastiConcessi and key.char not in tastiPremuti:
            tastiPremuti.append(key.char)
            invia_comando()
    except AttributeError:
        if key == keyboard.Key.esc or key == keyboard.Key.delete:
            invia_comando()
            client_tcp.send("end".encode('utf-8'))
            return False  # Ferma il listener

def on_release(key):
    try:
        if key.char in tastiConcessi and key.char in tastiPremuti:
            tastiPremuti.remove(key.char)
            invia_comando()
    except AttributeError:
        pass

# Listener per i tasti premuti
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Chiudi la connessione TCP
client_tcp.close()