from __future__ import annotations
from abc import ABC, abstractmethod
import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import json

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

        # Intentar orillar jefes para que no aparezcan en el inicio
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
    def __init__(self, mapa: Mapa):
        self.mapa = mapa
        self.console = Console()

    # Representación visual del mapa completo con colores
    def mostrar_mapa_completo(self) -> None:
        """
          S = inicio
          B = jefe
          M = monstruo
          T = tesoro
          E = evento
          · = vacío
        """
        t = Table(show_header=False, box=None, pad_edge=False)
        # Columnas = ancho del mapa
        for _ in range(self.mapa.ancho):
            t.add_column(justify="center", no_wrap=True)

        for y in range(self.mapa.alto):
            fila_render = []
            for x in range(self.mapa.ancho):
                h = self.mapa.habitaciones.get((x, y))
                if h is None:
                    fila_render.append(Text(" ", style="dim"))
                    continue

                if h.inicial:
                    fila_render.append(Text("S", style="bold green"))
                elif h.contenido is None:
                    fila_render.append(Text("·", style="dim"))
                else:
                    tipo = h.contenido.tipo
                    if tipo == "jefe":
                        fila_render.append(Text("B", style="bold red"))
                    elif tipo == "monstruo":
                        fila_render.append(Text("M", style="yellow"))
                    elif tipo == "tesoro":
                        fila_render.append(Text("T", style="bright_cyan"))
                    elif tipo == "evento":
                        fila_render.append(Text("E", style="magenta"))
                    else:
                        fila_render.append(Text("·", style="dim"))
            t.add_row(*fila_render)

        self.console.print(Panel(t, title="Mapa completo", border_style="cyan"))

    # Descripción detallada de la habitación actual del explorador
    def mostrar_habitacion_actual(self, explorador: Explorador) -> None:
        """
        Muestra información de la habitación actual
          - coordenadas
          - conexiones disponibles
          - descripción del contenido
        """
        actual = self.mapa.habitaciones.get(explorador.posicion_actual)
        if actual is None:
            self.console.print(Panel("No estás en una habitación válida.", border_style="red"))
            return

        direcciones = ", ".join(actual.conexiones.keys()) or "Sin conexiones"
        if actual.contenido is None:
            contenido_txt = "Vacía"
        else:
            contenido_txt = f"{actual.contenido.tipo}: {actual.contenido.descripcion}"

        body = Text()
        body.append(f"Posición: ({actual.x}, {actual.y})\n", style="bold")
        body.append(f"Conexiones: {direcciones}\n")
        body.append(f"Contenido: {contenido_txt}")

        titulo = "Habitación de inicio" if actual.inicial else "Habitación actual"
        self.console.print(Panel(body, title=titulo, border_style="green"))

    # Minimapa: solo habitaciones visitadas (con símbolos/colores) y posición
    def mostrar_minimapa(self, explorador: Explorador) -> None:
        """
        Muestra únicamente las habitaciones visitadas, más la posición actual.
        Símbolos:
          @ = posición actual
          * = visitada (no actual)
          S = inicio (si visitada)
          (vacío) = no visitada / no existe
        """
        t = Table(show_header=False, box=None, pad_edge=False)
        for _ in range(self.mapa.ancho):
            t.add_column(justify="center", no_wrap=True)

        pos_actual = explorador.posicion_actual
        for y in range(self.mapa.alto):
            fila = []
            for x in range(self.mapa.ancho):
                h = self.mapa.habitaciones.get((x, y))
                if h is None:
                    fila.append(Text(" ", style="dim"))
                    continue
                if (x, y) == pos_actual:
                    fila.append(Text("@", style="bold white on blue"))
                elif h.inicial and h.visitada:
                    fila.append(Text("S", style="bold green"))
                elif h.visitada:
                    fila.append(Text("*", style="bright_black"))
                else:
                    fila.append(Text(" ", style="dim"))
            t.add_row(*fila)

        self.console.print(Panel(t, title="Minimapa (visitadas)", border_style="magenta"))

    # Estado del explorador: vida, inventario y estadísticas
    def mostrar_estado_explorador(self, explorador: Explorador) -> None:
        """
        Muestra:
          - Vida
          - Posición actual
          - Inventario (nombre y valor)
          - Estadísticas básicas (habitaciones visitadas / total)
        """
        total = len(self.mapa.habitaciones)
        visitadas = sum(1 for h in self.mapa.habitaciones.values() if h.visitada)

        inv_lines = []
        if explorador.inventario:
            for obj in explorador.inventario:
                inv_lines.append(f"• {obj.nombre} (valor {obj.valor})")
        else:
            inv_lines.append("— (vacío)")

        body = Text()
        body.append(f"Vida: {explorador.vida}\n", style="bold red")
        body.append(f"Posición: {explorador.posicion_actual}\n")
        body.append(f"Visitadas: {visitadas}/{total}\n")
        body.append("Inventario:\n", style="bold")
        body.append("\n".join(inv_lines))

        self.console.print(Panel(body, title="Estado del explorador", border_style="yellow"))


def guardar_partida(mapa: Mapa, explorador: Explorador, archivo: str) -> None:
    def _dump_contenido(h: Habitacion):
        c = h.contenido
        if c is None:
            return None
        # Tesoro
        if isinstance(c, Tesoro):
            return {
                "tipo": "tesoro",
                "recompensa": {
                    "nombre": c.recompensa.nombre,
                    "valor": c.recompensa.valor,
                    "descripcion": c.recompensa.descripcion,
                },
            }
        # Jefe (subclase de Monstruo)
        if isinstance(c, Jefe):
            return {
                "tipo": "jefe",
                "nombre": c.nombre,
                "vida": c.vida,
                "ataque": c.ataque,
                "recompensa_especial": {
                    "nombre": c.recompensa_especial.nombre,
                    "valor": c.recompensa_especial.valor,
                    "descripcion": c.recompensa_especial.descripcion,
                },
            }
        # Monstruo
        if isinstance(c, Monstruo):
            return {"tipo": "monstruo", "nombre": c.nombre, "vida": c.vida, "ataque": c.ataque}
        # Evento (tu clase guarda el texto base en _descripcion)
        if isinstance(c, Evento):
            base_desc = getattr(c, "_descripcion", "")
            return {"tipo": "evento", "nombre": c.nombre, "descripcion": base_desc, "efecto": c.efecto}
        # Desconocido
        return None

    data = {
        "mapa": {
            "ancho": mapa.ancho,
            "alto": mapa.alto,
            "habitacion_inicial": [mapa.habitacion_inicial.x, mapa.habitacion_inicial.y] if mapa.habitacion_inicial else None,
            # Guardamos cada habitación y sus conexiones referenciadas por coordenadas (reconstruibles)
            "habitaciones": [
                {
                    "id": h.id,
                    "x": h.x,
                    "y": h.y,
                    "inicial": h.inicial,
                    "visitada": h.visitada,
                    "contenido": _dump_contenido(h),
                    "conexiones": {d: [dest.x, dest.y] for d, dest in h.conexiones.items()},
                }
                for (x, y), h in mapa.habitaciones.items()
            ],
        },
        "explorador": {
            "vida": explorador.vida,
            "posicion_actual": list(explorador.posicion_actual),
            "inventario": [
                {"nombre": o.nombre, "valor": o.valor, "descripcion": o.descripcion}
                for o in explorador.inventario
            ],
        },
    }

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def cargar_partida(archivo: str) -> tuple[Mapa, Explorador]:
    with open(archivo, "r", encoding="utf-8") as f:
        data = json.load(f)

    m = data["mapa"]
    ancho, alto = int(m["ancho"]), int(m["alto"])

    # 1) Crear habitaciones sin conexiones/contenido
    habitaciones: dict[tuple[int, int], Habitacion] = {}
    for h in m["habitaciones"]:
        hab = Habitacion(
            id=int(h["id"]),
            x=int(h["x"]),
            y=int(h["y"]),
            inicial=bool(h["inicial"]),
            contenido=None,
            conexiones={},
            visitada=bool(h["visitada"]),
        )
        habitaciones[(hab.x, hab.y)] = hab

    # 2) Reconstruir contenido
    for h in m["habitaciones"]:
        hab = habitaciones[(int(h["x"]), int(h["y"]))]
        c = h.get("contenido")
        if not c:
            hab.contenido = None
            continue
        t = c.get("tipo")
        if t == "tesoro":
            r = c["recompensa"]
            hab.contenido = Tesoro(Objeto(r["nombre"], int(r["valor"]), r["descripcion"]))
        elif t == "monstruo":
            hab.contenido = Monstruo(c["nombre"], int(c["vida"]), int(c["ataque"]))
        elif t == "jefe":
            esp = c["recompensa_especial"]
            hab.contenido = Jefe(
                c["nombre"], int(c["vida"]), int(c["ataque"]),
                Objeto(esp["nombre"], int(esp["valor"]), esp["descripcion"])
            )
        elif t == "evento":
            # usamos la descripción base guardada
            hab.contenido = Evento(c["nombre"], c.get("descripcion", ""), c.get("efecto"))
        else:
            hab.contenido = None

    # 3) Reconstruir conexiones bidireccionales
    OPUESTA = {"norte": "sur", "sur": "norte", "este": "oeste", "oeste": "este"}
    for h in m["habitaciones"]:
        a = habitaciones[(int(h["x"]), int(h["y"]))]
        for dirn, coords in h.get("conexiones", {}).items():
            bx, by = int(coords[0]), int(coords[1])
            b = habitaciones.get((bx, by))
            if not b:
                continue
            a.conexiones.setdefault(dirn, b)
            opp = OPUESTA.get(dirn)
            if opp:
                b.conexiones.setdefault(opp, a)

    # 4) Habitacion inicial y creación del mapa
    hi = m.get("habitacion_inicial")

    if hi is None:
        # forzar inicial
        hab_ini = next(iter(habitaciones.values()))
    else:
        hab_ini = habitaciones[tuple(hi)]

    mapa = Mapa(ancho=ancho, alto=alto, habitaciones=habitaciones, habitacion_inicial=hab_ini)

    # 5) Reconstruir explorador
    ex = data["explorador"]
    inventario = [Objeto(o["nombre"], int(o["valor"]), o["descripcion"]) for o in ex.get("inventario", [])]
    explorador = Explorador(
        vida=int(ex["vida"]),
        inventario=inventario,
        posicion_actual=tuple(ex["posicion_actual"]),
        mapa=mapa,
    )

    return mapa, explorador