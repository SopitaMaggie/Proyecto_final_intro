import json
import os

# Donde se guardan los registros de los jugadores
archivo_Usuarios = "Usuarios_Registrados.json"
def cargar_jugadores(): # Carga la info de los jugadores
    if not os.path.exists(archivo_Usuarios):
        return {} # Si no hay lo devuelve vacio
    with open(archivo_Usuarios, "r") as f:
        return json.load(f)
def guardar_jugadores(jugadores):
    with open(archivo_Usuarios, "w") as f:
        json.dump(jugadores, f, indent=4)

class Jugador:
    def __init__(self, username, password, victorias_defensor=0, victorias_atacante=0, nombre=""):
        self.username = username
        self.password = password
        self.victorias_defensor = victorias_defensor
        self.victorias_atacante = victorias_atacante
        self.nombre = nombre
    def exportar(self): # Convierte en archivo
        return {
            "username": self.username,
            "password": self.password,
            "victorias_defensor": self.victorias_defensor,
            "victorias_atacante": self.victorias_atacante,
            "nombre": self.nombre
        }
    @staticmethod
    def importar(datos): # Carga el archivo
        return Jugador(
            username=datos["username"],
            password=datos["password"],
            victorias_defensor=datos.get("victorias_defensor", 0),
            victorias_atacante=datos.get("victorias_atacante", 0),
            nombre=datos.get("nombre", "")
        )

    def mostrar(self):
        print("Usuario:", self.username)
        print("Victorias defensor:", self.victorias_defensor)
        print("Victorias atacante:", self.victorias_atacante)

    def agregar_victoria(self, rol):
        if rol == "defensor":
            self.victorias_defensor += 1
        elif rol == "atacante":
            self.victorias_atacante += 1

def registrar_jugador(username, password, nombre=""):
    jugadores = cargar_jugadores()
    if username in jugadores:
        return None, "El nombre de usuario ya existe."
    nuevo = Jugador(username, password, nombre=nombre)
    jugadores[username] = nuevo.exportar()
    guardar_jugadores(jugadores)
    return nuevo, "Registro exitoso."


def iniciar_sesion(username, password):
    jugadores = cargar_jugadores()
    if username not in jugadores:
        return None, "Usuario no encontrado."
    datos = jugadores[username]
    if datos["password"] != password:
        return None, "Contraseña incorrecta."
    return Jugador.importar(datos), "Inicio de sesión exitoso."


def actualizar_jugador(jugador):
    jugadores = cargar_jugadores()
    jugadores[jugador.username] = jugador.exportar()
    guardar_jugadores(jugadores)
    
def obtener_ranking():
    jugadores = cargar_jugadores()
    lista = [Jugador.importar(d) for d in jugadores.values()]

    ranking_defensor = sorted(lista, key=lambda j: j.victorias_defensor, reverse=True)[:5]
    ranking_atacante = sorted(lista, key=lambda j: j.victorias_atacante, reverse=True)[:5]

    return ranking_defensor, ranking_atacante

