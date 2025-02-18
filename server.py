import threading
import socket



host = '127.0.0.1' #localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def sendMessage(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            sendMessage(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            sendMessage(f'{nickname} left the chat!!!'.encode('ascii'))
            nicknames.remove(nickname)
            break


def receiveConnection():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of client is {nickname}')
        sendMessage(f'{nickname} joined the chat!!!'.encode('ascii'))
        client.send('Connected to the server!!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening....")
receiveConnection()

