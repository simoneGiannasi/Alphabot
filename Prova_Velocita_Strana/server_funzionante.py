import socket
import AlphaBot

def direzione(messaggio):
    if "w" in messaggio and "d" in messaggio:
        # Avanti e gira a destra
        left = -40
        right = 70
    elif "w" in messaggio and "a" in messaggio:
        # Avanti e gira a sinistra
        left = -70
        right = 40
    elif "s" in messaggio and "d" in messaggio:
        # Indietro e gira a destra
        left = 90
        right = -20
    elif "s" in messaggio and "a" in messaggio:
        # Indietro e gira a sinistra
        left = 20
        right = -90
    elif "w" in messaggio:
        # Solo avanti
        left = -50
        right = 50
    elif "s" in messaggio:
        # Solo indietro
        left = 50
        right = -50
    elif "a" in messaggio:
        # Solo sinistra
        left = -30
        right = 0
    elif "d" in messaggio:
        # Solo destra
        left = 0
        right = 30
    else:
        # Stop, nel caso di comando non valido
        left = 0
        right = 0
    alpha.setMotor(left, right)

alpha = AlphaBot.AlphaBot()
tastiConcessi = ["w", "a", "s", "d"]
alphabot_address = ("192.168.1.122", 22222)
alpha.stop()  # Ferma il robot all'inizio
alphabot_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alphabot_tcp.bind(alphabot_address)
alphabot_tcp.listen(1)
print("Server AlphaBot in ascolto...")

try:
    while True:
        client, address = alphabot_tcp.accept()
        print(f"Connessione accettata da {address}")
        last_message = None  # Variabile per tenere traccia dell'ultimo comando valido ricevuto

        while True:
            messaggio = client.recv(4096).decode('utf-8')
            if messaggio == 'stop':
                # Comando di stop
                print("Ricevuto comando 'stop', fermo i motori...")
                alpha.stop()  # Ferma il robot
                print("Motori fermati.")
                last_message = None  # Se riceviamo 'stop', resettiamo il comando
            elif messaggio == 'end':
                print("Chiusura connessione...")
                client.close()
                break
            elif messaggio in tastiConcessi or any(k in messaggio for k in tastiConcessi):
                # Gestiamo i comandi di movimento
                direzione(messaggio)
                print(f"Comando ricevuto: {messaggio}")
                last_message = messaggio  # Salviamo l'ultimo comando valido ricevuto
            elif last_message is None:
                # Se non c'è alcun comando, fermiamo il robot
                print("Nessun comando ricevuto, fermo il robot.")
                alpha.stop()

except KeyboardInterrupt:
    print("Server interrotto manualmente.")
finally:
    alphabot_tcp.close()
    print("Server chiuso.")
