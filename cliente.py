import socket

IP = '192.168.48.1'  
PUERTO = 1234

def iniciar_cliente():
    client_socket = socket.socket()
    client_socket.connect((IP, PUERTO))

    print(client_socket.recv(1024).decode())  
    nombre = input("Tu nombre: ")
    client_socket.send(nombre.encode())

    print(client_socket.recv(1024).decode())  
    print(client_socket.recv(1024).decode()) 

    while True:
        comando = input("> ")
        client_socket.send(comando.encode())

        respuesta = client_socket.recv(4096).decode()
        print(respuesta)

        if comando == '/adios':
            print("Cerrando conexión...")
            break

    client_socket.close()

if __name__ == "__main__":
    iniciar_cliente()
