import socket
from query import *
import threading

server_address = ('127.0.0.1', 12345)
menu_message = '''
1. Controlla se esiste un file con un nome specificato
2. Trova il numero di frammenti di un file con un nome specificato
3. Trova l'indirizzo IP dei host dei frammenti di un file con un nome specificato
4. Trova tutti gli indirizzi ip degli host sui quali sono salvati i frammenti di un file a partire dal nome file.
'''
admitted_commands = ["1", "2", "3", "4"]
connected_clients = []
BUFFER_SIZE = 4096

def handle_client(conn, client_address):
    """
    Handles communication with a connected client.

    This function sends a menu of options to the client and processes the client's requests
    based on the selected command. It interacts with a database to perform operations such as
    checking file existence, retrieving fragment numbers, and obtaining IP addresses of hosts
    storing file fragments.

    Parameters:
    conn (socket.socket): The socket object representing the client's connection.
    client_address (tuple): A tuple containing the client's IP address and port number.

    Returns:
    None
    """
    conn.send(menu_message.encode("utf-8"))
    while True:
        data = conn.recv(BUFFER_SIZE).decode('utf-8')
        if data == admitted_commands[0]:
            conn.send("1".encode("utf-8"))
            data = conn.recv(BUFFER_SIZE).decode('utf-8')
            cur, conn_db = connect_to_db()
            if are_there_files(cur=cur, conn=conn_db, filename=data):
                conn.send("Il file esiste.".encode("utf-8"))
            else:
                conn.send("Il file non esiste.".encode("utf-8"))
        elif data == admitted_commands[1]:
            cur, conn_db = connect_to_db()
            conn.send("2".encode("utf-8"))
            data = conn.recv(BUFFER_SIZE).decode('utf-8')
            result = n_frag_from_name(data, cur=cur, conn=conn_db)
            conn.send(str(result[0][1]).encode("utf-8"))
        elif data == admitted_commands[2]:
            conn.send("3".encode("utf-8"))
            filename = conn.recv(BUFFER_SIZE).decode('utf-8')
            conn.send("continue".encode("utf-8"))
            frag_n = conn.recv(BUFFER_SIZE).decode('utf-8')
            cur, conn_db = connect_to_db()
            result = ip_host_from_name_and_frag_number(filename=filename, n_frag=frag_n, cur=cur, conn=conn_db)
            conn.send(result[0][0].encode("utf-8"))
        elif data == admitted_commands[3]:
            conn.send("4".encode("utf-8"))
            data = conn.recv(BUFFER_SIZE).decode('utf-8')
            cur, conn_db = connect_to_db()
            result = all_ips_of_fragments(filename=data, cur=cur, conn=conn_db)
            string_to_send = ""
            #cicla la lista e prende le tuple
            for ip in result:
                string_to_send += ip[0] + "\n" 
            conn.send(string_to_send.encode("utf-8"))
        elif data.lower() == "exit":
            print(f"Chiusura della connessione con il client {client_address}")
            conn.close()
            break
        else:
            conn.send("Comando non valido.".encode("utf-8"))


def main():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(server_address)
    tcp_server_socket.listen(2)
    print(f"Server in ascolto su {server_address}")

    # Infinite loop to accept connections and handle them in separate threads.
    try:
        while True:
            conn, client_address = tcp_server_socket.accept()
            connection = threading.Thread(target=handle_client, args=(conn, client_address))
            connection.start()
            connected_clients.append((connection, client_address))
            print(connected_clients)
    except KeyboardInterrupt: # Handle keyboard interrupt
        print("Server chiuso dall'utente.")
        for connection in connected_clients:
            print("chiudendo thread")
            print(connection)
            connection[0].join()
            print(f"Connection {connection[1]} closed.")
        tcp_server_socket.close()
        print("Server terminato.")



if __name__ == '__main__':
    main()

