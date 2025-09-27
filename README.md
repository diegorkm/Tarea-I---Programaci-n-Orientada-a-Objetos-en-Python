////Instrucciones básicas para ejecutar el código\\\\

Descargar archivos del repositorio, poner todos en la misma carpeta y ejecutar main.py


////Descripción breve del diseño e implementación\\\\

Habitación: identificada por id, permite indicar si una habitación es inicial, guardar contenido, 
ver conexiones y verificar si la habitación fue visitada.

Mapa: genera la estructura de las habitaciones con conexiones válidas. 
También distribuye monstruos, tesoros y objetos, además de devolver un resúmen del mapa.

Objeto: Es la representación de los items, con mombre, valor y descripción

Explorador: con vida por defecto de 5, tiene el inventario, posición actual, y su referencia del mapa. 
También permite saber si el jugador se puede mover o no de una habitación a otra, además de permitir
la exploración y ser capaz de recibir daño.

---ContenidoHabitacion---

Es una clase abstracta que permite los contenidos en habitaciones, los cuales se ven en:
-Tesoro
-Monstruo
-Jefe
-Evento

---Visualizador---

Utiliza la librería rich para mostrar el mapa completo, sinceramente no sabía usar la librería, así que fue una de las partes que más apoyo he requerido
de fuentes externas tales como IA.

---Guardado y Cargado de partidas---

Son funciones las cuales sirven para guardar y cargar la partida.
Al intentar implementarlo aparecían demasiados problemas, por lo cual de igual manera que en Visualizador he requerido apoyo
de fuentes externas como IA.

Guarda y Carga habitaciones visitadas, mapa, vida, inventario y posición.

---Main.py---

Permite la utilización de todo lo creado en dungeon_generator.py, con un menú interactivo que permite el movimiento, la exploración,
el guardado y cargado de partidas y finalizar el programa.


////Cumplimiento Requerimientos\\\\

|-----------------------------------------------------------------|
| # |      Requerimiento     |     Estado    |    Observación     |
|-----------------------------------------------------------------|
| 1 | Clase habitación con   |    Cumplido   | ****************** |
|   | atributos solicitados  |               | ****************** |
|-----------------------------------------------------------------|
|   | Clase Mapa con generar |               | ****************** |
| 2 | estructura y colocar   |    Cumplido   | ****************** |
|   | contenido              |               | ****************** |
|-----------------------------------------------------------------|
|   | Clase Objeto con       |               | ****************** |
| 3 | nombre, valor y        |    Cumplido   | ****************** |
|   | descripción            |               | ****************** |
|-----------------------------------------------------------------|
|   | Clase explorador con   |               | Al centrarme solo  |
| 4 | vida 5, inventario,    |    Parcial    | en generar mapa no |
|   | posición y métodos     |               | altera combate ni  |
|   |                        |               | inventario         |
|-----------------------------------------------------------------|
|   | Clase abstracta        |               | Implementado, pero |
| 5 | ContenidoHabitacion y  |    Parcial    | interactuar() solo |
|   | subclases              |               | da mensaje         |
|-----------------------------------------------------------------|
|   | Distribución de        |               | ****************** |
| 6 | contenido en           |    Cumplido   | ****************** |
|   | colocar_contenido      |               | ****************** |
|-----------------------------------------------------------------|
|   | Método                 |               | ****************** |
| 7 | obtener_estadisticas_  |    Cumplido   | ****************** |
|   | mapa                   |               | ****************** |
|-----------------------------------------------------------------|
| 8 | Guardar y cargar       |    Cumplido   | ****************** |
|   | partida en JSON        |               | ****************** |
|-----------------------------------------------------------------|
| 9 | Clase visualizador con |    Cumplido   | ****************** |
|   | rich                   |               | ****************** |
|-----------------------------------------------------------------|
|   | Sistema de eventos     |               | Eventos creados,   |
| 10| aleatorios             |    Parcial    | no modifican nada, |
|   |                        |               | solo da texto      |
|-----------------------------------------------------------------|
| 11| Dificultad escalable   |    Cumplido   | ****************** |
|   | con distancia Manhattan|               | ****************** |
|-----------------------------------------------------------------|


////Observaciones finales (Resumen)\\\\

- Se cumple con la mayor parte de los requerimientos solicitados.
- No se aplican realmente efectos en inventario ni en la vida, solo se informa de los objetos y efectos.
- Se requirió ayuda de otras fuentes como compañerismo y IA para realizar algunas cosas tales como la utilización de librería rich y 
guardado y cargado de partida.