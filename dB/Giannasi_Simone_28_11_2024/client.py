import socket 

PORTA = 12345
server_address = ("localhost", PORTA)
BUFFER_SIZE = 4096


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creo la connessione al server attraverso un socket sulla porta 12345
    client_socket.connect(server_address) # Mi connetto al server

    while True:
        operazione = client_socket.recv(BUFFER_SIZE).decode('utf-8') # Ricevo l'operazione che devo fare dal server
        
        if operazione == "exit": # se è exit esco e chiudo la connessione
            break

        try:
            risultato = eval(operazione) # eseguo l'operazione con la funzione eval
            client_socket.send(str(risultato).encode('utf-8')) #mando il risultato al server
        except Exception as e:
            client_socket.send(str(e).encode('utf-8'))

    client_socket.close()




if __name__ == "__main__":
    main()