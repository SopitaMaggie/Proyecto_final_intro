class Unidad: #    # Diccionario con los tipos de unidades disponibles y su info
    TIPOS = {
        "flechas": {
            "nombre": "Flechas",
            "costo": 40,
            "vida": 50,
            "dano": 10,
            "velocidad": 2,
            "habilidad": "Lluvia de flechas (doble daño)",
            "turnos_habilidad": 3
        },
        "ninja": {
            "nombre": "Ninja",
            "costo": 90,
            "vida": 80,
            "dano": 20,
            "velocidad": 3,
            "habilidad": "Ataque crítico (1.8x daño)",
            "turnos_habilidad": 3
        },
        "reina_hielo": {
            "nombre": "Reina del Hielo",
            "costo": 120,
            "vida": 100,
            "dano": 28,
            "velocidad": 2,
            "habilidad": "Congela torres por 3 turnos",
            "turnos_habilidad": 4
        },
        "rey_barbaro": {
            "nombre": "Rey Bárbaro",
            "costo": 160,
            "vida": 200,
            "dano": 40,
            "velocidad": 1,
            "habilidad": "Escudo que reduce el daño recibido",
            "turnos_habilidad": 4
        },
        "fireball": {
            "nombre": "Fireball",
            "costo": 100,
            "vida": 120,
            "dano": 45,
            "velocidad": 1,
            "habilidad": "Ataque de área",
            "turnos_habilidad": 4
        }
    }

    def __init__(self, tipo): # pone una unidad según el tipo seleccionado con su info
        tipo = tipo.lower()

        if tipo not in self.TIPOS:
            raise ValueError(f"Tipo de unidad inválido: {tipo}")

        datos = self.TIPOS[tipo]

        self.tipo = tipo
        self.nombre = datos["nombre"]
        self.costo = datos["costo"]
        self.vida_max = datos["vida"]
        self.vida = datos["vida"]
        self.dano = datos["dano"] # daño
        self.velocidad = datos["velocidad"]
        self.habilidad = datos["habilidad"]
        self.turnos_habilidad = datos["turnos_habilidad"]
        self.contador_habilidad = 0 # para saber cuando usar la habilidad
        self.escudo_activo = 0
        self.envenenada = 0

    def esta_viva(self):
        return self.vida > 0
    def recibir_dano(self, cantidad):
        # Reduce la vida de la unidad.
        if self.escudo_activo > 0:
            cantidad = cantidad // 2
            self.escudo_activo -= 1

        self.vida = max(0, self.vida - cantidad)
    def aplicar_veneno(self, dano_veneno=5): #Aplica daño por veneno si la unidad está envenenada.
        if self.envenenada > 0:
            self.vida = max(0, self.vida - dano_veneno)
            self.envenenada -= 1

    def mostrar(self):
        print("Nombre:", self.nombre)
        print("Vida:", self.vida, "/", self.vida_max)
        print("Daño:", self.dano)
        print("Velocidad:", self.velocidad)
        print("Costo:", self.costo)
        print("Habilidad:", self.habilidad)
        print("Turnos para habilidad:", self.turnos_habilidad)
    def atacar(self, objetivo):

        self.contador_habilidad += 1

        if self.contador_habilidad >= self.turnos_habilidad:
            self.contador_habilidad = 0
            return self.usar_habilidad(objetivo)
        return self._ataque_normal(objetivo)

    def _ataque_normal(self, objetivo):
        # Ejecuta el ataque normal según el tipo de unidad.
        if self.tipo == "flechas":
            objetivo.recibir_dano(self.dano)
            return self.dano
        elif self.tipo == "ninja":
            objetivo.recibir_dano(self.dano)

            if hasattr(objetivo, "debilitada"): # Hasattr: Verifica si se tiene  un atributo(debilidad)
                objetivo.debilitada = True
            return self.dano
        elif self.tipo == "reina_hielo":
            objetivo.recibir_dano(self.dano)
            return self.dano
        elif self.tipo == "rey_barbaro":
            objetivo.recibir_dano(self.dano)
            return self.dano
        elif self.tipo == "fireball":
            objetivo.recibir_dano(self.dano)
            return self.dano
        return 0
    def usar_habilidad(self, objetivo_o_lista):
        if self.tipo == "flechas":
            dano_total = self.dano * 2
            objetivo_o_lista.recibir_dano(dano_total)
            return dano_total
        elif self.tipo == "ninja":
            dano_total = int(self.dano * 1.8)
            objetivo_o_lista.recibir_dano(dano_total)
            return dano_total
        elif self.tipo == "reina_hielo":
            objetivo_o_lista.recibir_dano(self.dano)
            if hasattr(objetivo_o_lista, "congelada"):
                objetivo_o_lista.congelada = 3
            return self.dano
        elif self.tipo == "rey_barbaro":
            self.escudo_activo = 2
            objetivo_o_lista.recibir_dano(self.dano)
            return self.dano
        elif self.tipo == "fireball":
            dano_total = 0
            if isinstance(objetivo_o_lista, list):
                for objetivo in objetivo_o_lista:
                    if hasattr(objetivo, "recibir_dano"):
                        objetivo.recibir_dano(self.dano)
                        dano_total += self.dano
            else:
                objetivo_o_lista.recibir_dano(self.dano)
                dano_total = self.dano
            return dano_total
        return 0