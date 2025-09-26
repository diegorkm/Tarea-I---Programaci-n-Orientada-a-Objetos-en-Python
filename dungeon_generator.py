from __future__ import annotations
from abc import ABC, abstractmethod


class Habitacion:
    def __init__(self, id: int, x: int, y: int, inicial: bool, contenido: ContenidoHabitacion | None, conexiones: dict[str, Habitacion], visitada: bool):
        self.id = id
        self.x = x
        self.y = y
        self.inicial = inicial
        self.contenido = contenido
        self.conexiones = conexiones
        self.visitada = visitada

class Mapa: # Implementar metodos
    def __init__(self, ancho: int, alto: int, habitaciones: dict[tuple[int, int], Habitacion], habitacion_inicial: Habitacion):
        self.ancho = ancho
        self.alto = alto
        self.habitaciones = habitaciones
        self.habitacion_inicial = habitacion_inicial

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

    @property
    def esta_vivo(self) -> bool:
        pass

class ContenidoHabitacion(ABC):
    @property
    @abstractmethod
    def descripcion(self) -> str:
        pass

    @property
    @abstractmethod
    def tipo(self) -> str:
        pass

    @abstractmethod
    def interactuar() -> str:
        pass

class Tesoro(ContenidoHabitacion):
    def __init__(self, recompensa: Objeto):
        self.recompensa = recompensa
        
    @property
    def descripcion(self) -> str:
        pass

    @property
    def tipo(self) -> str:
        pass

    def interactuar() -> str:
        pass

class Monstruo(ContenidoHabitacion):
    def __init__(self, nombre: str, vida: int, ataque: int):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque

    @property
    def descripcion(self) -> str:
        pass

    @property
    def tipo(self) -> str:
        pass


    def interactuar() -> str:
        pass

class Jefe(Monstruo):
    def __init__(self, nombre: str, vida: int, ataque: int, recompensa_especial: Objeto):
        super().__init__(nombre, vida, ataque)
        self.recompensa_especial = recompensa_especial

    @property
    def tipo(self) -> str:
        pass

    def interactuar() -> str:
        pass

class Evento(ContenidoHabitacion):
    def __init__(self, nombre: str, descripcion: str, efecto):
        self.nombre = nombre
        self._descripcion = descripcion
        self.efecto = efecto

    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    @property
    def tipo(self) -> str:
        pass
    
    def interactuar() -> str:
        pass

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



