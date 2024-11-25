import sqlite3
import socket
import threading
from ipaddress import ip_network


rete_da_scansionare = '192.168.0.0/27'
PORTE_COMUNI = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306]  # Porte comuni
DB_NAME = './ip_list.db'


def scansionare_porta(ip, porta, porte_aperte):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.settimeout(1)  # Timeout di 1 secondo
    ris = my_socket.connect_ex((ip, porta))
    if ris == 0:
        porte_aperte.append(porta)
    socket.close()

def salva_su_db(ip, porte_aperte):
    try:
        host = socket.gethostbyaddr(ip)[0]
    except:
        host = None
   
    connessione_db = sqlite3.connect(DB_NAME)
    cursor = connessione_db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ports(
                   ip: TEXT,
                   host_name: TEXT,
                   porte_aperte: TEXT)''')
    
    if host:
        porte_aperte_stringa = ','.join(map(str, porte_aperte))
        cursor.execute("INSERT INTO ports (ip, host_name, porte_aperte) VALUES (?,?,?)", (ip, host, porte_aperte_stringa))
    connessione_db.commit()
    connessione_db.close()
   

def scansionare_host(ip):
    porte_aperte = []
    for porta in PORTE_COMUNI:
        scansionare_porta(ip, porta, porte_aperte)
    salva_su_db(ip, porte_aperte)


def main():
    network = ip_network(rete_da_scansionare)
    threads = []

    for ip in network.hosts():  # per ogni host nella rete
        thread = threading.Thread(target=scansionare_host, args=(str(ip),))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print('Scansione completa.')

if __name__ == '__main__':
    main()