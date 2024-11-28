import socket

# nome_file:cod_op:num_framm
#facciamo la split su i :

buffer_size = 4096
indirizzo_server = 'localhost'  # L'indirizzo server dove il server è in esecuzione
porta_server = 22222  # La porta deve essere un intero

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((indirizzo_server, porta_server))

numCom = 0

while True:
    while numCom not in range(1, 6):
        numCom = int(input('1. il file con nome x è presente?;\n2. numero di frammenti da nome file;\n3. da numero frammento di nome file a IP host contenitore;\n4. da nome file a tutti gli IP degli host contenenti i frammenti.\n5. esci\nComando: '))
    
    if numCom == 1 or numCom == 2 or numCom == 4:
        # il file con nome x è presente?
        nomeFile = input('Inserisci il nome del file: ')
        comando = nomeFile + ':' + str(numCom)  # componiamo il comando
        client.sendall(comando.encode('utf-8'))
        numCom = 0

    elif numCom == 3:
        numCom = 0
        # da numero frammento di nome file a IP host contenitore
        nomeFile = input('Inserisci il nome del file: ')
        numeroFrammento = input("Inserisci il numero del frammento: ")
        comando = nomeFile + ':3:' + numeroFrammento  # componiamo il comando
        client.sendall(comando.encode('utf-8'))
    else:
        client.close()
        break



    # #pulizia dell'output
    #stringa_modificata= client.recv(buffer_size).decode("utf-8")
    # da_sostituire=[' ','[',']','(',')']
    # for carattere in da_sostituire: 
    #     stringa_modificata = stringa_modificata.replace(carattere, "")
    # stringa_modificata = stringa_modificata.replace(',',"\n")         
    # print(f'Dati ricevuti:\n\n{stringa_modificata}\n')

    data=client.recv(buffer_size).decode("utf-8")
    print(f'Dati ricevuti:\n{data}\n\n')

   




