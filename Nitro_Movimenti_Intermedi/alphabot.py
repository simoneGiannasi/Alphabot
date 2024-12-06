import socket
import alphaLib

def direzione(comandi):
    # Inizializza i valori di velocità
    right = 0
    left = 0

    # Analizza i comandi ricevuti
    for comando in comandi:
        if comando == "w":  # Avanti
            right = 50
            left = -50
        elif comando == "s":  # Indietro
            right = -50
            left = 50
        elif comando == "a":  # Sinistra
            right = 20  # Riduce la velocità della ruota destra
            left = -50   # Mantiene la velocità della ruota sinistra
        elif comando == "d":  # Destra
            right = 50   # Mantiene la velocità della ruota destra
            left = -20    # Riduce la velocità della ruota sinistra

    # Imposta i motori con i valori calcolati
    alpha.setMotor(left, right)

# Impostazione dell'indirizzo del server
alphabot_address = ("192.168.1.124", 12345)

# Creazione del socket TCP del server
alphabot_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alphabot_tcp.bind(alphabot_address)
alphabot_tcp.listen(1)
print("Server AlphaBot in ascolto...")

alpha = alphaLib.AlphaBot()
try:
    while True:
        client, address = alphabot_tcp.accept()
        print(f"Connessione accettata da {address}")
        while True:
            messaggio = client.recv(4096).decode('utf-8')
            if messaggio:
                if messaggio == 'end':
                    print("Chiusura connessione...")
                    client.close()
                    break
                comandi = messaggio.split(",")  # Splitta i comandi
                direzione(comandi)
                print(f"Comando ricevuto: {messaggio}")
            else:
                break  # Chiude la connessione se non ci sono più messaggi
finally:
    alphabot_tcp.close()