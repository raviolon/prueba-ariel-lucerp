import socket
import threading
import requests

def manejar_cliente(cliente_socket):
    cliente_socket.send(b'ingrese su nombre de usuario: ')
    nombre = cliente_socket.recv(1024).decode().strip()
    cliente_socket.send(f'bienvenido, {nombre}\n'.encode())
    cliente_socket.send(f'escribí /pokemon <nombre> para buscar un pokemon o /adios para salir\n')

    while True:
        comando = cliente_socket.recv(1024).decode().strip()

        if comando.startswith('/pokemon '):
            nombre_pokemon = comando.split(' ', 1)[1].lower()
            url = f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon}"
            respuesta = requests.get(url)

            if respuesta.status_code == 200:
                data = respuesta.json()
                info = f"Nombre: {data['name']}\nAltura: {data['height']}\nPeso: {data['weight']}\n"
                cliente_socket.send(info.encode())
            else:
                cliente_socket.send(f"Pokémon '{nombre_pokemon}' no encontrado.\n".encode())

        elif comando == '/adios':
            cliente_socket.send(f'¡Adiós, {nombre}! Que tengas un buen día.\n'.encode())
            break

        else:
            cliente_socket.send(b'Comando no reconocido. Usa /pokemon <nombre> o /adios\n')

    cliente_socket.close()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('192.168.48.1', 1234))  
    servidor.listen(5)

    while True:
        cliente_socket, direccion = servidor.accept()
        print(f"[Servidor] conexion aceptada de {direccion}")
        threading.Thread(target=manejar_cliente, args=(cliente_socket,), daemon=True).start()

if __name__ == "__main__":
    iniciar_servidor()
