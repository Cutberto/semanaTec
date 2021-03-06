"""
    Pacman, classic arcade game.
    Exercises

    1. Change the board. -- Done
    2. Change the number of ghosts. -- Done
    3. Change where pacman starts. -- Done
    4. Make the ghosts faster/slower. -- Done
    5. Make the ghosts smarter. -- Done
"""

from random import choice
from turtle import Turtle, bgcolor, done, onkey, listen, tracer, hideturtle
from turtle import setup, clear, up, goto, dot, update, ontimer

from freegames import floor, vector


state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(0, 0)
pacman = vector(0, 0)  # Posición base de Pacman
# Se definen todos los fantasmas, con vectores Posicion X,Y
# un segundo vector para definir el movimiento y
# un tercero para definir el color
ghosts = [
    [vector(-180, 160), vector(5, 0), 'pink'],
    [vector(-180, -160), vector(0, 5), 'red'],
    [vector(100, 160), vector(0, -5), 'green'],
    [vector(100, -160), vector(-5, 0), 'purple'],
    [vector(-180, 0), vector(5, 0), 'blue'],
    [vector(100, 0), vector(5, 0), 'white']
]
# fmt: off
# Definimos todo el tablero, 0 para pared 1 para corredor
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on


def square(x, y):
    """Draw square using path at (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


# Ajuste para imprimir en pantalla matriz "tiles"
def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """
        Return True if point is valid in tiles.
        @point is a X and Y position vector
    """
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Draw world using path."""
    bgcolor('black')  # Color de Fondo
    path.color('gray')  # Color de Pasillos

    for index in range(len(tiles)):
        tile = tiles[index]
        #  Dibuja los pasillos
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            # Dibuja los puntos Dorados
            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(3, 'yellow')


def move():
    """Move pacman and all ghosts."""
    writer.undo()
    writer.write(state['score'])

    clear()
    onkey(lambda: change(10, 0), 'Right')
    onkey(lambda: change(-10, 0), 'Left')
    onkey(lambda: change(0, 10), 'Up')
    onkey(lambda: change(0, -10), 'Down')
    # Chequeo de movimiento de Pacman
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    # Come el Punto Amarillo y aumenta el Marcador
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')  # Dibuja a Pacman

    # Proceso para dibujar y mover a los fantasmas
    for point, course, color in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            # Vector de velocidades para fantasmas
            options = [
                vector(10, 0),
                vector(-10, 0),
                vector(0, 10),
                vector(0, -10),
            ]
            # Revisar posicion de pacman
            difx = pacman.x - point.x
            dify = pacman.y - point.y
            if dify > 0 and valid(point + options[2]):
                plan = options[2]
            elif dify < 0 and valid(point.y + options[3]):
                plan = options[3]
            elif difx > 0 and valid(point.x + options[0]):
                plan = options[0]
            elif difx < 0 and valid(point.x + options[1]):
                plan = options[1]
            else:
                plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, color)

    update()

    for point, course, color in ghosts:
        if abs(pacman - point) < 20:
            return

    ontimer(move, 100)


def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
# Velocidades para PacMan
world()
move()
done()
