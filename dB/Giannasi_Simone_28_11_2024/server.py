import socket 
import sqlite3
import threading

PORTA = 12345
server_address = ("localhost", PORTA) # server address che uso per la connessione TCP
BUFFER_SIZE = 4096 # dimensione buffer di informazioni



def carica_dati_dB():
    # Questa funzione la uso per aprire una connessione con il db sqlite3 da cui prendo tutte le tuple che poi passerò ai thread come da traccia
    conn = sqlite3.connect("operations.db",check_same_thread=False)
    cursore = conn.cursor()
    cursore.execute('''SELECT id, client, operation
                    FROM operations''') # Eseguo la select per ricavare le informazioni dal dB
    dati_db = cursore.fetchall()
    conn.close()
    return dati_db

def gestione_client(socket, address, informazioni_db, num_client):
    # Questa funzione è quella del thread che mi permette di comunicare al client l'operazione che deve svolgere in base ai dati del dB
    # Poi aspetta il risultato e lo stampa 
    # Infine chiude la connessione dopo avere dato il comando exit al client
    operazione = None
    for tupla in informazioni_db:
        if tupla[1] == int(num_client):
            operazione = str(tupla[2]) # Prendo l'operazione nelle informazioni del dB e la mando al client che la esegue
            operazione_filtrata = ''.join(carattere for carattere in operazione if carattere in "1234567890+-/*") # se l'operazione non è exit allora la filtro per non avere caratteri sconosciuti (solo numeri e operazioni)

            socket.send(operazione_filtrata.encode('utf-8'))
            risultato_thread = socket.recv(BUFFER_SIZE).decode('utf-8')
            print (f"{operazione_filtrata} = {risultato_thread} from {address[0]} - {address[1]}") #stampo il risultato
    socket.send("exit".encode('utf-8'))
    socket.close()

def main():
    informazioni_db_thread = carica_dati_dB() #carichiamo i dati dal dB
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # server TCP
    server_socket.bind(server_address)
    server_socket.listen(5)

    num_client = 1
    lista_thread = []
    
    try:
        while True:
            client_socket, client_address = server_socket.accept() 
            thread = threading.Thread(target=gestione_client, args=(client_socket, client_address, informazioni_db_thread, num_client)) 
            # mandiamo al thread le informazioni del client + i dati del dB + il contatore progressivo del client
            thread.start()
            num_client += 1 # incrementiamo il contatore dei client
            lista_thread.append(thread) #facciamo la lista di Threads

    except KeyboardInterrupt: # Controllo se si chiude per errore
        print("Server chiudo dall'utente")
        for thread in lista_thread:
            thread.join()
            print(f"Thread {thread} chiuso")
        server_socket.close()


if __name__ == "__main__":
    main()