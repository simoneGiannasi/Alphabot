import socket
import sqlite3
import threading
from ipaddress import ip_network

# Configurazione
NETWORK = '192.168.0.0/27'
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306]  # Porte comuni
DB_NAME = './ip_list.db'

# Funzione per scansionare una porta su un host
def scan_port(ip, port, open_ports):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket TCP
    sock.settimeout(1)  # Timeout di 1 secondo
    result = sock.connect_ex((ip, port))
    if result == 0:
        open_ports.append(port)
    sock.close()
        

# Funzione per scansionare un host
def scan_host(ip):
    open_ports = [] # Lista delle porte aperte
    for port in COMMON_PORTS:
        scan_port(ip, port, open_ports)
    # Salva i risultati nel database
    save_to_db(ip, open_ports) # Passi id e le porte aperte e poi dentro la funzione vado a vedere il nome dell'host


# Funzione per salvare i risultati nel database
def save_to_db(ip, open_ports):
    try:
        # Ottieni il nome dell'host
        host_name = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        host_name = None

    # Connessione al database SQLite
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Crea la tabella se non esiste
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ports (
            ip_host TEXT,
            nome_host TEXT,
            port_list TEXT
        )
    ''')
    
    # Salva i dati solo se il nome dell'host è disponibile
    if host_name:
        port_list_str = ','.join(map(str, open_ports))
        cursor.execute('''
            INSERT INTO ports (ip_host, nome_host, port_list) VALUES (?, ?, ?)
        ''', (ip, host_name, port_list_str))
    
    conn.commit()
    conn.close()

# Funzione principale per avviare la scansione
def main():
    network = ip_network(NETWORK)
    threads = []

    for ip in network.hosts():  # per ogni host nella rete
        # Crea un thread per la scansione del host corrente
        thread = threading.Thread(target=scan_host, args=(str(ip),))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print('Scansione completa.')

if __name__ == '__main__':
    main()