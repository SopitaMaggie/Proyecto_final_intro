class Torre:
    TIPOS = {
        "olimpo": {
            "nombre": "Torre del Olimpo",
            "costo": 150,
            "vida": 120,
            "dano": 25,
            "alcance": 3,
            "turnos_habilidad": 3
        },
        "oscura": {
            "nombre": "Torre Oscura",
            "costo": 70,
            "vida": 80,
            "dano": 10,
            "alcance": 2,
            "turnos_habilidad": 2
        },
        "volcan": {
            "nombre": "Torre del Volcán",
            "costo": 200,
            "vida": 180,
            "dano": 35,
            "alcance": 4,
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
        self.costo = datos["costo"]
        self.vida_max = datos["vida"]
        self.vida = datos["vida"]
        self.dano = datos["dano"]
        self.alcance = datos["alcance"]
        self.turnos_habilidad = datos["turnos_habilidad"]
        self.contador_habilidad = 0
        self.congelada = 0        # turnos restantes congelada
        self.debilitada = False   # efecto del Ninja

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
        if self.tipo == "olimpo": # Rayos
            dano_total = self.dano * 2
            objetivo_o_lista.recibir_dano(dano_total)
            return dano_total
        elif self.tipo == "oscura": # Neblina
            objetivo_o_lista.recibir_dano(self.dano)
            objetivo_o_lista.envenenada = 1  # solo ese turno
            return self.dano
        elif self.tipo == "volcan": # Sana torre cercana
            sanadas = 0
            if isinstance(objetivo_o_lista, list):
                for torre in objetivo_o_lista:
                    if torre is not self and torre.esta_viva():
                        curacion = 30
                        torre.vida = min(torre.vida_max, torre.vida + curacion)
                        sanadas += 1
            return sanadas
        return 0



class Muro:
    TIPOS = {
        "madera": {
            "nombre": "Muro de Madera",
            "costo": 30,
            "resistencia": 60
        },
        "metal": {
            "nombre": "Muro de Metal",
            "costo": 80,
            "resistencia": 150
        }
    }

    def __init__(self, tipo):
        tipo = tipo.lower()
        if tipo not in self.TIPOS:
            raise ValueError(f"Tipo de muro inválido: {tipo}")
        datos = self.TIPOS[tipo]
        self.tipo = tipo
        self.nombre = datos["nombre"]
        self.costo = datos["costo"]
        self.resistencia_max = datos["resistencia"]
        self.resistencia = datos["resistencia"]

    def mostrar(self):
        print("Nombre:", self.nombre)
        print("Resistencia:", self.resistencia, "/", self.resistencia_max)
        print("Costo:", self.costo)

    def esta_en_pie(self):
        return self.resistencia > 0

    def recibir_dano(self, cantidad):
        self.resistencia = max(0, self.resistencia - cantidad)

