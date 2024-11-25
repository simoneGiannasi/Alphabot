import socket
import alphaLib

def direzione(messaggio):
    right = 0
    left = 0
    if "w" in messaggio:
        right = 50
        left = 50
    if "s" in messaggio and "w" not in messaggio:
        right = -50
        left = -50
    if "a" in messaggio:
        if right >= 0:
            right += 20
        else:
            right -= 20
    if "d" in messaggio and "a" not in messaggio:
        if left >= 0:
            left += 20
        else:
            left -= 20
    alpha.setMotor(left, right)



tastiConcessi = ["w", "a", "s", "d"]
alphabot_address = ("192.168.1.124", 12345)

alphabot_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alphabot_tcp.bind(alphabot_address)
alphabot_tcp.listen(1)
print("Server AlphaBot in ascolto...")

alpha = alphaLib.AlphaBot()
try:
    while True:
        client, address = alphabot_tcp.accept()
        print(f"Connessione accettata da {address}")
        while True:
            messaggio = client.recv(4096).decode('utf-8')
            if messaggio in tastiConcessi:
                direzione(messaggio)
                print(f"Comando ricevuto: {messaggio}")
            elif messaggio == 'stop':
                alpha.stop()
            elif messaggio == 'end':
                print("Chiusura connessione...")
                client.close()
                break
            else:
                print("Comando non riconosciuto.")

except KeyboardInterrupt:
    print("Server interrotto manualmente.")
finally:
    alphabot_tcp.close()
    print("Server chiuso.")


