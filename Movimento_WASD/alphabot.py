import socket
import alphaLib


# L'alphabot è il nostro server
# Creazione del socket TCP
alphabot_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Definizione dell'indirizzo del server (IP e porta)
alphabot_address = ("192.168.1.129", 34512)

# Associazione del socket all'indirizzo del server
alphabot_tcp.bind(alphabot_address)

# Imposta il server in modalità di ascolto per le connessioni in ingresso
alphabot_tcp.listen(1)
print("Server AlphaBot in ascolto...")

alpha = alphaLib.AlphaBot()
# Loop principale che accetta le connessioni dal client
try:
    while True:
        # Accetta la connessione del client
        client, address = alphabot_tcp.accept()
        print(f"Connessione accettata da {address}")

        # Riceve i comandi dal client
        while True:
            messaggio = client.recv(4096).decode('utf-8')
            if not messaggio:
                break  # Chiude la connessione se non ci sono più messaggi

            print(f"Comando ricevuto: {messaggio}")
            # Interpretazione dei comandi per muovere l'AlphaBot
            if 'w' in messaggio:
                alpha.forward()  # Avanti
            elif 'a' in messaggio:
                alpha.left()     # Sinistra
            elif 'd' in messaggio:
                alpha.right()    # Destra
            elif 's' in messaggio:
                alpha.backward() # Indietro
            elif 'stop' in messaggio:
                alpha.stop()     # Stop
            elif 'end' in messaggio:
                print("Chiusura connessione...")
                client.close()         # Chiude la connessione al client
                break
            else:
                print("Comando non riconosciuto.")

except KeyboardInterrupt:
    print("Server interrotto manualmente.")
finally:
    # Chiude il socket del server
    alphabot_tcp.close()
    print("Server chiuso.")
