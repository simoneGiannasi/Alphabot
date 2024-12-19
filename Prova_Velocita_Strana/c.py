import socket
from pynput import keyboard

# Tasti concessi
tastiConcessi = ["w", "a", "s", "d"]
tastiPremuti = set()  # Usato un set per evitare duplicati

# Definizione dell'indirizzo del server
server_tcp_address = ("192.168.1.122", 22222)

# Creazione del socket TCP del client
client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_tcp.connect(server_tcp_address)

# Funzione per inviare il comando al server
def invia_comando(messaggio):
    client_tcp.send(messaggio.encode('utf-8'))

# Funzione per gestire la pressione dei tasti
def gestione_congestione_on_press(key):
    if key not in tastiPremuti:
        tastiPremuti.add(key)  # Aggiungi il tasto alla lista
        invia_comando("".join(sorted(tastiPremuti)))  # Invia i tasti premuti come stringa concatenata

# Funzione per gestire il rilascio dei tasti
def gestione_congestione_on_release(key):
    if key in tastiPremuti:
        tastiPremuti.remove(key)  # Rimuovi il tasto dalla lista
        if tastiPremuti:
            invia_comando("".join(sorted(tastiPremuti)))  # Invia i tasti rimanenti concatenati
        else:
            invia_comando("stop")  # Se non ci sono tasti premuti, invia il comando "stop"
# Funzione per gestire i tasti premuti
def on_press(key):
    try:
        if key.char in tastiConcessi:
            gestione_congestione_on_press(key.char)
    except AttributeError:
        # Gestione dei tasti speciali come ESC o DEL
        if key == keyboard.Key.esc or key == keyboard.Key.delete:
            invia_comando("end")  # Invia comando di fine connessione

def on_release(key):
    try:
        if key.char in tastiConcessi:
            gestione_congestione_on_release(key.char)
    except AttributeError:
        pass

# Listener per i tasti premuti
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Chiude la connessione TCP al termine del listener
client_tcp.close()
