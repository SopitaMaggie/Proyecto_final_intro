class Unidad:
    TIPOS = {
        "flechas": {
            "nombre": "Flechas",
            "costo": 40,
            "vida": 50,
            "dano": 10,
            "velocidad": 2,
            "turnos_habilidad": 3
        },
        "ninja": {
            "nombre": "Ninja",
            "costo": 90,
            "vida": 80,
            "dano": 20,
            "velocidad": 3,
            "turnos_habilidad": 3
        },
        "reina_hielo": {
            "nombre": "Reina del Hielo",
            "costo": 120,
            "vida": 100,
            "dano": 28,
            "velocidad": 2,
            "turnos_habilidad": 4
        },
        "rey_barbaro": {
            "nombre": "Rey Bárbaro",
            "costo": 160,
            "vida": 200,
            "dano": 40,
            "velocidad": 1,
            "turnos_habilidad": 4
        },
        "fireball": {
            "nombre": "Fireball",
            "costo": 170,
            "vida": 120,
            "dano": 45,
            "velocidad": 1,
            "turnos_habilidad": 4
        }
    }

    def __init__(self, tipo):
        tipo = tipo.lower()
        if tipo not in self.TIPOS:
            raise ValueError(f"Tipo de unidad inválido: {tipo}")
        datos = self.TIPOS[tipo]
        self.tipo = tipo
        self.nombre = datos["nombre"]
        self.costo = datos["costo"]
        self.vida_max = datos["vida"]
        self.vida = datos["vida"] #Baja cuando recibe daño
        self.dano = datos["dano"] #Daño
        self.velocidad = datos["velocidad"]
        self.turnos_habilidad = datos["turnos_habilidad"]
        self.contador_habilidad = 0
        self.escudo_activo = 0    # turnos restantes con escudo (Rey Bárbaro)
        self.envenenada = 0       # turnos restantes de veneno (Torre Oscura)

    def esta_viva(self):
        return self.vida > 0

    def recibir_dano(self, cantidad): # Rey Barbaro
        if self.escudo_activo > 0:
            cantidad = cantidad // 2
            self.escudo_activo -= 1
        self.vida = max(0, self.vida - cantidad)

    def aplicar_veneno(self, dano_veneno=5): # Torre oscura
        if self.envenenada > 0:
            self.vida = max(0, self.vida - dano_veneno)
            self.envenenada -= 1

    def mostrar(self):
        print("Nombre:", self.nombre)
        print("Vida:", self.vida, "/", self.vida_max)
        print("Daño:", self.dano)
        print("Velocidad:", self.velocidad)
        print("Costo:", self.costo)

    def atacar(self, objetivo):
        self.contador_habilidad += 1
        if self.contador_habilidad >= self.turnos_habilidad:
            self.contador_habilidad = 0
            return self.usar_habilidad(objetivo)
        return self._ataque_normal(objetivo)

    def _ataque_normal(self, objetivo):
        if self.tipo == "flechas": # 3 flechas, daño bajo
            objetivo.recibir_dano(self.dano)
            return self.dano
        elif self.tipo == "ninja":
            objetivo.recibir_dano(self.dano)
            if hasattr(objetivo, "debilitada"):
                objetivo.debilitada = True
            return self.dano
        elif self.tipo == "reina_hielo": # Bola de hielo, daño medio-alto
            objetivo.recibir_dano(self.dano)
            return self.dano
        elif self.tipo == "rey_barbaro": # Hacha, daño alto
            objetivo.recibir_dano(self.dano)
            return self.dano
        elif self.tipo == "fireball": # Roca de fuego, daño alto
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
            if hasattr(objetivo_o_lista, "congelada"): # Hasattr: Verifica si se tiene  un atributo(debilidad)
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

