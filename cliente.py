import socketio

sio = socketio.Client()

nombre = input("Tu nombre: ")

modo = input("comunidad (c) o privado (p): ")

if modo == "c":
    comunidad = input("nombre comunidad: ")
else:
    destino = input("usuario destino: ")

@sio.event
def connect():

    print("conectado")

    sio.emit("registrar", {"uid": nombre})

    if modo == "c":
        sio.emit("join_comunidad", {"comunidad": comunidad})


@sio.on("message")
def recibir(data):

    if data.get("privado"):
        print(f"[privado] {data['nombre']}: {data['mensaje']}")
    else:
        print(f"[{data['comunidad']}] {data['nombre']}: {data['mensaje']}")


sio.connect("https://proyectointernet.onrender.com/chat/programacion")


while True:

    texto = input()

    if modo == "c":

        sio.emit("mensaje", {
            "nombre": nombre,
            "mensaje": texto,
            "comunidad": comunidad,
            "privado": False
        })

    else:

        sio.emit("mensaje", {
            "nombre": nombre,
            "mensaje": texto,
            "privado": True,
            "usuarios": [nombre, destino]
        })
