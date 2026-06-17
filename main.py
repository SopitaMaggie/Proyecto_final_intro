import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from usuario import registrar_jugador, iniciar_sesion, obtener_ranking
from juego import Partida, BaseCentral
from defensor import Torre, Muro
from atacante import Unidad

def vtn_principal():  #vtn: ventana
    vtn = tk.Tk()
    vtn.title("Defensa y Asalto")
    vtn.geometry("1300x800")
    vtn.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(
        Image.open("Imagenes/inicio.png").resize((1300, 800))
    )
    img_jugar = ImageTk.PhotoImage(
        Image.open("Imagenes/btn_jugar.png").resize((600, 350))
    )
    img_registrar = ImageTk.PhotoImage(
        Image.open("Imagenes/btn_login.png").resize((600, 350))
    )
    img_ranking = ImageTk.PhotoImage(
        Image.open("Imagenes/btn_ranking.png").resize((600, 350))
    )
    img_info = ImageTk.PhotoImage(
        Image.open("Imagenes/btn_info.png").resize((600, 350))
    )
    img_salir = ImageTk.PhotoImage(
        Image.open("Imagenes/btn_salir.png").resize((600, 350))
    )
    canvas = tk.Canvas(
        vtn,
        width=1300,
        height=800,
        highlightthickness=0
    )
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0,0,
        image=img_fondo,
        anchor="nw"
    )
    # POSICIONES 
    X_BOTONES = 670
    Y_INICIAL = 360
    ESPACIO = 85
#botones
    canvas.create_image(
        X_BOTONES,
        Y_INICIAL,
        image=img_jugar
    )
    canvas.create_image(
        X_BOTONES,
        Y_INICIAL + ESPACIO,
        image=img_registrar
    )
    canvas.create_image(
        X_BOTONES,
        Y_INICIAL + ESPACIO * 2,
        image=img_ranking
    )
    canvas.create_image(
        X_BOTONES,
        Y_INICIAL + ESPACIO * 3,
        image=img_info
    )
    canvas.create_image(
        X_BOTONES,
        Y_INICIAL + ESPACIO * 4,
        image=img_salir
    )

    def Zclick(x1, y1, x2, y2, funcion):
        zona = canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            outline="",
            fill=""
        )
        canvas.tag_bind(
            zona,
            "<Button-1>",
            lambda e: funcion()
        )
        canvas.tag_bind(
            zona,
            "<Enter>",
            lambda e: canvas.config(cursor="hand2")
        )
        canvas.tag_bind(
            zona,
            "<Leave>",
            lambda e: canvas.config(cursor="")
        )
        return zona
    Zclick(
        430,
        325,
        910,
        395,
        lambda: vtn_iniciar_sesion(vtn)
    )
    Zclick(
        430,
        410,
        910,
        480,
        lambda: vtn_registrarse(vtn)
    )
    Zclick(
        430,
        495,
        910,
        565,
        lambda: vtn_ranking(vtn)
    )
    Zclick(
        430,
        580,
        910,
        650,
        lambda: vtn_informacion(vtn)
    )
    Zclick(
        430,
        665,
        910,
        735,
        vtn.destroy
    )
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
    win.geometry("350x300")
    win.resizable(False, False)

    tk.Label(win, text="REGISTRARSE", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Label(win, text="Username:", font=("Arial", 11)).pack()
    entry_user = tk.Entry(win, font=("Arial", 11))
    entry_user.pack(pady=5)

    tk.Label(win, text="Password:", font=("Arial", 11)).pack()
    entry_pass = tk.Entry(win, font=("Arial", 11), show="*")
    entry_pass.pack(pady=5)

    tk.Label(win, text="Nombre (opcional):", font=("Arial", 11)).pack()
    entry_nombre = tk.Entry(win, font=("Arial", 11))
    entry_nombre.pack(pady=5)

    def registrar():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()
        nombre = entry_nombre.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Username y password son obligatorios.", parent=win)
            return
        jugador, msg = registrar_jugador(username, password, nombre)
        if jugador:
            win.destroy()
            vtn_registro_exitoso(principal)
        else:
            messagebox.showerror("Error", msg, parent=win)

    tk.Button(win, text="Registrarse", width=15, font=("Arial", 11), command=registrar).pack(pady=15)


def vtn_registro_exitoso(principal):
    win = tk.Toplevel(principal)
    win.title("Registro exitoso")
    win.geometry("300x200")
    win.resizable(False, False)

    tk.Label(win, text="¡Registro exitoso!", font=("Arial", 14, "bold")).pack(pady=40)
    tk.Label(win, text="Ya puedes iniciar sesión.", font=("Arial", 11)).pack()
    tk.Button(win, text="Volver al menú", font=("Arial", 11), command=win.destroy).pack(pady=20)


def vtn_iniciar_sesion(principal):
    win = tk.Toplevel(principal)
    win.title("Iniciar sesión")
    win.geometry("350x250")
    win.resizable(False, False)

    tk.Label(win, text="INICIAR SESIÓN", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Label(win, text="Username:", font=("Arial", 11)).pack()
    entry_user = tk.Entry(win, font=("Arial", 11))
    entry_user.pack(pady=5)

    tk.Label(win, text="Password:", font=("Arial", 11)).pack()
    entry_pass = tk.Entry(win, font=("Arial", 11), show="*")
    entry_pass.pack(pady=5)

    def login():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()
        jugador, msg = iniciar_sesion(username, password)
        if jugador:
            win.destroy()
            vtn_menu_juego(principal, jugador)
        else:
            messagebox.showerror("Error", msg, parent=win)

    tk.Button(win, text="Iniciar sesión", width=15, font=("Arial", 11), command=login).pack(pady=15)


def vtn_menu_juego(principal, jugador):
    win = tk.Toplevel(principal)
    win.title("Menú de juego")
    win.geometry("400x300")
    win.resizable(False, False)

    tk.Label(win, text=f"Bienvenido, {jugador.username}!", font=("Arial", 16, "bold")).pack(pady=30)

    tk.Button(win, text="Nueva partida", width=20, font=("Arial", 12),
              command=lambda: vtn_segunda_sesion(win, jugador)).pack(pady=8)
    tk.Button(win, text="Ver ranking", width=20, font=("Arial", 12),
              command=lambda: vtn_ranking(win)).pack(pady=8)
    tk.Button(win, text="Cerrar sesión", width=20, font=("Arial", 12),
              command=win.destroy).pack(pady=8)


def vtn_segunda_sesion(menu_win, jugador1):
    win = tk.Toplevel(menu_win)
    win.title("Segundo jugador")
    win.geometry("350x250")
    win.resizable(False, False)

    tk.Label(win, text="SEGUNDO JUGADOR", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Label(win, text="Username:", font=("Arial", 11)).pack()
    entry_user = tk.Entry(win, font=("Arial", 11))
    entry_user.pack(pady=5)

    tk.Label(win, text="Password:", font=("Arial", 11)).pack()
    entry_pass = tk.Entry(win, font=("Arial", 11), show="*")
    entry_pass.pack(pady=5)

    def login_j2():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()
        jugador2, msg = iniciar_sesion(username, password)
        if jugador2:
            win.destroy()
            vtn_partida(menu_win, jugador1, jugador2)
        else:
            messagebox.showerror("Error", msg, parent=win)

    tk.Button(win, text="Iniciar sesión", width=15, font=("Arial", 11), command=login_j2).pack(pady=15)


def vtn_ranking(padre):
    win = tk.Toplevel(padre)
    win.title("Ranking")
    win.geometry("350x400")
    win.resizable(False, False)

    tk.Label(win, text="RANKING", font=("Arial", 16, "bold")).pack(pady=15)

    ranking_def, ranking_atk = obtener_ranking()

    tk.Label(win, text="TOP 5 DEFENSORES", font=("Arial", 12, "bold")).pack()
    for i, j in enumerate(ranking_def, 1):
        tk.Label(win, text=f"{i}. {j.username} - {j.victorias_defensor} victorias",
                 font=("Arial", 11)).pack()

    tk.Label(win, text="").pack()
    tk.Label(win, text="TOP 5 ATACANTES", font=("Arial", 12, "bold")).pack()
    for i, j in enumerate(ranking_atk, 1):
        tk.Label(win, text=f"{i}. {j.username} - {j.victorias_atacante} victorias",
                 font=("Arial", 11)).pack()

    tk.Button(win, text="Cerrar", font=("Arial", 11), command=win.destroy).pack(pady=15)


def vtn_informacion(padre):
    win = tk.Toplevel(padre)
    win.title("Información")
    win.geometry("400x350")
    win.resizable(False, False)

    tk.Label(win, text="INFORMACIÓN", font=("Arial", 16, "bold")).pack(pady=15)

    info = (
        "Defensa y Asalto es un juego de estrategia\n"
        "para 2 jugadores.\n\n"
        "El defensor coloca torres y muros para\n"
        "proteger su base central.\n\n"
        "El atacante coloca unidades para destruir\n"
        "la base del defensor.\n\n"
        "Gana el primero en ganar 3 rondas."
    )
    tk.Label(win, text=info, font=("Arial", 11), justify="center").pack(pady=10)
    tk.Button(win, text="Cerrar", font=("Arial", 11), command=win.destroy).pack(pady=15)



CELL = 52  # tamaño de cada celda en píxeles

# Colores y etiquetas por tipo de entidad
ESTILOS = {
    "olimpo":      ("#1a5fb4", "OLI"),
    "oscura":      ("#5e35b1", "OSC"),
    "volcan":      ("#b5381d", "VOL"),
    "madera":      ("#a0785a", "MUR"),
    "metal":       ("#5e6264", "MET"),
    "flechas":     ("#e07b00", "FLE"),
    "ninja":       ("#2d3436", "NIN"),
    "reina_hielo": ("#4fc3f7", "REI"),
    "rey_barbaro": ("#7b3f00", "REY"),
    "fireball":    ("#e01b24", "FIR"),
}


def vtn_partida(padre, jugador1, jugador2):
    partida = Partida(jugador1, jugador2)

    win = tk.Toplevel(padre)
    win.title("Partida")
    win.resizable(False, False)

    ronda_actual = [None]
    tipo_seleccionado = [None]
    turno = [1]


    frame_info = tk.Frame(win, bg="#1e1e2e", width=210, padx=10, pady=10)
    frame_info.grid(row=0, column=0, sticky="ns")
    frame_info.grid_propagate(False)

    canvas = tk.Canvas(win, width=10 * CELL, height=10 * CELL)
    canvas.grid(row=0, column=1)


    for i in range(10):
        for j in range(10):
            if j <= 4:
                color = "#6aaa3c" if (i + j) % 2 == 0 else "#5e9c33"
            else:
                color = "#8b7355" if (i + j) % 2 == 0 else "#7d6648"
            canvas.create_rectangle(j * CELL, i * CELL,
                                    (j + 1) * CELL, (i + 1) * CELL,
                                    fill=color, outline="", tags="fondo")

    # Resaltar casilla de la base
    canvas.create_rectangle(9 * CELL + 3, 4 * CELL + 3,
                            10 * CELL - 3, 5 * CELL - 3,
                            fill="#f6d32d", outline="#e5a50a", width=2, tags="fondo")


    s = {"bg": "#1e1e2e", "fg": "white"}

    lbl_ronda = tk.Label(frame_info, text="", font=("Arial", 13, "bold"), **s)
    lbl_ronda.pack(pady=(5, 2))

    lbl_fase = tk.Label(frame_info, text="", font=("Arial", 10), **s)
    lbl_fase.pack()

    lbl_dinero = tk.Label(frame_info, text="", font=("Arial", 10), **s)
    lbl_dinero.pack(pady=(0, 10))

    tk.Label(frame_info, text="Selecciona tipo:", font=("Arial", 10, "bold"), **s).pack()

    frame_tipos = tk.Frame(frame_info, bg="#1e1e2e")
    frame_tipos.pack()

    lbl_log = tk.Label(frame_info, text="", font=("Arial", 9),
                       wraplength=190, justify="left", fg="#a6e3a1", bg="#1e1e2e")
    lbl_log.pack(pady=8)

    btn_accion = tk.Button(frame_info, font=("Arial", 10), width=18)
    btn_accion.pack(pady=5)


    def dibujar_entidades():
        canvas.delete("entidad")
        ronda = ronda_actual[0]
        for i in range(10):
            for j in range(10):
                celda = ronda.mapa.obtener(i, j)
                if celda is None:
                    continue
                cx = j * CELL + CELL // 2
                cy = i * CELL + CELL // 2
                x1, y1 = j * CELL + 5, i * CELL + 5
                x2, y2 = (j + 1) * CELL - 5, (i + 1) * CELL - 5

                if isinstance(celda, BaseCentral):
                    pct = celda.vida / celda.vida_max
                    barra = int((CELL - 10) * pct)
                    canvas.create_rectangle(x1, y1, x1 + barra, y1 + 7,
                                            fill="#26a269", outline="", tags="entidad")
                    canvas.create_text(cx, cy + 4, text=f"BASE\n{celda.vida}",
                                       fill="#1a1a1a", font=("Arial", 7, "bold"), tags="entidad")

                elif isinstance(celda, Torre):
                    color, letra = ESTILOS[celda.tipo]
                    canvas.create_rectangle(x1, y1, x2, y2, fill=color,
                                            outline="white", width=1, tags="entidad")
                    canvas.create_text(cx, cy, text=letra, fill="white",
                                       font=("Arial", 8, "bold"), tags="entidad")

                elif isinstance(celda, Muro):
                    color, letra = ESTILOS[celda.tipo]
                    canvas.create_rectangle(x1, y1, x2, y2, fill=color,
                                            outline="white", width=1, tags="entidad")
                    canvas.create_text(cx, cy, text=letra, fill="white",
                                       font=("Arial", 8, "bold"), tags="entidad")

                elif isinstance(celda, Unidad):
                    color, letra = ESTILOS[celda.tipo]
                    canvas.create_oval(x1, y1, x2, y2, fill=color,
                                       outline="white", width=1, tags="entidad")
                    canvas.create_text(cx, cy, text=letra, fill="white",
                                       font=("Arial", 8, "bold"), tags="entidad")


    def iniciar_ronda():
        ronda_actual[0] = partida.iniciar_ronda()
        tipo_seleccionado[0] = None
        turno[0] = 1
        dibujar_entidades()
        mostrar_fase_defensor()


    def mostrar_fase_defensor():
        ronda = ronda_actual[0]
        lbl_ronda.config(text=f"Ronda {partida.ronda_actual}")
        lbl_fase.config(text=f"DEFENSOR: {ronda.jugador_defensor.username}")
        lbl_dinero.config(text=f"Dinero: {ronda.dinero_defensor}")
        lbl_log.config(text="")

        for w in frame_tipos.winfo_children():
            w.destroy()

        opciones = [("olimpo", 150), ("oscura", 70), ("volcan", 200),
                    ("madera", 30), ("metal", 80)]
        for tipo, costo in opciones:
            color = ESTILOS[tipo][0]
            tk.Button(frame_tipos, text=f"{tipo} (${costo})", width=16,
                      font=("Arial", 8), bg=color, fg="black",
                      command=lambda t=tipo: seleccionar(t)).pack(pady=2)

        btn_accion.config(text="Terminar colocación", bg="#e0c800", fg="black",
                          command=lambda: mostrar_fase_atacante())
        canvas.bind("<Button-1>", clic_defensor)

    def clic_defensor(event):
        col = event.x // CELL
        fila = event.y // CELL
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

        for w in frame_tipos.winfo_children():
            w.destroy()

        opciones = [("flechas", 40), ("ninja", 90), ("reina_hielo", 120),
                    ("rey_barbaro", 160), ("fireball", 170)]
        for tipo, costo in opciones:
            color = ESTILOS[tipo][0]
            tk.Button(frame_tipos, text=f"{tipo} (${costo})", width=16,
                      font=("Arial", 8), bg=color, fg="black",
                      command=lambda t=tipo: seleccionar(t)).pack(pady=2)

        btn_accion.config(text="Iniciar combate", bg="#e01b24", fg="white",
                          command=lambda: iniciar_combate())
        canvas.bind("<Button-1>", clic_atacante)

    def clic_atacante(event):
        col = event.x // CELL
        fila = event.y // CELL
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
                btn_accion.config(text=f"¡{partida.ganador.username} gana!",
                                  bg="#26a269", fg="white", command=lambda: None)
            else:
                btn_accion.config(text="Siguiente ronda", bg="#1a5fb4", fg="white",
                                  command=iniciar_ronda)
        else:
            win.after(700, auto_turno)

    def seleccionar(tipo):
        tipo_seleccionado[0] = tipo
        lbl_log.config(text=f"Seleccionado: {tipo}")

    iniciar_ronda()



vtn_principal()
