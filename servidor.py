# servidor.py
# servidor de chat en python con chats por comunidad y privados
import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 5000

uid = input("Tu UID: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

cliente.send(uid.encode())

def recibir():

    while True:

        try:
            mensaje = cliente.recv(4096).decode()
            data = json.loads(mensaje)

            print(f"{data['nombre']} ({data['hora']}): {data['mensaje']}")

        except:
            print("conexion cerrada")
            break

def enviar():

    while True:

        texto = input()

        data = {
            "nombre": uid,
            "mensaje": texto
        }

        cliente.send(json.dumps(data).encode())

threading.Thread(target=recibir).start()

enviar()
