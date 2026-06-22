from defensor import Torre, Muro
from atacante import Unidad

filas = 10
columnas = 10

dinero_inicial_defensor = 400
dinero_inicial_atacante = 500
dinero_por_ronda_defensor = 75
dinero_por_ronda_atacante = 100

vida_base = 250
rondas_para_ganar = 3

base_fila = 4
base_col = 9

recompensa_defensor_eliminar_unidad = 25
recompensa_atacante_danar_base = 10
recompensa_atacante_destruir_torre = 35

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

        if fila == base_fila and col == base_col:
            return False, "No puedes colocar nada sobre la base."

        if self.grid[fila][col] is not None:
            return False, "Casilla ocupada."

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

class Ronda:
    def __init__(self, numero, jugador_defensor, jugador_atacante):
        self.numero = numero
        self.jugador_defensor = jugador_defensor
        self.jugador_atacante = jugador_atacante
        self.mapa = Mapa()
        self.dinero_defensor = dinero_inicial_defensor + (numero - 1) * dinero_por_ronda_defensor
        self.dinero_atacante = dinero_inicial_atacante + (numero - 1) * dinero_por_ronda_atacante
        self.terminada = False
        self.ganador_rol = None
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
        self._turno_torres()
        self._turno_unidades()
        self._mover_unidades()
        self._verificar_ganador()
    def _turno_torres(self):
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
                            self.dinero_defensor += recompensa_defensor_eliminar_unidad
    def _turno_unidades(self):
        for i in range(filas):
            for j in range(columnas):
                celda = self.mapa.obtener(i, j)
                if isinstance(celda, Unidad) and celda.esta_viva():
                    celda.aplicar_veneno()
                    if not celda.esta_viva():
                        self._eliminar_unidad(celda)
                        self.dinero_defensor += recompensa_defensor_eliminar_unidad
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
                            self.dinero_atacante += recompensa_atacante_danar_base
                        elif isinstance(objetivo, Torre) and not objetivo.esta_viva():
                            self._eliminar_torre(objetivo)
                            self.dinero_atacante += recompensa_atacante_destruir_torre
    def _mover_unidades(self):
        unidades_a_mover = []
        for i in range(filas):
            for j in range(columnas):
                celda = self.mapa.obtener(i, j)
                if isinstance(celda, Unidad) and celda.esta_viva():
                    unidades_a_mover.append((i, j, celda))
        for i, j, unidad in unidades_a_mover:
            if self.mapa.obtener(i, j) is not unidad:
                continue
            objetivo = self._buscar_torre_o_base_cercana(i, j)
            if objetivo:
                continue

            fila_actual = i
            col_actual = j

            for _ in range(unidad.velocidad):
                movimientos = []
                if col_actual < base_col:
                    movimientos.append((fila_actual, col_actual + 1))
                elif col_actual > base_col:
                    movimientos.append((fila_actual, col_actual - 1))
                if fila_actual < base_fila:
                    movimientos.append((fila_actual + 1, col_actual))
                elif fila_actual > base_fila:
                    movimientos.append((fila_actual - 1, col_actual))
                movimientos.append((fila_actual - 1, col_actual))
                movimientos.append((fila_actual + 1, col_actual))
                movimientos.append((fila_actual, col_actual + 1))
                movimientos.append((fila_actual, col_actual - 1))
                se_movio = False
                for nueva_fila, nueva_col in movimientos:
                    if not (0 <= nueva_fila < filas and 0 <= nueva_col < columnas):
                        continue
                    siguiente = self.mapa.obtener(nueva_fila, nueva_col)
                    if siguiente is None:
                        self.mapa.grid[fila_actual][col_actual] = None
                        self.mapa.grid[nueva_fila][nueva_col] = unidad
                        fila_actual = nueva_fila
                        col_actual = nueva_col
                        se_movio = True
                        break
                if not se_movio:
                    break

    def _verificar_ganador(self):
        if not self.mapa.base.esta_en_pie():
            self.terminada = True
            self.ganador_rol = "atacante"
            return
        if not self.mapa.unidades_activas():
            self.terminada = True
            self.ganador_rol = "defensor"
            return

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
        return Ronda(
            self.ronda_actual,
            self.defensor_actual,
            self.atacante_actual
        )

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

        if self.victorias_j1 >= 3:
            self.terminada = True
            self.ganador = self.jugador1

        elif self.victorias_j2 >= 3:
            self.terminada = True
            self.ganador = self.jugador2

        else:
            self.defensor_actual, self.atacante_actual = (
                self.atacante_actual,
                self.defensor_actual
            )
            self.ronda_actual += 1

    def marcador(self):
        return f"{self.jugador1.username}: {self.victorias_j1} | {self.jugador2.username}: {self.victorias_j2}"

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