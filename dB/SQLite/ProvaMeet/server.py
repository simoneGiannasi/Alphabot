import socket
import sqlite3
from threading import Thread

indirizzo = 'localhost'
porta = 22222
buffer_size = 1024

# Creazione del server TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((indirizzo, porta))
server.listen(5)  # Si prepara ad accettare le connessioni

def gestioneClient(client_socket, client_address):
    # Crea una nuova connessione al database per questo thread
    conn = sqlite3.connect('file.db')
    cursor = conn.cursor()
    
    print(f"Connessione da {client_address} stabilita.")
    
    try:
        while True:
            data = client_socket.recv(buffer_size)
            if not data:
                break
            
            dataConvertiti = data.decode('utf-8')
            dati = dataConvertiti.split(':')
            nomeFile = dati[0]
            cod_com = dati[1]
            num_framm = ''
            if cod_com == '3':
                num_framm = dati[2]
            
            if cod_com == '1':
                cursor.execute('''
                    SELECT 'è_presente' AS risultato
                    FROM files
                    WHERE nome LIKE ?
                    UNION
                    SELECT 'non_è_presente' AS risultato
                    WHERE NOT EXISTS (SELECT 1 FROM files WHERE nome LIKE ?);
                ''', (f'%{nomeFile}%', f'%{nomeFile}%'))
            elif cod_com == '2': 
                cursor.execute('''
                    SELECT tot_frammenti 
                    FROM files
                    WHERE nome LIKE ?;
                ''', (f'%{nomeFile}%',)) #se si mette solamente un parametro dentro la tupla mettere la virgola alla fine del dato
            elif cod_com == '3':
                cursor.execute('''
                    SELECT FRAMMENTI.host
                    FROM FILES INNER JOIN FRAMMENTI ON FRAMMENTI.id_file = FILES.id_file
                    WHERE nome LIKE ? AND FRAMMENTI.n_frammento LIKE ?
                ''', (f'%{nomeFile}%',f'%{num_framm}%'))
            elif cod_com== '4':
                cursor.execute('''
                    SELECT FRAMMENTI.host
                    FROM FILES INNER JOIN FRAMMENTI ON FRAMMENTI.id_file = FILES.id_file
                    WHERE nome LIKE ?
                ''', (f'%{nomeFile}%',))

            results = cursor.fetchall()
            #print(results)
            client_socket.sendall(str(results).encode('utf-8'))

    except Exception as e:
        print(f"Errore nella comunicazione con {client_address}: {e}")
    finally:
        client_socket.close()
        conn.close()
        print(f"Connessione con {client_address} chiusa.")

while True:
    client, address = server.accept()
    print(f"Connessione con {client} iniziata.")
    client_thread = Thread(target=gestioneClient, args=(client, address))
    client_thread.start()
