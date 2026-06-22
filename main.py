import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from usuario import registrar_jugador, iniciar_sesion, obtener_ranking
from juego import Partida, BaseCentral
from defensor import Torre, Muro
from atacante import Unidad


FACCIONES = { # configura la parte visual
    "olimpo": {
        "nombre": "Olimpo",
        "descripcion": "Poder divino y rayos del cielo",
        "color_a": "#6aaa3c",
        "color_b": "#5e9c33",
        "color_preview": "#4a8c3f",
    },
    "oscura": {
        "nombre": "Oscura",
        "descripcion": "Sombras y neblina como escudo",
        "color_a": "#3a2060",
        "color_b": "#2e1850",
        "color_preview": "#5e35b1",
    },
    "volcan": {
        "nombre": "Volcán",
        "descripcion": "Fuego y lava protegen la base",
        "color_a": "#7d2c14",
        "color_b": "#5e2010",
        "color_preview": "#b5381d",
    }
}
def ventana_siguiente_ronda(padre, texto_boton, funcion_siguiente):
    win = tk.Toplevel(padre)
    win.title("Siguiente ronda")
    centrar_ventana(win, 650, 420)
    win.resizable(False, False)
    canvas = tk.Canvas(win, width=650, height=420, bg="#1b102d", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_text(
        325, 110,
        text="⚔ RONDA TERMINADA ⚔",
        fill="#ffd700",
        font=("Copperplate", 26, "bold")
    )
    canvas.create_text(
        325, 210,
        text="Escoge una jugada sabia.",
        fill="white",
        font=("Copperplate", 22, "bold")
    )
    boton = tk.Button(
        win,
        text=texto_boton,
        font=("Copperplate", 14, "bold"),
        bg="#f6d32d",
        fg="#1e1e2e",
        activebackground="#ffd966",
        activeforeground="#000000",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda: cerrar_y_continuar()
    )
    canvas.create_window(325, 320, width=280, height=55, window=boton)
    def cerrar_y_continuar():
        win.destroy()
        funcion_siguiente()

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho - ancho) // 2
    y = (pantalla_alto - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def ventana_felicitaciones(padre, ganador):
    win = tk.Toplevel(padre)
    win.title("Felicitaciones")
    centrar_ventana(win, 700, 500)
    win.resizable(False, False)
    img_btn_volver = ImageTk.PhotoImage(
        Image.open("Imagenes/volver.png").resize((400, 250))
    )
    canvas = tk.Canvas(win, width=700, height=500, bg="#1b102d", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_text(350, 100, text="🏆 ¡FELICIDADES! 🏆",
                       fill="#ffd700", font=("Copperplate", 28, "bold"))

    canvas.create_text(350, 200, text=f"{ganador.username}",
                       fill="white", font=("Copperplate", 24, "bold"))

    canvas.create_text(350, 280,
                       text="Has conquistado el campo de batalla\ny alcanzado la gloria.",
                       fill="#d0d0d0", font=("Arial", 16), justify="center")
    canvas.create_image(350, 410, image=img_btn_volver)
    def volver_menu_juego():
        win.destroy()
        padre.destroy()
        vtn_menu_juego(padre.master, ganador)
    zona = canvas.create_rectangle(230, 355, 470, 465, outline="", fill="")
    canvas.tag_bind(zona, "<Button-1>", lambda e: volver_menu_juego())
    canvas.tag_bind(zona, "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind(zona, "<Leave>", lambda e: canvas.config(cursor=""))

    win.img_btn_volver = img_btn_volver

def vtn_principal(): #vtn: ventana
    vtn = tk.Tk()
    vtn.title("Defensa y Asalto")
    centrar_ventana(vtn, 1300, 800)
    vtn.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(Image.open("Imagenes/inicio.png").resize((1300, 800)))
    img_jugar = ImageTk.PhotoImage(Image.open("Imagenes/btn_jugar.png").resize((600, 350)))
    img_registrar = ImageTk.PhotoImage(Image.open("Imagenes/btn_login.png").resize((600, 350)))
    img_ranking = ImageTk.PhotoImage(Image.open("Imagenes/btn_ranking.png").resize((600, 350)))
    img_info = ImageTk.PhotoImage(Image.open("Imagenes/btn_info.png").resize((600, 350)))
    img_salir = ImageTk.PhotoImage(Image.open("Imagenes/btn_salir.png").resize((600, 350)))

    canvas = tk.Canvas(vtn, width=1300, height=800, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=img_fondo, anchor="nw")

    x_botones = 670
    y_inicial = 360
    espacio = 85

    canvas.create_image(x_botones, y_inicial, image=img_jugar)
    canvas.create_image(x_botones, y_inicial + espacio, image=img_registrar)
    canvas.create_image(x_botones, y_inicial + espacio * 2, image=img_ranking)
    canvas.create_image(x_botones, y_inicial + espacio * 3, image=img_info)
    canvas.create_image(x_botones, y_inicial + espacio * 4, image=img_salir)

    def Zclick(x1, y1, x2, y2, funcion): #zona donde hace click
        zona = canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="")
        canvas.tag_bind(zona, "<Button-1>", lambda e: funcion())
        canvas.tag_bind(zona, "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind(zona, "<Leave>", lambda e: canvas.config(cursor=""))

    Zclick(430, 325, 910, 395, lambda: vtn_iniciar_sesion(vtn))
    Zclick(430, 410, 910, 480, lambda: vtn_registrarse(vtn))
    Zclick(430, 495, 910, 565, lambda: vtn_ranking(vtn))
    Zclick(430, 580, 910, 650, lambda: vtn_informacion(vtn))
    Zclick(430, 665, 910, 735, vtn.destroy)

    canvas.img_fondo = img_fondo
    canvas.img_jugar = img_jugar
    canvas.img_registrar = img_registrar
    canvas.img_ranking = img_ranking
    canvas.img_info = img_info
    canvas.img_salir = img_salir

    vtn.mainloop()


def vtn_registrarse(principal):
    win = tk.Toplevel(principal)
    win.title("Registrarse")
    centrar_ventana(win, 1300, 800)
    win.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(Image.open("Imagenes/fondo_registrar.png").resize((1300, 800)))
    img_btn_registrar = ImageTk.PhotoImage(Image.open("Imagenes/registrar.png").resize((800, 400)))
    img_btn_volver = ImageTk.PhotoImage(Image.open("Imagenes/volver.png").resize((400, 300)))

    canvas = tk.Canvas(win, width=1300, height=800, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=img_fondo, anchor="nw")

    entry_user = tk.Entry(win, font=("Arial", 18), bg="#020b1d", fg="white",
                          insertbackground="white", relief="flat", bd=0, highlightthickness=0)
    canvas.create_window(680, 310, width=500, height=28, window=entry_user)

    entry_pass = tk.Entry(win, font=("Arial", 18), bg="#020b1d", fg="white",
                          insertbackground="white", relief="flat", bd=0, highlightthickness=0, show="*")
    canvas.create_window(680, 410, width=500, height=28, window=entry_pass)

    entry_nombre = tk.Entry(win, font=("Arial", 18), bg="#020b1d", fg="white",
                            insertbackground="white", relief="flat", bd=0, highlightthickness=0)
    canvas.create_window(680, 510, width=500, height=28, window=entry_nombre)

    canvas.create_image(650, 620, image=img_btn_registrar)
    canvas.create_image(650, 730, image=img_btn_volver)

    def registrar():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()
        nombre = entry_nombre.get().strip()

        if username == "" or password == "":
            messagebox.showwarning("Campos vacíos", "Usuario y contraseña son obligatorios.", parent=win)
            return

        if nombre == "":
            nombre = username

        jugador, msg = registrar_jugador(username, password, nombre)

        if jugador:
            messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.\nYa puedes iniciar sesión.", parent=win)
            win.destroy()
            vtn_iniciar_sesion(principal)
        else:
            messagebox.showerror("Error", msg, parent=win)

    def volver_menu():
        win.destroy()

    def Zclick(x1, y1, x2, y2, funcion):
        zona = canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="")
        canvas.tag_bind(zona, "<Button-1>", lambda e: funcion())
        canvas.tag_bind(zona, "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind(zona, "<Leave>", lambda e: canvas.config(cursor=""))

    Zclick(500, 575, 800, 665, registrar)
    Zclick(540, 700, 760, 760, volver_menu)

    entry_user.bind("<Return>", lambda e: entry_pass.focus())
    entry_pass.bind("<Return>", lambda e: entry_nombre.focus())
    entry_nombre.bind("<Return>", lambda e: registrar())
    entry_user.focus()

    win.img_fondo = img_fondo
    win.img_btn_registrar = img_btn_registrar
    win.img_btn_volver = img_btn_volver


def vtn_iniciar_sesion(principal):
    win = tk.Toplevel(principal)
    win.title("Iniciar sesión")
    centrar_ventana(win, 1300, 800)
    win.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(Image.open("Imagenes/jugar_fondo.png").resize((1300, 800)))
    img_caja_usuario = ImageTk.PhotoImage(Image.open("Imagenes/caja_usuario.png").resize((700, 300)))
    img_caja_password = ImageTk.PhotoImage(Image.open("Imagenes/caja_password.png").resize((700, 300)))
    img_btn_inicio = ImageTk.PhotoImage(Image.open("Imagenes/btn_inicio.png").resize((600, 400)))
    img_btn_volver = ImageTk.PhotoImage(Image.open("Imagenes/volver.png").resize((400, 300)))
    img_btn_registrar = ImageTk.PhotoImage(Image.open("Imagenes/registrar.png").resize((400, 250)))

    canvas = tk.Canvas(win, width=1300, height=800, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, image=img_fondo, anchor="nw")
    canvas.create_image(780, 660, image=img_btn_registrar)
    canvas.create_image(500, 340, image=img_caja_usuario)
    canvas.create_image(500, 435, image=img_caja_password)
    canvas.create_image(650, 555, image=img_btn_inicio)
    canvas.create_image(650, 730, image=img_btn_volver)

    entry_user = tk.Entry(win, font=("Arial", 18), bg="#001122", fg="white",
                          insertbackground="white", relief="flat", bd=0, highlightthickness=0)
    canvas.create_window(540, 325, width=320, height=28, window=entry_user)

    entry_pass = tk.Entry(win, font=("Arial", 18), bg="#001122", fg="white",
                          insertbackground="white", relief="flat", bd=0, highlightthickness=0, show="*")
    canvas.create_window(540, 420, width=320, height=28, window=entry_pass)

    def login():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()

        if username == "" or password == "":
            messagebox.showwarning("Campos vacíos", "Debes escribir usuario y contraseña.", parent=win)
            return

        jugador, msg = iniciar_sesion(username, password)

        if jugador:
            win.destroy()
            vtn_menu_juego(principal, jugador)
        else:
            messagebox.showerror("Usuario no encontrado",
                                 "No existe este usuario o la contraseña es incorrecta.\n\nRegistra un usuario nuevo o revisa los datos.",
                                 parent=win)

    def abrir_registro():
        win.destroy()
        vtn_registrarse(principal)

    def volver_menu():
        win.destroy()

    def Zclick(x1, y1, x2, y2, funcion):
        zona = canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="")
        canvas.tag_bind(zona, "<Button-1>", lambda e: funcion())
        canvas.tag_bind(zona, "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind(zona, "<Leave>", lambda e: canvas.config(cursor=""))

    Zclick(375, 505, 925, 600, login)
    Zclick(650, 605, 875, 675, abrir_registro)
    Zclick(540, 700, 760, 760, volver_menu)

    entry_user.bind("<Return>", lambda e: entry_pass.focus())
    entry_pass.bind("<Return>", lambda e: login())
    entry_user.focus()

    win.img_fondo = img_fondo
    win.img_caja_usuario = img_caja_usuario
    win.img_caja_password = img_caja_password
    win.img_btn_inicio = img_btn_inicio
    win.img_btn_volver = img_btn_volver
    win.img_btn_registrar = img_btn_registrar


def vtn_menu_juego(principal, jugador):
    win = tk.Toplevel(principal)
    win.title("Menú de juego")
    centrar_ventana(win, 1000, 700)
    win.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(Image.open("Imagenes/menu_juego.png").resize((1000, 700)))
    img_nueva = ImageTk.PhotoImage(Image.open("Imagenes/nueva_partida.png").resize((700, 400)))
    img_ranking = ImageTk.PhotoImage(Image.open("Imagenes/salon_gloria.png").resize((700, 400)))
    img_salir = ImageTk.PhotoImage(Image.open("Imagenes/cerrar_sesion.png").resize((700, 400)))

    canvas = tk.Canvas(win, width=1000, height=700, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=img_fondo, anchor="nw")

    canvas.create_text(500, 200, text=f"Bienvenid@, {jugador.username}!",
                       fill="white", font=("Copperplate", 30, "bold"))

    canvas.create_image(500, 300, image=img_nueva)
    canvas.create_image(500, 400, image=img_ranking)
    canvas.create_image(500, 500, image=img_salir)

    def nueva_partida():
        win.destroy()
        vtn_facciones(
            principal,
            f"FACCIÓN — {jugador.username}",
            lambda f1: vtn_segunda_sesion(principal, jugador, f1)
        )

    def ranking():
        vtn_ranking(win)

    def cerrar():
        win.destroy()

    def Zclick(x1, y1, x2, y2, funcion):
        zona = canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="")
        canvas.tag_bind(zona, "<Button-1>", lambda e: funcion())
        canvas.tag_bind(zona, "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind(zona, "<Leave>", lambda e: canvas.config(cursor=""))
    Zclick(280, 255, 720, 345, nueva_partida)
    Zclick(280, 355, 720, 445, ranking)
    Zclick(280, 455, 720, 545, cerrar)

    win.img_fondo = img_fondo
    win.img_nueva = img_nueva
    win.img_ranking = img_ranking
    win.img_salir = img_salir


def vtn_facciones(padre, titulo, on_select):
    win = tk.Toplevel(padre)
    win.title("Seleccionar Facción")
    centrar_ventana(win, 1000, 700)
    win.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(Image.open("Imagenes/mapas_menu.png").resize((1000, 700)))
    img_boton_verde = ImageTk.PhotoImage(Image.open("Imagenes/boton_verde.png").resize((400, 200)))
    img_boton_morado = ImageTk.PhotoImage(Image.open("Imagenes/boton_morado.png").resize((400, 200)))
    img_boton_rojo = ImageTk.PhotoImage(Image.open("Imagenes/boton_rojo.png").resize((400, 200)))

    canvas = tk.Canvas(win, width=1000, height=700, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=img_fondo, anchor="nw")

    canvas.create_text(500, 80, text=titulo, fill="white", font=("Copperplate", 30, "bold"))

    def dibujar_mapa(x, y, faccion):
        data = FACCIONES[faccion]
        ancho = 75
        alto = 45
        for fi in range(3):
            for fj in range(3):
                color = data["color_a"] if (fi + fj) % 2 == 0 else data["color_b"]
                canvas.create_rectangle(
                    x + fj * ancho,
                    y + fi * alto,
                    x + (fj + 1) * ancho,
                    y + (fi + 1) * alto,
                    fill=color,
                    outline=""
                )

    dibujar_mapa(85, 230, "olimpo")
    dibujar_mapa(390, 230, "oscura")
    dibujar_mapa(690, 230, "volcan")

    canvas.create_image(200, 550, image=img_boton_verde)
    canvas.create_image(500, 550, image=img_boton_morado)
    canvas.create_image(800, 550, image=img_boton_rojo)

    def seleccionar(faccion):
        win.destroy()
        on_select(faccion)

    def Zclick(x1, y1, x2, y2, funcion):
        zona = canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="")
        canvas.tag_bind(zona, "<Button-1>", lambda e: funcion())
        canvas.tag_bind(zona, "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind(zona, "<Leave>", lambda e: canvas.config(cursor=""))

    Zclick(75, 500, 375, 610, lambda: seleccionar("olimpo"))
    Zclick(350, 500, 650, 610, lambda: seleccionar("oscura"))
    Zclick(625, 500, 925, 610, lambda: seleccionar("volcan"))

    win.img_fondo = img_fondo
    win.img_boton_verde = img_boton_verde
    win.img_boton_morado = img_boton_morado
    win.img_boton_rojo = img_boton_rojo


def vtn_segunda_sesion(menu_win, jugador1, faccion1):
    win = tk.Toplevel(menu_win)
    win.title("Segundo Jugador")
    centrar_ventana(win, 900, 600)
    win.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(Image.open("Imagenes/segundo_fondo.png").resize((900, 600)))
    img_caja_usuario = ImageTk.PhotoImage(Image.open("Imagenes/caja_usuario.png").resize((590, 250)))
    img_caja_password = ImageTk.PhotoImage(Image.open("Imagenes/caja_password.png").resize((590, 250)))
    img_btn_inicio = ImageTk.PhotoImage(Image.open("Imagenes/btn_inicio.png").resize((550, 280)))
    img_btn_volver = ImageTk.PhotoImage(Image.open("Imagenes/volver.png").resize((400, 200)))

    canvas = tk.Canvas(win, width=900, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=img_fondo, anchor="nw")
    canvas.create_image(400, 260, image=img_caja_usuario)
    canvas.create_image(400, 320, image=img_caja_password)
    canvas.create_image(450, 400, image=img_btn_inicio)
    canvas.create_image(450, 500, image=img_btn_volver)

    entry_user = tk.Entry(win, font=("Arial", 16), bg="#001122", fg="white",
                          insertbackground="white", relief="flat", bd=0)
    canvas.create_window(430, 250, width=260, height=26, window=entry_user)

    entry_pass = tk.Entry(win, font=("Arial", 16), bg="#001122", fg="white",
                          insertbackground="white", relief="flat", bd=0, show="*")
    canvas.create_window(430, 310, width=260, height=26, window=entry_pass)

    def login_j2():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()

        jugador2, msg = iniciar_sesion(username, password)

        if jugador2:
            win.destroy()

            def seleccionar_faccion_j2(f2):
                if f2 == faccion1:
                    messagebox.showwarning(
                        "Facción ocupada",
                        "El segundo jugador debe escoger una facción diferente."
                    )
                    vtn_facciones(
                        menu_win,
                        f"FACCIÓN — {jugador2.username}",
                        seleccionar_faccion_j2
                    )
                    return

                vtn_partida(menu_win, jugador1, jugador2, faccion1, f2)

            vtn_facciones(
                menu_win,
                f"FACCIÓN — {jugador2.username}",
                seleccionar_faccion_j2
            )

    def volver():
        win.destroy()

    def Zclick(x1, y1, x2, y2, funcion):
        zona = canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="")
        canvas.tag_bind(zona, "<Button-1>", lambda e: funcion())
        canvas.tag_bind(zona, "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind(zona, "<Leave>", lambda e: canvas.config(cursor=""))

    Zclick(240, 380, 660, 470, login_j2)
    Zclick(330, 520, 570, 590, volver)

    entry_user.bind("<Return>", lambda e: entry_pass.focus())
    entry_pass.bind("<Return>", lambda e: login_j2())
    entry_user.focus()

    win.img_fondo = img_fondo
    win.img_caja_usuario = img_caja_usuario
    win.img_caja_password = img_caja_password
    win.img_btn_inicio = img_btn_inicio
    win.img_btn_volver = img_btn_volver


def vtn_ranking(padre):
    win = tk.Toplevel(padre)
    win.title("Ranking")
    centrar_ventana(win, 1000, 800)
    win.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(Image.open("Imagenes/fondo_rancking.png").resize((1000, 800)))
    img_btn_volver = ImageTk.PhotoImage(Image.open("Imagenes/volver.png").resize((400, 300)))

    canvas = tk.Canvas(win, width=1000, height=800, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=img_fondo, anchor="nw")

    ranking_def, ranking_atk = obtener_ranking()

    y = 240
    for i, j in enumerate(ranking_def, 1):
        canvas.create_text(
            300, y,
            text=f"{i}. {j.username}  -  {j.victorias_defensor} victorias",
            fill="white",
            font=("Copperplate", 20, "bold")
        )
        y += 45

    y = 540
    for i, j in enumerate(ranking_atk, 1):
        canvas.create_text(
            300, y,
            text=f"{i}. {j.username}  -  {j.victorias_atacante} victorias",
            fill="white",
            font=("Copperplate", 20, "bold")
        )
        y += 45

    canvas.create_image(500, 780, image=img_btn_volver)

    def volver():
        win.destroy()

    zona = canvas.create_rectangle(390, 710, 610, 800, outline="", fill="")
    canvas.tag_bind(zona, "<Button-1>", lambda e: volver())
    canvas.tag_bind(zona, "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind(zona, "<Leave>", lambda e: canvas.config(cursor=""))

    win.img_fondo = img_fondo
    win.img_btn_volver = img_btn_volver


def vtn_informacion(padre):
    win = tk.Toplevel(padre)
    win.title("Información")
    centrar_ventana(win, 1000, 800)
    win.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(Image.open("Imagenes/informacion.png").resize((1000, 800)))
    img_btn_volver = ImageTk.PhotoImage(Image.open("Imagenes/volver.png").resize((400, 300)))

    canvas = tk.Canvas(win, width=1000, height=800, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=img_fondo, anchor="nw")
    canvas.create_image(500, 730, image=img_btn_volver)

    def volver():
        win.destroy()

    zona = canvas.create_rectangle(390, 700, 610, 760, outline="", fill="")
    canvas.tag_bind(zona, "<Button-1>", lambda e: volver())
    canvas.tag_bind(zona, "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind(zona, "<Leave>", lambda e: canvas.config(cursor=""))

    win.img_fondo = img_fondo
    win.img_btn_volver = img_btn_volver


CELL = 85

ESTILOS = {
    "olimpo": ("#1a5fb4", "OLI"),
    "oscura": ("#5e35b1", "OSC"),
    "volcan": ("#b5381d", "VOL"),
    "madera": ("#a0785a", "MUR"),
    "metal": ("#5e6264", "MET"),
    "flechas": ("#e07b00", "FLE"),
    "ninja": ("#2d3436", "NIN"),
    "reina_hielo": ("#4fc3f7", "REI"),
    "rey_barbaro": ("#7b3f00", "REY"),
    "fireball": ("#e01b24", "FIR"),
}


def cargar_imagen_faccion(faccion, tipo):
    try:
        ruta = f"Imagenes/facciones/{faccion}/{tipo}.png"
        img = Image.open(ruta).resize((CELL - 8, CELL - 8))
        return ImageTk.PhotoImage(img)
    except Exception:
        return None


def vtn_partida(padre, jugador1, jugador2, faccion1, faccion2):
    partida = Partida(jugador1, jugador2)

    win = tk.Toplevel(padre)
    win.title("Partida")
    centrar_ventana(win, 1200, 830)
    win.resizable(False, False)

    ronda_actual = [None]
    tipo_seleccionado = [None]
    turno = [1]
    imagenes_cache = {}

    img_base_verde = ImageTk.PhotoImage(Image.open("Imagenes/base_verde.png").resize((CELL + 10, CELL + 10)))
    img_base_morada = ImageTk.PhotoImage(Image.open("Imagenes/base_morada.png").resize((CELL + 10, CELL + 10)))
    img_base_roja = ImageTk.PhotoImage(Image.open("Imagenes/base_roja.png").resize((CELL + 10, CELL + 10)))

    img_muro_madera = ImageTk.PhotoImage(Image.open("Imagenes/muro_madera.png").resize((CELL - 8, CELL - 8)))
    img_muro_metal = ImageTk.PhotoImage(Image.open("Imagenes/muro_metal.png").resize((CELL - 8, CELL - 8)))

    img_rey = ImageTk.PhotoImage(Image.open("Imagenes/rey.png").resize((CELL - 8, CELL - 8)))
    img_ninja = ImageTk.PhotoImage(Image.open("Imagenes/ninja.png").resize((CELL - 8, CELL - 8)))
    img_hielo = ImageTk.PhotoImage(Image.open("Imagenes/hielo.png").resize((CELL - 8, CELL - 8)))
    img_fire = ImageTk.PhotoImage(Image.open("Imagenes/fire.png").resize((CELL - 8, CELL - 8)))
    img_flechas = ImageTk.PhotoImage(Image.open("Imagenes/flechas.png").resize((CELL - 8, CELL - 8)))

    imagenes_tablero = {
    "olimpo": img_base_verde,
    "oscura": img_base_morada,
    "volcan": img_base_roja,
    "madera": img_muro_madera,
    "metal": img_muro_metal,
    "rey_barbaro": img_rey,
    "ninja": img_ninja,
    "reina_hielo": img_hielo,
    "fireball": img_fire,
    "flechas": img_flechas,

    }

    frame_info = tk.Frame(win, bg="#1e1e2e", width=350, padx=8, pady=8)
    frame_info.grid(row=0, column=0, sticky="ns")
    frame_info.grid_propagate(False)

    canvas = tk.Canvas(win, width=10 * CELL, height=10 * CELL, highlightthickness=0)
    canvas.grid(row=0, column=1)

    s = {"bg": "#1e1e2e", "fg": "white"}

    lbl_ronda = tk.Label(frame_info, text="", font=("Arial", 14, "bold"), **s)
    lbl_ronda.pack(pady=(5, 2))

    lbl_fase = tk.Label(frame_info, text="", font=("Arial", 11), **s)
    lbl_fase.pack()

    lbl_dinero = tk.Label(frame_info, text="", font=("Arial", 11), **s)
    lbl_dinero.pack(pady=(0, 10))

    tk.Label(frame_info, text="Selecciona tipo:", font=("Arial", 10, "bold"), **s).pack()

    frame_tipos = tk.Frame(frame_info, bg="#1e1e2e")
    frame_tipos.pack()

    lbl_log = tk.Label(
        frame_info,
        text="",
        font=("Arial", 9),
        wraplength=215,
        justify="left",
        fg="#a6e3a1",
        bg="#1e1e2e"
    )
    lbl_log.pack(pady=8)

    btn_accion = tk.Button(
        frame_info,
        text="",
        font=("Copperplate", 13, "bold"),
        width=22,
        height=2,
        bg="#f6d32d",
        fg="#1e1e2e",
        activebackground="#ffd966",
        activeforeground="#000000",
        relief="flat",
        bd=0,
        cursor="hand2"
    )
    btn_accion.pack(pady=12)

    def dibujar_fondo():
        canvas.delete("fondo")

        if partida.defensor_actual is jugador1:
            f_atk = FACCIONES[faccion2]
            f_def = FACCIONES[faccion1]
        else:
            f_atk = FACCIONES[faccion1]
            f_def = FACCIONES[faccion2]

        for i in range(10):
            for j in range(10):
                if j <= 4:
                    color = f_atk["color_a"] if (i + j) % 2 == 0 else f_atk["color_b"]
                else:
                    color = f_def["color_a"] if (i + j) % 2 == 0 else f_def["color_b"]

                canvas.create_rectangle(
                    j * CELL,
                    i * CELL,
                    (j + 1) * CELL,
                    (i + 1) * CELL,
                    fill=color,
                    outline="",
                    tags="fondo"
                )

    def mostrar_grilla():
        canvas.delete("grilla")

        for i in range(11):
            canvas.create_line(0, i * CELL, 10 * CELL, i * CELL,
                               fill="white", width=1, tags="grilla")

        for j in range(11):
            canvas.create_line(j * CELL, 0, j * CELL, 10 * CELL,
                               fill="white", width=1, tags="grilla")

    def ocultar_grilla():
        canvas.delete("grilla")

    def dibujar_entidades():
        canvas.delete("entidad")
        ronda = ronda_actual[0]

        if partida.defensor_actual is jugador1:
            faccion_def = faccion1
            faccion_atk = faccion2
        else:
            faccion_def = faccion2
            faccion_atk = faccion1

        for i in range(10):
            for j in range(10):
                celda = ronda.mapa.obtener(i, j)

                if celda is None:
                    continue

                cx = j * CELL + CELL // 2
                cy = i * CELL + CELL // 2
                x1 = j * CELL + 5
                y1 = i * CELL + 5

                if isinstance(celda, BaseCentral):
                    if faccion_def == "olimpo":
                        img_base = img_base_verde
                    elif faccion_def == "oscura":
                        img_base = img_base_morada
                    else:
                        img_base = img_base_roja

                    canvas.create_image(cx, cy, image=img_base, tags="entidad")

                    pct = celda.vida / celda.vida_max
                    barra = int((CELL - 14) * pct)

                    canvas.create_rectangle(
                        x1,
                        y1,
                        x1 + barra,
                        y1 + 6,
                        fill="#26a269",
                        outline="",
                        tags="entidad"
                    )
                    continue

                if isinstance(celda, (Torre, Muro)):
                    faccion_entidad = faccion_def
                else:
                    faccion_entidad = faccion_atk

                clave = f"{faccion_entidad}_{celda.tipo}"

                if clave not in imagenes_cache:
                    imagenes_cache[clave] = cargar_imagen_faccion(faccion_entidad, celda.tipo)

                img = imagenes_cache[clave]

                if celda.tipo in imagenes_tablero:
                    canvas.create_image(cx, cy, image=imagenes_tablero[celda.tipo], tags="entidad")
                elif img:
                    canvas.create_image(cx, cy, image=img, tags="entidad")
                else:
                    color, letra = ESTILOS[celda.tipo]
                    canvas.create_rectangle(
                        j * CELL + 5,
                        i * CELL + 5,
                        (j + 1) * CELL - 5,
                        (i + 1) * CELL - 5,
                        fill=color,
                        outline="white",
                        width=1,
                        tags="entidad"
                    )
                    canvas.create_text(cx, cy, text=letra, fill="white",
                                       font=("Arial", 9, "bold"), tags="entidad")

    def seleccionar(tipo):
        tipo_seleccionado[0] = tipo

        if tipo in Torre.TIPOS:
            nombre = Torre.TIPOS[tipo]["nombre"]
            lbl_log.config(text=f"Torre seleccionada: {nombre}")
        elif tipo in Muro.TIPOS:
            nombre = Muro.TIPOS[tipo]["nombre"]
            lbl_log.config(text=f"Muro seleccionado: {nombre}")
        elif tipo in Unidad.TIPOS:
            nombre = Unidad.TIPOS[tipo]["nombre"]
            lbl_log.config(text=f"Unidad seleccionada: {nombre}")
        else:
            lbl_log.config(text=f"Seleccionado: {tipo}")

    def cargar_tarjeta(nombre, ancho=100, alto=100):
        img = ImageTk.PhotoImage(Image.open(f"Imagenes/{nombre}.png").resize((ancho, alto)))
        return img

    tarjetas_labels = {}
    tarjetas_normales = {}
    tarjetas_info = {}

    def crear_tarjeta(frame, imagen_normal, imagen_info, tipo):
        tarjetas_normales[tipo] = imagen_normal
        tarjetas_info[tipo] = imagen_info

        lbl = tk.Label(frame, image=imagen_normal, bg="#1e1e2e", cursor="hand2")
        lbl.pack(side="left", padx=2)

        tarjetas_labels[tipo] = lbl

        def click_tarjeta():
            seleccionar(tipo)

            for t, label in tarjetas_labels.items():
                label.config(image=tarjetas_normales[t])

            lbl.config(image=tarjetas_info[tipo])

        lbl.bind("<Button-1>", lambda e: click_tarjeta())
        lbl.bind("<Enter>", lambda e: lbl.config(bg="#2e2e45"))
        lbl.bind("<Leave>", lambda e: lbl.config(bg="#1e1e2e"))

    def mostrar_fase_defensor():
        ronda = ronda_actual[0]

        lbl_ronda.config(text=f"Ronda {partida.ronda_actual}")
        lbl_fase.config(text=f"DEFENSOR: {ronda.jugador_defensor.username}")
        lbl_dinero.config(text=f"Dinero: {ronda.dinero_defensor}")
        lbl_log.config(text="")

        tipo_seleccionado[0] = None
        mostrar_grilla()

        for w in frame_tipos.winfo_children():
            w.destroy()

        tarjetas = {}
        tarjetas_labels.clear()
        tarjetas_normales.clear()
        tarjetas_info.clear()

        img_olimpo = cargar_tarjeta("tarjeta_olimpo")
        img_oscura = cargar_tarjeta("tarjeta_oscura")
        img_volcan = cargar_tarjeta("tarjeta_volcan")
        img_madera = cargar_tarjeta("tarjeta_madera")
        img_metal = cargar_tarjeta("tarjeta_metal")

        info_olimpo = cargar_tarjeta("info_olimpo")
        info_oscura = cargar_tarjeta("info_oscura")
        info_volcan = cargar_tarjeta("info_volcan")
        info_madera = cargar_tarjeta("info_madera")
        info_metal = cargar_tarjeta("info_metal")

        tarjetas["olimpo"] = img_olimpo
        tarjetas["oscura"] = img_oscura
        tarjetas["volcan"] = img_volcan
        tarjetas["madera"] = img_madera
        tarjetas["metal"] = img_metal

        tarjetas["info_olimpo"] = info_olimpo
        tarjetas["info_oscura"] = info_oscura
        tarjetas["info_volcan"] = info_volcan
        tarjetas["info_madera"] = info_madera
        tarjetas["info_metal"] = info_metal

        frame_torres = tk.Frame(frame_tipos, bg="#1e1e2e")
        frame_torres.pack(pady=(0, 2))

        tk.Label(frame_torres, text="TORRES", bg="#1e1e2e", fg="#f6d32d",
                 font=("Arial", 10, "bold")).pack()

        fila_torres = tk.Frame(frame_torres, bg="#1e1e2e")
        fila_torres.pack()

        crear_tarjeta(fila_torres, img_olimpo, info_olimpo, "olimpo")
        crear_tarjeta(fila_torres, img_oscura, info_oscura, "oscura")
        crear_tarjeta(fila_torres, img_volcan, info_volcan, "volcan")

        frame_muros = tk.Frame(frame_tipos, bg="#1e1e2e")
        frame_muros.pack(pady=(2, 5))

        tk.Label(
            frame_muros,
            text="MUROS",
            bg="#1e1e2e",
            fg="#f6d32d",
            font=("Arial", 10, "bold")
        ).pack()

        fila_muros = tk.Frame(frame_muros, bg="#1e1e2e")
        fila_muros.pack()

        crear_tarjeta(fila_muros, img_madera, info_madera, "madera")
        crear_tarjeta(fila_muros, img_metal, info_metal, "metal")

        btn_accion.config(
            text="⚔ TERMINAR COLOCACIÓN ⚔",
            bg="#f6d32d",
            fg="#1e1e2e",
            activebackground="#ffd966",
            activeforeground="#000000",
            state="normal",
            command=mostrar_fase_atacante
        )

        canvas.bind("<Button-1>", clic_defensor)
        win.tarjetas_defensor = tarjetas

    def clic_defensor(event):
        col = event.x // CELL
        fila = event.y // CELL

        if not (0 <= fila < 10 and 0 <= col < 10):
            return

        tipo = tipo_seleccionado[0]

        if not tipo:
            lbl_log.config(text="Primero selecciona un tipo.")
            return

        ronda = ronda_actual[0]

        if tipo in Torre.TIPOS:
            ok, msg = ronda.defensor_colocar_torre(tipo, fila, col)
        else:
            ok, msg = ronda.defensor_colocar_muro(tipo, fila, col)

        lbl_log.config(text=msg)
        lbl_dinero.config(text=f"Dinero: {ronda.dinero_defensor}")
        dibujar_entidades()

    def mostrar_fase_atacante():
        ronda = ronda_actual[0]

        lbl_fase.config(text=f"ATACANTE: {ronda.jugador_atacante.username}")
        lbl_dinero.config(text=f"Dinero: {ronda.dinero_atacante}")
        lbl_log.config(text="")

        tipo_seleccionado[0] = None
        mostrar_grilla()

        for w in frame_tipos.winfo_children():
            w.destroy()
        tarjetas_labels.clear()
        tarjetas_normales.clear()
        tarjetas_info.clear()
        tarjetas_atacante = {}

        img_flecha = cargar_tarjeta("tarjeta_flecha")
        img_ninja_card = cargar_tarjeta("tarjeta_ninja")
        img_reina = cargar_tarjeta("tarjeta_hielo")
        img_rey_card = cargar_tarjeta("tarjeta_rey")
        img_fireball = cargar_tarjeta("tarjeta_fuego")
        info_flecha = cargar_tarjeta("info_flecha")
        info_ninja = cargar_tarjeta("info_ninja")
        info_hielo = cargar_tarjeta("info_hielo")
        info_rey = cargar_tarjeta("info_rey")
        info_fuego = cargar_tarjeta("info_fuego")

        tarjetas_atacante["flechas"] = img_flecha
        tarjetas_atacante["ninja"] = img_ninja_card
        tarjetas_atacante["reina_hielo"] = img_reina
        tarjetas_atacante["rey_barbaro"] = img_rey_card
        tarjetas_atacante["fireball"] = img_fireball

        tarjetas_atacante["info_flecha"] = info_flecha
        tarjetas_atacante["info_ninja"] = info_ninja
        tarjetas_atacante["info_hielo"] = info_hielo
        tarjetas_atacante["info_rey"] = info_rey
        tarjetas_atacante["info_fuego"] = info_fuego

        tk.Label(frame_tipos, text="UNIDADES", bg="#1e1e2e", fg="#f6d32d",
                 font=("Arial", 10, "bold")).pack(pady=(4, 8))

        fila1 = tk.Frame(frame_tipos, bg="#1e1e2e")
        fila1.pack(pady=3)

        fila2 = tk.Frame(frame_tipos, bg="#1e1e2e")
        fila2.pack(pady=3)

        crear_tarjeta(fila1, img_flecha, info_flecha, "flechas")
        crear_tarjeta(fila1, img_ninja_card, info_ninja, "ninja")
        crear_tarjeta(fila1, img_reina, info_hielo, "reina_hielo")

        crear_tarjeta(fila2, img_rey_card, info_rey, "rey_barbaro")
        crear_tarjeta(fila2, img_fireball, info_fuego, "fireball")

        btn_accion.config(
            text="🔥 INICIAR COMBATE 🔥",
            bg="#e01b24",
            fg="white",
            activebackground="#ff4d4d",
            activeforeground="white",
            state="normal",
            command=iniciar_combate
        )

        canvas.bind("<Button-1>", clic_atacante)
        win.tarjetas_atacante = tarjetas_atacante

    def clic_atacante(event):
        col = event.x // CELL
        fila = event.y // CELL

        if not (0 <= fila < 10 and 0 <= col < 10):
            return

        tipo = tipo_seleccionado[0]

        if not tipo:
            lbl_log.config(text="Primero selecciona un tipo.")
            return

        ronda = ronda_actual[0]
        ok, msg = ronda.atacante_colocar_unidad(tipo, fila, col)

        lbl_log.config(text=msg)
        lbl_dinero.config(text=f"Dinero: {ronda.dinero_atacante}")
        dibujar_entidades()

    def iniciar_combate():
        canvas.unbind("<Button-1>")
        ocultar_grilla()

        for w in frame_tipos.winfo_children():
            w.destroy()

        lbl_fase.config(text="COMBATE")
        btn_accion.config(state="disabled")

        turno[0] = 1
        auto_turno()

    def auto_turno():
        ronda = ronda_actual[0]
        ronda.ejecutar_turno_combate()
        dibujar_entidades()

        base = ronda.mapa.base
        lbl_dinero.config(text=f"Base: {base.vida}/{base.vida_max}")
        lbl_log.config(text=f"Turno {turno[0]}")
        turno[0] += 1

        if ronda.terminada:
            partida.registrar_resultado_ronda(ronda.ganador_rol)

            ganador = "ATACANTE" if ronda.ganador_rol == "atacante" else "DEFENSOR"
            lbl_log.config(text=f"¡Ganó el {ganador}!")
            btn_accion.config(state="normal")

            if partida.terminada:
                partida.actualizar_victorias_jugadores()
                ventana_felicitaciones(win, partida.ganador)

                btn_accion.config(
                    text=f"🏆 ¡{partida.ganador.username} gana! 🏆",
                    bg="#26a269",
                    fg="white",
                    command=lambda: None
                )
            else:
                btn_accion.config(state="disabled")
                ventana_siguiente_ronda(
                    win,
                    f"Siguiente ronda | {jugador1.username}: {partida.victorias_j1} - {jugador2.username}: {partida.victorias_j2}",
                    iniciar_ronda
                )
        else:
            win.after(700, auto_turno)

    def iniciar_ronda():
        ronda_actual[0] = partida.iniciar_ronda()
        tipo_seleccionado[0] = None
        turno[0] = 1

        dibujar_fondo()
        dibujar_entidades()
        mostrar_fase_defensor()

    win.img_base_verde = img_base_verde
    win.img_base_morada = img_base_morada
    win.img_base_roja = img_base_roja
    win.img_muro_madera = img_muro_madera
    win.img_muro_metal = img_muro_metal
    win.img_rey = img_rey
    win.img_ninja = img_ninja
    win.img_hielo = img_hielo
    win.img_fire = img_fire
    win.img_flechas = img_flechas
    iniciar_ronda()
vtn_principal()



