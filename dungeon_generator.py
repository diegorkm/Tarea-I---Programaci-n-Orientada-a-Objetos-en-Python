class Habitacion:
    def __init__(self, id: int, x: int, y: int, inicial: bool, contenido: ContenidoHabitacion | None, conexiones: dict[str, Habitacion], visitado: bool):
        self.id = id
        self.x = x
        self.y = y
        self.inicial = inicial
        self.contenido = contenido
        self.conexiones = conexiones
        self.visitado = visitado

class Mapa: # Implementar metodos
    def __init__(self, ancho: int, alto: int, habitaciones: dict[tuple[int, int], Habitacion], habitacion_inicial: Habitacion):
        self.ancho = ancho
        self.alto = alto
        self.habitaciones = habitaciones

    def generar_estructura(self, n_habitaciones: int):
        pass

    def colocar_contenido(self):
        pass

    def obtener_estadisticas_mapa(self) -> dict[str, int | float]:
        pass

class Objeto:
    def __init__(self, nombre: str, valor: int, descripcion: str):
        self.nombre = nombre
        self.valor = valor
        self.descripcion = descripcion

class Explorador: # Implementar metodos
    def __init__(self, vida: int, inventario: list[Objeto],  posicion_actual: tuple[int, int], mapa: Mapa):
        self.vida = vida
        self.inventario = inventario
        self.posicion_actual = posicion_actual
        self.mapa = mapa

    def mover(self, direccion: str) -> bool:
        pass

    def explorar_habitacion(self) -> str:
        pass

    def obtener_habitaciones_adyacentes(self) -> list[str]:
        pass

    def recibir_dano(self, cantidad: int):
        pass

    def  esta_vivo(self) -> bool:
        pass

#  Crear la clase abstracta ContenidoHabitacion

class Visualizador:
    def __init__(self):
        pass

    def  mostrar_mapa_completo(self):
        pass

    def  mostrar_habitacion_actual(self, explorador: Explorador):
        pass

    def  mostrar_minimapa(self, explorador: Explorador):
        pass

    def  mostrar_estado_explorador(self, explorador: Explorador):
        pass

class Evento:
    pass

