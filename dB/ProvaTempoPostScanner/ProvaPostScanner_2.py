import sqlite3
import socket
import threading
from ipaddress import ip_network

network_scansionare = "192.168.0.0/27"
PORTE_COMUNI = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306]
DB_NAME = "ip_list.db"



def scan_porta(ip, porta, porte_aperte):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket TCP
    sock.settimeout(1)  # Timeout di 1 secondo
    ris = sock.connect_ex((str(ip), porta))
    if ris == 0:
        porte_aperte.append(porta)
    sock.close()


def scan_utente(ip):
    porte_aperte = []
    for porta in PORTE_COMUNI:
        scan_porta(ip, porta, porte_aperte) #qua mi devo gestire le porte aperte append
    salva_dati_db(ip,porte_aperte) #nome host lo devo guardare qua dentro



def salva_dati_db(ip,porte_aperte):
    
    try:
        nome_host = socket.gethostbyaddr(ip)
    except:
        nome_host = "Non reperibile"



    connessione_db = sqlite3.connect(DB_NAME)
    cursor = connessione_db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ports(
                   ip_host TEXT,
                   nome_host TEXT,
                   port_list TEXT)''')
    porte_aperte_str = ",".join(map(str, porte_aperte))
    cursor.execute("INSERT INTO ports (ip_host, nome_host, port_list) VALUES (?,?,?)", (str(ip), nome_host, porte_aperte_str))
    connessione_db.commit()
    connessione_db.close()



def main():
    lista_threads = []
    network = ip_network(network_scansionare)

    for ip in network.hosts():
        thread = threading.Thread(target=scan_utente, args=(ip,))    
        lista_threads.append(thread)
        thread.start()

    for thread in lista_threads:
        thread.join()

    print("Scansione Completata")


if __name__ == "__main__":
    main()