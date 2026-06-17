from defensor import Torre, Muro
from atacante import Unidad

filas = 10
columnas = 10
dinero_inicial = 300
dinero_por_ronda = 150
vida_base = 200
rondas_para_ganar = 3

# Posicion fija de la base en el mapa
base_fila = 4
base_col = 9


class BaseCentral:
    def __init__(self):
        self.vida_max = vida_base
        self.vida = vida_base

    def mostrar(self):
        print("Base Central")
        print("Vida:", self.vida, "/", self.vida_max)

    def recibir_dano(self, cantidad):
        self.vida = max(0, self.vida - cantidad)

    def esta_en_pie(self):
        return self.vida > 0



class Mapa:
    VACIO = None

    def __init__(self):
        self.grid = [[self.VACIO for _ in range(columnas)] for _ in range(filas)]
        self.base = BaseCentral()
        self.grid[base_fila][base_col] = self.base

    def colocar(self, entidad, fila, col):
        if not self._valida(fila, col):
            return False, "Posición fuera del mapa."
        if self.grid[fila][col] is not None:
            return False, "Casilla ocupada."
        # La base no puede ser tapada
        if fila == base_fila and col == base_col:
            return False, "No puedes colocar nada sobre la base."
        self.grid[fila][col] = entidad
        return True, "Colocado."

    def eliminar(self, fila, col):
        if self._valida(fila, col):
            self.grid[fila][col] = self.VACIO

    def obtener(self, fila, col):
        if self._valida(fila, col):
            return self.grid[fila][col]
        return None

    def _valida(self, fila, col):
        return 0 <= fila < filas and 0 <= col < columnas

    def torres_activas(self):
        torres = []
        for fila in self.grid:
            for celda in fila:
                if isinstance(celda, Torre) and celda.esta_viva():
                    torres.append(celda)
        return torres

    def muros_activos(self):
        muros = []
        for fila in self.grid:
            for celda in fila:
                if isinstance(celda, Muro) and celda.esta_en_pie():
                    muros.append(celda)
        return muros

    def unidades_activas(self):
        unidades = []
        for fila in self.grid:
            for celda in fila:
                if isinstance(celda, Unidad) and celda.esta_viva():
                    unidades.append(celda)
        return unidades

    def torres_cercanas(self, fila, col, radio=1):
        cercanas = []
        for df in range(-radio, radio + 1):
            for dc in range(-radio, radio + 1):
                if df == 0 and dc == 0:
                    continue
                celda = self.obtener(fila + df, col + dc)
                if isinstance(celda, Torre) and celda.esta_viva():
                    cercanas.append(celda)
        return cercanas

    def imprimir(self):
        simbolos = {
            "vacio": ".",
            "torre": "T",
            "muro": "M",
            "unidad": "U",
            "base": "B"
        }
        print("  " + " ".join(str(c) for c in range(columnas)))
        for i, fila in enumerate(self.grid):
            fila_str = f"{i} "
            for celda in fila:
                if celda is None:
                    fila_str += simbolos["vacio"] + " "
                elif isinstance(celda, Torre):
                    fila_str += simbolos["torre"] + " "
                elif isinstance(celda, Muro):
                    fila_str += simbolos["muro"] + " "
                elif isinstance(celda, Unidad):
                    fila_str += simbolos["unidad"] + " "
                elif isinstance(celda, BaseCentral):
                    fila_str += simbolos["base"] + " "
                else:
                    fila_str += "? "
            print(fila_str)


class Ronda:
    def __init__(self, numero, jugador_defensor, jugador_atacante):
        self.numero = numero
        self.jugador_defensor = jugador_defensor
        self.jugador_atacante = jugador_atacante
        self.mapa = Mapa()
        self.dinero_defensor = dinero_inicial + (numero - 1) * dinero_por_ronda
        self.dinero_atacante = dinero_inicial + (numero - 1) * dinero_por_ronda
        self.terminada = False
        self.ganador_rol = None  # "defensor" o "atacante"

    # --- Fase de colocación del defensor ---

    def defensor_colocar_torre(self, tipo, fila, col):
        if tipo not in Torre.TIPOS:
            return False, "Tipo de torre inválido."
        torre = Torre(tipo)
        if self.dinero_defensor < torre.costo:
            return False, "Dinero insuficiente."
        ok, msg = self.mapa.colocar(torre, fila, col)
        if ok:
            self.dinero_defensor -= torre.costo
        return ok, msg

    def defensor_colocar_muro(self, tipo, fila, col):
        if tipo not in Muro.TIPOS:
            return False, "Tipo de muro inválido."
        muro = Muro(tipo)
        if self.dinero_defensor < muro.costo:
            return False, "Dinero insuficiente."
        ok, msg = self.mapa.colocar(muro, fila, col)
        if ok:
            self.dinero_defensor -= muro.costo
        return ok, msg

    # --- Fase de colocación del atacante ---

    def atacante_colocar_unidad(self, tipo, fila, col):
        if tipo not in Unidad.TIPOS:
            return False, "Tipo de unidad inválido."
        unidad = Unidad(tipo)
        if self.dinero_atacante < unidad.costo:
            return False, "Dinero insuficiente."
        ok, msg = self.mapa.colocar(unidad, fila, col)
        if ok:
            self.dinero_atacante -= unidad.costo
        return ok, msg



    def ejecutar_turno_combate(self):
        if self.terminada:
            return


        for i in range(filas):
            for j in range(columnas):
                celda = self.mapa.obtener(i, j)
                if isinstance(celda, Torre) and celda.esta_viva():
                    objetivo = self._buscar_unidad_en_alcance(i, j, celda.alcance)
                    if objetivo:
                        if celda.tipo == "volcan" and celda.contador_habilidad + 1 >= celda.turnos_habilidad:
                            torres_cercanas = self.mapa.torres_cercanas(i, j)
                            celda.usar_habilidad(torres_cercanas)
                            celda.contador_habilidad = 0
                        else:
                            celda.atacar(objetivo)
                        if not objetivo.esta_viva():
                            self._eliminar_unidad(objetivo)
                            self.dinero_defensor += 20  # dinero por eliminar unidad

        for i in range(filas):
            for j in range(columnas):
                celda = self.mapa.obtener(i, j)
                if isinstance(celda, Unidad) and celda.esta_viva():
                    celda.aplicar_veneno()
                    if not celda.esta_viva():
                        self._eliminar_unidad(celda)
                        self.dinero_defensor += 20
                        continue
                    objetivo = self._buscar_torre_o_base_cercana(i, j)
                    if objetivo:
                        if celda.tipo == "fireball":
                            objetivos_area = self._buscar_objetivos_area(i, j)
                            if celda.contador_habilidad + 1 >= celda.turnos_habilidad:
                                celda.usar_habilidad(objetivos_area)
                                celda.contador_habilidad = 0
                            else:
                                celda.atacar(objetivo)
                        else:
                            celda.atacar(objetivo)
                        if isinstance(objetivo, BaseCentral):
                            self.dinero_atacante += 15
                        elif isinstance(objetivo, Torre) and not objetivo.esta_viva():
                            self._eliminar_torre(objetivo)
                            self.dinero_atacante += 30

        # Mover unidades hacia la base (de derecha a izquierda para no moverlas dos veces)
        for i in range(filas):
            for j in range(columnas - 2, -1, -1):
                celda = self.mapa.obtener(i, j)
                if isinstance(celda, Unidad) and celda.esta_viva():
                    objetivo = self._buscar_torre_o_base_cercana(i, j)
                    if not objetivo:
                        pasos = celda.velocidad
                        nueva_col = j
                        for _ in range(pasos):
                            if nueva_col + 1 >= columnas:
                                break
                            siguiente = self.mapa.obtener(i, nueva_col + 1)
                            if siguiente is None:
                                nueva_col += 1
                            else:
                                break
                        if nueva_col != j:
                            self.mapa.grid[i][j] = None
                            self.mapa.grid[i][nueva_col] = celda

        if not self.mapa.base.esta_en_pie(): # Verificar si la base fue destruida
            self.terminada = True
            self.ganador_rol = "atacante"
            return

        if not self.mapa.unidades_activas() and self.dinero_atacante < min(
            Unidad.TIPOS[t]["costo"] for t in Unidad.TIPOS
        ):
            self.terminada = True
            self.ganador_rol = "defensor"

    def _buscar_unidad_en_alcance(self, fila, col, alcance):
        for df in range(-alcance, alcance + 1):
            for dc in range(-alcance, alcance + 1):
                celda = self.mapa.obtener(fila + df, col + dc)
                if isinstance(celda, Unidad) and celda.esta_viva():
                    return celda
        return None

    def _buscar_torre_o_base_cercana(self, fila, col):
        for df in range(-1, 2):
            for dc in range(-1, 2):
                celda = self.mapa.obtener(fila + df, col + dc)
                if isinstance(celda, (Torre, BaseCentral)):
                    return celda
        return None

    def _buscar_objetivos_area(self, fila, col, radio=2):
        objetivos = []
        for df in range(-radio, radio + 1):
            for dc in range(-radio, radio + 1):
                celda = self.mapa.obtener(fila + df, col + dc)
                if isinstance(celda, (Torre, BaseCentral)):
                    objetivos.append(celda)
        return objetivos

    def _eliminar_unidad(self, unidad):
        for i in range(filas):
            for j in range(columnas):
                if self.mapa.obtener(i, j) is unidad:
                    self.mapa.eliminar(i, j)
                    return

    def _eliminar_torre(self, torre):
        for i in range(filas):
            for j in range(columnas):
                if self.mapa.obtener(i, j) is torre:
                    self.mapa.eliminar(i, j)
                    return


class Partida:
    def __init__(self, jugador1, jugador2):
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.victorias_j1 = 0
        self.victorias_j2 = 0
        self.ronda_actual = 1
        self.terminada = False
        self.ganador = None
        self.defensor_actual = jugador1
        self.atacante_actual = jugador2

    def iniciar_ronda(self):
        return Ronda(self.ronda_actual, self.defensor_actual, self.atacante_actual)

    def registrar_resultado_ronda(self, ganador_rol):
        if ganador_rol == "defensor":
            if self.defensor_actual is self.jugador1:
                self.victorias_j1 += 1
            else:
                self.victorias_j2 += 1
        elif ganador_rol == "atacante":
            if self.atacante_actual is self.jugador1:
                self.victorias_j1 += 1
            else:
                self.victorias_j2 += 1

        if self.victorias_j1 >= rondas_para_ganar:
            self.terminada = True
            self.ganador = self.jugador1
        elif self.victorias_j2 >= rondas_para_ganar:
            self.terminada = True
            self.ganador = self.jugador2
        else:
            self.defensor_actual, self.atacante_actual = self.atacante_actual, self.defensor_actual
            self.ronda_actual += 1

    def actualizar_victorias_jugadores(self):
        from usuario import actualizar_jugador
        if self.ganador is self.jugador1:
            rol_ganador = "defensor" if self.defensor_actual is self.jugador1 else "atacante"
            self.jugador1.agregar_victoria(rol_ganador)
        elif self.ganador is self.jugador2:
            rol_ganador = "defensor" if self.defensor_actual is self.jugador2 else "atacante"
            self.jugador2.agregar_victoria(rol_ganador)
        actualizar_jugador(self.jugador1)
        actualizar_jugador(self.jugador2)
