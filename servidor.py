from flask import Flask, request
from flask_socketio import SocketIO, join_room
from datetime import datetime
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

socketio = SocketIO(app, cors_allowed_origins="*")

usuarios = {}  # sid -> uid


@socketio.on("connect")
def conectar():
    print("cliente conectado")


@socketio.on("registrar")
def registrar(data):

    uid = data.get("uid")

    usuarios[request.sid] = uid

    print("usuario registrado:", uid)


@socketio.on("join_comunidad")
def join_comunidad(data):

    comunidad = data.get("comunidad")

    if comunidad:
        join_room(comunidad)
        print("usuario entro a comunidad:", comunidad)


@socketio.on("mensaje")
def manejar_mensaje(data):

    now = datetime.now()

    data["hora"] = now.strftime("%H:%M")
    data["fecha"] = now.isoformat()

    privado = data.get("privado", False)

    if privado:

        usuarios_destino = data.get("usuarios", [])

        for sid, uid in usuarios.items():

            if uid in usuarios_destino:
                socketio.emit("message", data, room=sid)

    else:

        comunidad = data.get("comunidad")

        socketio.emit("message", data, room=comunidad)


@socketio.on("disconnect")
def desconectar():

    if request.sid in usuarios:
        print("usuario desconectado:", usuarios[request.sid])
        usuarios.pop(request.sid)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    socketio.run(app, host="0.0.0.0", port=port)
