from socket import *

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


message = clientSocket.recv(4096).decode()
print(message)

while True:
    country_iso = input("\nIntroduce ISO del país a consultar o \"exit\" en cualquier momento para salir: ")
    clientSocket.send(country_iso.encode())
    if country_iso.lower() == "exit":
        print(clientSocket.recv(1024).decode())
        break

    message = clientSocket.recv(1024).decode()
    print(message)
    if "no se encuentra en el ranking" in message:
        continue
    option = input("\nElige entre 1, 2 y 3 o 'exit': ")
    clientSocket.send(option.encode())
    if option.lower() == "exit":
        print(clientSocket.recv(1024).decode())
        break

    response = clientSocket.recv(4096).decode()
    print(response)

clientSocket.close()
