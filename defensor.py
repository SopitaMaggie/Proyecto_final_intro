# Contiene las estructuras defensivas:
# torres y muros.

class Torre: # Diccionario con los tipos de torres disponibles
    TIPOS = {
        "olimpo": {
            "nombre": "Torre del Olimpo",
            "vida": 180,
            "dano": 25,
            "alcance": 3,
            "habilidad": "Rayo doble que causa el doble de daño",
            "turnos_habilidad": 3
        },
        "oscura": {
            "nombre": "Torre Oscura",
            "vida": 120,
            "dano": 10,
            "alcance": 2,
            "habilidad": "Neblina venenosa que envenena enemigos",
            "turnos_habilidad": 2
        },
        "volcan": {
            "nombre": "Torre del Volcán",
            "vida": 250,
            "dano": 35,
            "alcance": 4,
            "habilidad": "Lava curativa que sana torres cercanas",
            "turnos_habilidad": 2
        }
    }

    def __init__(self, tipo):
        tipo = tipo.lower()

        if tipo not in self.TIPOS:
            raise ValueError(f"Tipo de torre inválido: {tipo}")

        datos = self.TIPOS[tipo]

        self.tipo = tipo
        self.nombre = datos["nombre"]
        self.vida_max = datos["vida"]
        self.vida = datos["vida"]
        self.dano = datos["dano"]
        self.alcance = datos["alcance"]
        self.habilidad = datos["habilidad"]
        self.turnos_habilidad = datos["turnos_habilidad"]

        self.costo = self.calcular_costo()

        self.contador_habilidad = 0
        self.congelada = 0
        self.debilitada = False

    def calcular_costo(self):
        if self.tipo == "oscura":
            return 35
        elif self.tipo == "olimpo":
            return 50
        elif self.tipo == "volcan":
            return 70

    def esta_viva(self):
        return self.vida > 0

    def recibir_dano(self, cantidad):
        if self.debilitada:
            cantidad = int(cantidad * 1.5)
            self.debilitada = False

        self.vida = max(0, self.vida - cantidad)

    def mostrar(self):
        print("Nombre:", self.nombre)
        print("Vida:", self.vida, "/", self.vida_max)
        print("Daño:", self.dano)
        print("Alcance:", self.alcance)
        print("Costo:", self.costo)
        print("Habilidad:", self.habilidad)
        print("Turnos para habilidad:", self.turnos_habilidad)

    def atacar(self, objetivo):

        if self.congelada > 0:
            self.congelada -= 1
            return 0

        self.contador_habilidad += 1

        if self.contador_habilidad >= self.turnos_habilidad:
            self.contador_habilidad = 0
            return self.usar_habilidad(objetivo)

        return self._ataque_normal(objetivo)

    def _ataque_normal(self, objetivo):

        if self.tipo == "olimpo":
            objetivo.recibir_dano(self.dano)
            return self.dano

        elif self.tipo == "oscura":
            objetivo.recibir_dano(self.dano)
            return self.dano

        elif self.tipo == "volcan":
            objetivo.recibir_dano(self.dano)
            return self.dano

        return 0

    def usar_habilidad(self, objetivo_o_lista):

        if self.tipo == "olimpo":
            # Rayo doble
            dano_total = self.dano * 2
            objetivo_o_lista.recibir_dano(dano_total)
            return dano_total

        elif self.tipo == "oscura":
            # Neblina venenosa
            objetivo_o_lista.recibir_dano(self.dano)
            objetivo_o_lista.envenenada = 1
            return self.dano

        elif self.tipo == "volcan":
            # Cura torres cercanas
            sanadas = 0

            if isinstance(objetivo_o_lista, list):

                for torre in objetivo_o_lista:

                    if torre is not self and torre.esta_viva():
                        curacion = 30
                        torre.vida = min(
                            torre.vida_max,
                            torre.vida + curacion
                        )
                        sanadas += 1

            return sanadas

        return 0


class Muro:
    TIPOS = {
        "madera": {
            "nombre": "Muro de Madera",
            "resistencia": 60
        },
        "metal": {
            "nombre": "Muro de Metal",
            "resistencia": 150
        }
    }

    def __init__(self, tipo):
        tipo = tipo.lower()

        datos = self.TIPOS[tipo]

        self.tipo = tipo
        self.nombre = datos["nombre"]
        self.resistencia_max = datos["resistencia"]
        self.resistencia = datos["resistencia"]

        self.costo = self.calcular_costo()

    def mostrar(self):
        print("Nombre:", self.nombre)
        print("Resistencia:", self.resistencia, "/", self.resistencia_max)
        print("Costo:", self.costo)

    def esta_en_pie(self):
        return self.resistencia > 0

    def recibir_dano(self, cantidad):
        self.resistencia = max(
            0,
            self.resistencia - cantidad
        )

    def calcular_costo(self):
        return self.resistencia_max // 2