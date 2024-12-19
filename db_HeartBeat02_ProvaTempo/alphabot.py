import socket
import alphaLib
import sqlite3
import threading
import time

# Impostazione dell'indirizzo del server
alphabot_address = ("192.168.190.75", 54321)
DB_NAME = "./movimenti.db"
HEARTBEAT_TIMEOUT = 10 # Tempo massimo di attesa tra gli heartbeat
BUFFER_SIZE = 4096
last_heartbeat_time = time.time()  # Variabile globale per tracciare l'ultimo heartbeat
is_connected = False
alpha = alphaLib.AlphaBot()


def main():
    '''# Funzione main in cui apro il db e mi savo nella variabile dati quello che ottengo
    Creo il collegamento TCP con il client accetto la connessione e mando il thread dell'heartbeat e quello del monitoraggio.
    Leggo il messaggio del client:
    - se il messaggio è "end" termino la connessione
    - se il messaggio è composto da due valori (quelli dei motori) svolgo l'azione richiamando la funzione gestioneMovimento
    - se il messaggio è composto da un valore richiamo la funzione gestioneComandiSpeciali
    #'''
    global is_connected
    global alpha
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    dati = cursor.execute('''SELECT * FROM movimento''').fetchall()
    
    movimenti_speciali_dict = {}
    for com in dati:
        movimenti_speciali_dict[com[0]] = com[1]
    print(movimenti_speciali_dict)

    comandi_speciali_iop = False

    # Creazione del socket TCP del server
    alphabot_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alphabot_tcp.bind(alphabot_address)
    alphabot_tcp.listen(1)
    print("Server AlphaBot in ascolto...")
    alpha.setMotor(0, 0)

    
    while not is_connected:
        try:
            client, address = alphabot_tcp.accept()
            is_connected = True
            print(f"Connessione accettata da {address}")

            # N.B. i thread di heartbeat sono daemon, non bisogna chiuderli esplicitamente
            heartbeat_thread = threading.Thread(target=handle_heartbeat, daemon=True)
            heartbeat_thread.start()

            heartbeat_monitor_thread = threading.Thread(target=monitor_heartbeat, daemon=True)
            heartbeat_monitor_thread.start()
            while True:
                messaggio = client.recv(BUFFER_SIZE).decode('utf-8')
                if messaggio:
                    if messaggio == 'end':
                        print("Chiusura connessione...")
                        client.send("Connessione chiusa con successo".encode('utf-8'))
                        time.sleep(2)
                        client.close()
                        is_connected = False
                        print("Connessione chiusa con successo")
                        break
                    comandi = messaggio.split(",")  # Splitta i comandi
                    if len(comandi) == 2 and comandi_speciali_iop==False:
                        left = int(comandi[0])
                        right = int(comandi[1])
                        print(f"Comando ricevuto: {left},{right}")
                        alpha.setMotor(left, right)
                    else:
                        comando = comandi[0]
                        comandi_speciali_iop = True
                        gestisciComandiSpeciali(comando, movimenti_speciali_dict)
                        comandi_speciali_iop = False
                        
                else:
                    break  # Chiude la connessione se non ci sono più messaggi
        except:
            print("Errore nella connessione con il client.")
            is_connected = False
            client.close()
            alpha.stop()
        #finally:
            #alphabot_tcp.close()

# Funzione per gestire gli heartbeat
def handle_heartbeat():
    '''Funzione che uso per ricevere l'heartbeat dal client, la usa il thread apposito.
    Prendo lo stesso ip della prima connessione ma uso la porta+1
    '''
    global last_heartbeat_time
    global alphabot_address
    global is_connected
    is_connected = True
    address = alphabot_address[0]
    port = alphabot_address[1] + 1
    alphabot_address2 = (address, port)
    alphabot_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alphabot_tcp.bind(alphabot_address2)
    alphabot_tcp.listen(1)
    client, address = alphabot_tcp.accept()
    print(f"Collegamento per l'heartbeat con {alphabot_address2}")

    while is_connected:
        try:
            data = client.recv(BUFFER_SIZE).decode("utf-8")
            if data == "HEARTBEAT":
                last_heartbeat_time = time.time()
        except (socket.error, ConnectionResetError):
            print("Errore di connessione mentre si riceve l'heartbeat.")
            print("Connessione chiusa con successo")
            is_connected = False
            client.close()
            alphabot_tcp.close()
            alpha.stop()
            break

def monitor_heartbeat():
    '''Funzione che monitora l'heartbeat in base al tempo
    '''
    global last_heartbeat_time, is_connected
    global HEARTBEAT_TIMEOUT
    while is_connected:
        if time.time() - last_heartbeat_time > HEARTBEAT_TIMEOUT:
            print("Heartbeat non ricevuto in tempo! Arresto del robot.")
            #ab.stop()
            is_connected = False
            break
        time.sleep(HEARTBEAT_TIMEOUT / 2)  # Controlla frequentemente lo stato degli heartbeat


def gestisciComandiSpeciali(comando, movimenti_speciali_dict):
    if comando in movimenti_speciali_dict:
        print(movimenti_speciali_dict[comando])
        movimento = movimenti_speciali_dict[comando]
        gestioneMovimento(movimento)


def gestioneMovimento(movimento):
    pezzi_movimento = movimento.split(',')

    for pezzo_movimento in pezzi_movimento:
        pezzo = pezzo_movimento.split(':')
        wasd = pezzo[0] # dice wasd in base a dove andare
        tempo = int(pezzo[1]) # dice il tempo per cui deve andare
        print(f"Wasd={wasd},tempo={tempo}")
        
        # Registra il tempo di inizio
        start_time = time.time()
        # Continua ad eseguire finché non sono trascorsi n secondi
        while time.time() - start_time < tempo:
            if wasd == "w":
                alpha.setMotor(-50, 50)
                pass
            if wasd == "s":
                alpha.setMotor(50, -50)
                pass
            if wasd == "a":
                alpha.setMotor(0, 30)
                pass
            if wasd == "d":
                alpha.setMotor(-30, 0)
                pass
        

if __name__ == '__main__':
    main()