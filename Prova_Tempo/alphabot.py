import socket
#import alphaLib

# Impostazione dell'indirizzo del server
alphabot_address = ("localhost", 12345)


def main():
    # Creazione del socket TCP del server
    alphabot_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alphabot_tcp.bind(alphabot_address)
    alphabot_tcp.listen(1)
    print("Server AlphaBot in ascolto...")
    #alpha = alphaLib.AlphaBot()
    
    try:
        #alpha.setMotor(0, 0)
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
                    if len(comandi) == 2:
                        left = comandi[0]
                        right = comandi[1]
                        print(f"Comando ricevuto: {left},{right}")
                        #alpha.setMotor(left, right)
                    else:
                        print(comandi)
                else:
                    break  # Chiude la connessione se non ci sono più messaggi
    finally:
        alphabot_tcp.close()



if __name__ == '__main__':
    main()