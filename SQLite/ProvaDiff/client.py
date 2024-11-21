import socket


server_address = ('127.0.0.1', 12345)
BUFFER_SIZE = 4096
admitted_commands = ["1","2","3","4"]
def main():
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp_client_socket.connect(server_address)
    print(f"Connesso al server {server_address}")

    menu_message = tcp_client_socket.recv(BUFFER_SIZE).decode("utf-8")
    print(menu_message)
    while True:
        option = input("Seleziona un opzione: ")
        while option not in admitted_commands and option.lower() != "exit":
            option = input("Valore non valido. Per favore selezionare il numero tra le scelte. Seleziona un opzione valida: ")
        tcp_client_socket.send(option.encode("utf-8"))
        choice = tcp_client_socket.recv(BUFFER_SIZE).decode("utf-8")
        if choice == "1":
            filename = input("Inserisci il nome del file: ")
            tcp_client_socket.send(filename.encode("utf-8"))
            response = tcp_client_socket.recv(BUFFER_SIZE).decode("utf-8")
            print(response)

        elif choice == "2":
            filename = input("Inserisci il nome del file: ")
            tcp_client_socket.send(filename.encode("utf-8"))
            response = tcp_client_socket.recv(BUFFER_SIZE).decode("utf-8")
            print(response)

        elif choice == "3":
            filename = input("Inserisci il nome del file: ")
            tcp_client_socket.send(filename.encode("utf-8"))
            response = tcp_client_socket.recv(BUFFER_SIZE).decode("utf-8")
            if response != "continue": 
                print("Errore nella restituzione")
                break
            n_frag = input("Inserisci il numero del frammento: ")
            tcp_client_socket.send(n_frag.encode("utf-8"))
            response = tcp_client_socket.recv(BUFFER_SIZE).decode("utf-8")
            print(response)

        elif choice == "4":
            filename = input("Inserisci il nome del file: ")
            tcp_client_socket.send(filename.encode("utf-8"))
            response = tcp_client_socket.recv(BUFFER_SIZE).decode("utf-8")
            print(response)
        else:
            print("Chiusura del client")
            tcp_client_socket.close()
            break

   
if __name__ == '__main__':
    main()