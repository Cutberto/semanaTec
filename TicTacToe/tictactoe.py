from turtle import *

from freegames import line


# This function draws the grid in the display
def grid():
    """Draw tic-tac-toe grid."""
    line(-67, 200, -67, -200)
    line(67, 200, 67, -200)
    line(-200, -67, 200, -67)
    line(-200, 67, 200, 67)


# This functions draws the X for player #1
def drawx(x, y):
    """Draw X player."""
    line(x, y, x + 133, y + 133)
    line(x, y + 133, x + 133, y)


# This function draws the o for player #2
def drawo(x, y):
    """Draw O player."""
    up()
    goto(x + 67, y + 5)
    down()
    circle(62)


# This function returns the value rounded down
def floor(value):
    """Round value down to grid with square size 133."""
    return ((value + 200) // 133) * 133 - 200


# These variables contain the turn of the player and
# and array of both players
state = {'player': 0}
players = [drawx, drawo]
# Matrix to determine if a block is occupied
isUsed = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


def tap(x, y):

    """Draw X or O in tapped square."""
    x = floor(x)
    y = floor(y)
    player = state['player']
    draw = players[player]
    if (player):
        pencolor("red")
        width(2)
    else:
        pencolor("blue")
        width(4)
    #Conditional structure to check if a place is used
    if x == -200.0 and y == 66.0:
        if not isUsed[0][0]:
            draw(x, y)
            isUsed[0][0] = 1
            state['player'] = not player
    elif x == -67.0 and y == 66.0:
        if not isUsed[0][1]:
            draw(x, y)
            isUsed[0][1] = 1
            state['player'] = not player
    elif x == 66.0 and y == 66.0:
        if not isUsed[0][2]:
            draw(x, y)
            isUsed[0][2] = 1
            state['player'] = not player
    elif x == -200.0 and y == -67.0:
        if not isUsed[1][0]:
            draw(x, y)
            isUsed[1][0] = 1
            state['player'] = not player
    elif x == -67.0 and y == -67.0:
        if not isUsed[1][1]:
            draw(x, y)
            isUsed[1][1] = 1
            state['player'] = not player
    elif x == 66.0 and y == -67.0:
        if not isUsed[1][2]:
            draw(x, y)
            isUsed[1][2] = 1
            state['player'] = not player
    elif x == -200.0 and y == -200.0:
        if not isUsed[2][0]:
            draw(x, y)
            isUsed[2][0] = 1
            state['player'] = not player
    elif x == -67.0 and y == -200.0:
        if not isUsed[2][1]:
            draw(x, y)
            isUsed[2][1] = 1
            state['player'] = not player
    elif x == 66.0 and y == -200.0:
        if not isUsed[2][2]:
            draw(x, y)
            isUsed[2][2] = 1
            state['player'] = not player
    update()


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
grid()
update()
onscreenclick(tap)
done()
