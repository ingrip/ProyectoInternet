import socketio
import threading

SERVER_URL = "https://proyectointernet.onrender.com"  # tu URL en Render

uid = input("Ingresa tu UID: ").strip()
nombre = input("Ingresa tu nombre: ").strip()
modo = input("Comunidad (c) o chat privado (p)?: ").strip().lower()

if modo == "c":
    comunidad_actual = input("Nombre de la comunidad: ").strip()
    chat_privado_actual = None
    usuarios_privados = []
else:
    chat_privado_actual = input("UID del chat privado: ").strip()
    comunidad_actual = None
    usuarios_privados = [uid, chat_privado_actual]

sio = socketio.Client()

@sio.event
def connect():
    print("Conectado al servidor")
    if comunidad_actual:
        sio.emit("join_comunidad", {"comunidad": comunidad_actual})
    else:
        sio.emit("join", {"uid": uid, "nombre": nombre})
    sio.emit("cargar_historial", {
        "uid": uid,
        "comunidad": comunidad_actual,
        "privado_con": chat_privado_actual
    })

@sio.event
def disconnect():
    print("Desconectado")

@sio.on("message")
def recibir(data):
    if data.get("privado"):
        if chat_privado_actual and data["uid"] in usuarios_privados:
            print(f"[PRIVADO] {data['nombre']} ({data['hora']}): {data['mensaje']}")
    else:
        if comunidad_actual and data.get("comunidad") == comunidad_actual:
            print(f"[{data['comunidad']}] {data['nombre']} ({data['hora']}): {data['mensaje']}")

@sio.on("historial")
def mostrar_historial(mensajes):
    print("Historial:")
    for m in mensajes:
        if m.get("privado"):
            if chat_privado_actual and set(m.get("usuarios", [])) == set(usuarios_privados):
                print(f"[PRIVADO] {m['nombre']} ({m['hora']}): {m['mensaje']}")
        else:
            if comunidad_actual and m.get("comunidad") == comunidad_actual:
                print(f"[{m['comunidad']}] {m['nombre']} ({m['hora']}): {m['mensaje']}")
    print("----- Fin historial -----")

def enviar_mensajes():
    while True:
        texto = input()
        if not texto.strip():
            continue
        data = {
            "nombre": nombre,
            "mensaje": texto,
            "uid": uid,
            "privado": False,
            "comunidad": comunidad_actual
        }
        if chat_privado_actual:
            data["privado"] = True
            data["usuarios"] = usuarios_privados
            data.pop("comunidad", None)
        sio.emit("mensaje", data)

def main():
    try:
        sio.connect(SERVER_URL)
    except Exception as e:
        print("Error conectando:", e)
        return

    hilo = threading.Thread(target=enviar_mensajes)
    hilo.daemon = True
    hilo.start()

    sio.wait()

if __name__ == "__main__":
    main()
