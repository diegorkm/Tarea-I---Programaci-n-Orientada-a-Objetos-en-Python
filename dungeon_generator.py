from __future__ import annotations
from abc import ABC, abstractmethod
import random

class Habitacion:
    def __init__(self, id: int, x: int, y: int, inicial: bool, contenido: ContenidoHabitacion | None, conexiones: dict[str, Habitacion], visitada: bool):
        self.id = id
        self.x = x
        self.y = y
        self.inicial = inicial
        self.contenido = contenido
        self.conexiones = conexiones
        self.visitada = visitada

class Mapa:
    def __init__(self, ancho: int, alto: int, habitaciones: dict[tuple[int, int], Habitacion], habitacion_inicial: Habitacion):
        self.ancho = ancho
        self.alto = alto
        self.habitaciones = habitaciones
        self.habitacion_inicial = habitacion_inicial

    def generar_estructura(self, n_habitaciones: int):
        # Verigicar si es posible crear el mapa
        max_posibles = self.ancho * self.alto
        if n_habitaciones < 1 or n_habitaciones > max_posibles:
            return

        # Limpiar estado
        self.habitaciones = {}

        # Matriz de ocupación (None = libre / Habitacion = ocupada)
        matriz = [[None for _ in range(self.ancho)] for _ in range(self.alto)]

        # Direcciones y su opuesta
        DIRECCIONES = {"norte": (0, -1), "sur": (0, 1), "este": (1, 0), "oeste": (-1, 0)}
        OPUESTA = {"norte": "sur", "sur": "norte", "este": "oeste", "oeste": "este"}

        # Inicio en borde aleatorio
        borde = []
        for x in range(self.ancho):
            borde.append((x, 0))
            borde.append((x, self.alto - 1))
        for y in range(self.alto):
            borde.append((0, y))
            borde.append((self.ancho - 1, y))
        # quitar duplicados de esquinas
        borde = list(set(borde))
        x, y = random.choice(borde)

        h0 = Habitacion(id=1, x=x, y=y, inicial=True, contenido=None, conexiones={}, visitada=False)
        self.habitaciones[(x, y)] = h0
        self.habitacion_inicial = h0
        matriz[y][x] = h0

        # Expansión desde la inicial
        siguiente_id = 2
        frontera = [(x, y)]  # celdas desde donde intentamos expandir

        while len(self.habitaciones) < n_habitaciones and frontera:
            cx, cy = random.choice(frontera)

            dirs = list(DIRECCIONES.items())
            random.shuffle(dirs)

            expando = False
            for nombre_dir, (dx, dy) in dirs:
                nx, ny = cx + dx, cy + dy
                # dentro de los límites del mapa real y libre
                if 0 <= nx < self.ancho and 0 <= ny < self.alto and matriz[ny][nx] is None:
                    nueva = Habitacion(
                        id=siguiente_id, x=nx, y=ny, inicial=False,
                        contenido=None, conexiones={}, visitada=False
                    )
                    self.habitaciones[(nx, ny)] = nueva
                    matriz[ny][nx] = nueva

                    # Conexión bidireccional
                    actual = self.habitaciones[(cx, cy)]
                    actual.conexiones[nombre_dir] = nueva
                    nueva.conexiones[OPUESTA[nombre_dir]] = actual

                    frontera.append((nx, ny))
                    siguiente_id += 1
                    expando = True
                    break

            # Si desde (cx, cy) no se pudo expandir a ningún vecino libre, la retiramos de la frontera
            if not expando:
                try:
                    frontera.remove((cx, cy))
                except ValueError:
                    pass


    def colocar_contenido(self):

        if not self.habitaciones or self.habitacion_inicial is None:
            return

        todas = list(self.habitaciones.values())
        inicial = self.habitacion_inicial

        # Candidatas = todas menos la inicial
        candidatas = []
        for h in todas:
            if h is not inicial:
                candidatas.append(h)
        if len(candidatas) == 0:
            return

        total = len(todas)
        restantes = len(candidatas)

        # Porcentajes simples
        min_m, max_m = int(restantes * 0.20), int(restantes * 0.30)
        if max_m < min_m:
            max_m = min_m
        n_monstruos = random.randint(min_m, max_m)

        min_t, max_t = int(restantes * 0.15), int(restantes * 0.25)
        if max_t < min_t:
            max_t = min_t
        n_tesoros = random.randint(min_t, max_t)

        min_e, max_e = int(total * 0.05), int(total * 0.10)
        if max_e < min_e:
            max_e = min_e
        n_eventos = random.randint(min_e, max_e)

        # Esquinas presentes (distintas de la inicial)
        esquinas_coords = [(0, 0), (0, self.alto - 1), (self.ancho - 1, 0), (self.ancho - 1, self.alto - 1)]
        esquinas_presentes = []
        for c in esquinas_coords:
            if c in self.habitaciones and self.habitaciones[c] is not inicial:
                esquinas_presentes.append(self.habitaciones[c])

        # Al menos 1 jefe en esquina: si no hay otra esquina, usamos la inicial misma
        jefes_en = []
        if len(esquinas_presentes) > 0:
            random.shuffle(esquinas_presentes)
            jefes_en.append(esquinas_presentes[0])
        else:
            jefes_en.append(inicial)

        ocupadas = set((h.x, h.y) for h in jefes_en)

        # Monstruos
        pool_m = []
        for h in candidatas:
            if (h.x, h.y) not in ocupadas:
                pool_m.append(h)
        random.shuffle(pool_m)
        monstruos_en = pool_m[:min(n_monstruos, len(pool_m))]
        for h in monstruos_en:
            ocupadas.add((h.x, h.y))

        # Tesoros
        pool_t = []
        for h in candidatas:
            if (h.x, h.y) not in ocupadas:
                pool_t.append(h)
        random.shuffle(pool_t)
        tesoros_en = pool_t[:min(n_tesoros, len(pool_t))]
        for h in tesoros_en:
            ocupadas.add((h.x, h.y))

        # Eventos
        pool_e = []
        for h in candidatas:
            if (h.x, h.y) not in ocupadas:
                pool_e.append(h)
        random.shuffle(pool_e)
        eventos_en = pool_e[:min(n_eventos, len(pool_e))]
        for h in eventos_en:
            ocupadas.add((h.x, h.y))

        # Distancia Manhattan a la inicial (para valores simples)
        ix, iy = inicial.x, inicial.y

        # Jefe (stats/valor según distancia)
        for h in jefes_en:
            d = abs(h.x - ix) + abs(h.y - iy)
            vida = 10 + d // 2
            ataque = 3 + d // 3
            valor_esp = 25 + d * 2
            h.contenido = Jefe(
                nombre="Jefe",
                vida=vida,
                ataque=ataque,
                recompensa_especial=Objeto(nombre="Reliquia", valor=valor_esp, descripcion="Tesoro especial")
            )

        # Monstruos
        for h in monstruos_en:
            d = abs(h.x - ix) + abs(h.y - iy)
            vida = 5 + d // 3
            ataque = 1 + d // 4
            nombres = ["Ese tal calculo", "Prueba de estadistica", "Juan"]
            h.contenido = Monstruo(nombre=random.choice(nombres), vida=vida, ataque=ataque)

        # Tesoros
        for h in tesoros_en:
            d = abs(h.x - ix) + abs(h.y - iy)
            valor = 10 + d * 2
            h.contenido = Tesoro(recompensa=Objeto(nombre="Cofre", valor=valor, descripcion="Licencia medica"))

        # Eventos (texto simple)
        eventos_catalogo = [
            ("Bendición", "Recuperas vida.", "curar"),
            ("Trampa", "Recibes daño.", "dano"),
            ("Portal", "Te teletransportas.", "teleport"),
            ("Furia", "Bonus temporal en combate.", "buff"),
        ]
        for h in eventos_en:
            nombre, desc, efecto = random.choice(eventos_catalogo)
            h.contenido = Evento(nombre=nombre, descripcion=desc, efecto=efecto)

        # La inicial queda vacia si no la usamos para jefe
        if all(h is not inicial for h in jefes_en):
            inicial.contenido = None

    def obtener_estadisticas_mapa(self) -> dict[str, int | float]:
        if not self.habitaciones:
            return {
                "total_habitaciones": 0,
                "inicial": 0,
                "vacias": 0,
                "tesoros": 0,
                "monstruos": 0,
                "jefes": 0,
                "eventos": 0,
                "promedio_conexiones": 0.0,
            }

        total = len(self.habitaciones)
        iniciales = 0
        vacias = 0
        tesoros = 0
        monstruos = 0
        jefes = 0
        eventos = 0
        suma_conexiones = 0

        for h in self.habitaciones.values():
            suma_conexiones += len(h.conexiones)
            if h.inicial:
                iniciales += 1
            c = h.contenido
            if c is None:
                if not h.inicial:
                    vacias += 1
            else:
                if isinstance(c, Tesoro):
                    tesoros += 1
                elif isinstance(c, Jefe):
                    jefes += 1
                elif isinstance(c, Monstruo):
                    monstruos += 1
                elif isinstance(c, Evento):
                    eventos += 1

        return {
            "total_habitaciones": total,
            "inicial": iniciales,
            "vacias": vacias,
            "tesoros": tesoros,
            "monstruos": monstruos,
            "jefes": jefes,
            "eventos": eventos,
            "promedio_conexiones": round(suma_conexiones / float(total), 3),
        }


class Objeto:
    def __init__(self, nombre: str, valor: int, descripcion: str):
        self.nombre = nombre
        self.valor = valor
        self.descripcion = descripcion

class Explorador:
    def __init__(self, vida: int, inventario: list[Objeto],  posicion_actual: tuple[int, int], mapa: Mapa):
        self.vida = 5
        self.inventario = inventario
        self.posicion_actual = posicion_actual  # (x, y)
        self.mapa = mapa

    def mover(self, direccion: str) -> bool:
        #Se mueve a una habitación conectada (norte/sur/este/oeste). Enfocado en navegación del mapa.
        d = direccion.lower().strip()
        actual = self.mapa.habitaciones.get(self.posicion_actual)
        if actual is None:
            return False
        destino = actual.conexiones.get(d)
        if destino is None:
            return False
        self.posicion_actual = (destino.x, destino.y)
        return True

    def explorar_habitacion(self) -> str:
        #Marca la habitación actual como visitada y devuelve una descripción del contenido.
        actual = self.mapa.habitaciones.get(self.posicion_actual)
        if actual is None:
            return "No estás en una habitación válida."

        actual.visitada = True
        if actual.contenido is None:
            return "La habitación está vacía."

        # Acceso directo a las propiedades/método del contenido
        tipo = actual.contenido.tipo # tipo puede ser monstruo, tesoro etc
        desc = actual.contenido.descripcion
        extra = actual.contenido.interactuar()

        msg = f"Te encuentras con un {tipo}."
        if desc:
            msg += f" {desc}"
        if isinstance(extra, str) and extra:
            msg += f"\n{extra}"
        return msg


    def obtener_habitaciones_adyacentes(self) -> list[str]:
        #Lista de direcciones disponibles desde la habitación actual.
        actual = self.mapa.habitaciones.get(self.posicion_actual)
        if actual is None:
            return []
        return list(actual.conexiones.keys())

    def recibir_dano(self, cantidad: int):
        if cantidad < 0:
            cantidad = 0
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

    @property
    def esta_vivo(self) -> bool:
        return self.vida > 0


class ContenidoHabitacion(ABC):
    @property
    @abstractmethod
    def descripcion(self) -> str:
        # Valor por defecto
        return "Contenido de habitación"

    @property
    @abstractmethod
    def tipo(self) -> str:
        # Valor por defecto
        return "contenido"

    @abstractmethod
    def interactuar(self) -> str:
        # Como me enfoque en la generacion del mapa solo lo dejo asi
        return "Interacción descriptiva."


class Tesoro(ContenidoHabitacion):
    def __init__(self, recompensa: Objeto):
        self.recompensa = recompensa

    @property
    def descripcion(self) -> str:
        return f"Tesoro: {self.recompensa.nombre} (valor {self.recompensa.valor})"

    @property
    def tipo(self) -> str:
        return "tesoro"

    def interactuar(self) -> str:
        # Solo informa, por lo mismo de denante, me enfoque en la generacion del mapa
        return "Hay un tesoro aquí."


class Monstruo(ContenidoHabitacion):
    def __init__(self, nombre: str, vida: int, ataque: int):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque

    @property
    def descripcion(self) -> str:
        return f"{self.nombre} (vida {self.vida}, ataque {self.ataque})"

    @property
    def tipo(self) -> str:
        return "monstruo"

    def interactuar(self) -> str:
        return "Un monstruo esta presente en esta habitación."

class Jefe(Monstruo):
    def __init__(self, nombre: str, vida: int, ataque: int, recompensa_especial: Objeto):
        super().__init__(nombre, vida, ataque)
        self.recompensa_especial = recompensa_especial

    @property
    def tipo(self) -> str:
        return "jefe"

    def interactuar(self) -> str:
        return "Un jefe cuida esta habitación"

class Evento(ContenidoHabitacion):
    def __init__(self, nombre: str, descripcion: str, efecto):
        self.nombre = nombre
        self._descripcion = descripcion
        self.efecto = efecto  # 'curar', 'dano', 'teleport', 'buff'

    @property
    def descripcion(self) -> str:
        return f"Evento: {self.nombre}. {self._descripcion}"

    @property
    def tipo(self) -> str:
        return "evento"

    def interactuar(self) -> str:
        # Solo texto, realmente no modifica el estado por lo mismo de mas atras
        return f"Ocurre un evento: {self.nombre}."


class Visualizador:
    def __init__(self):
        pass

    def mostrar_mapa_completo(self) -> None:
        pass

    def mostrar_habitacion_actual(self, explorador: Explorador) -> None:
        pass

    def mostrar_minimapa(self, explorador: Explorador) -> None:
        pass

    def mostrar_estado_explorador(self, explorador: Explorador) -> None:
        pass