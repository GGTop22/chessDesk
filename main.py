from tkinter import *


def symbolsToIntCoord(k: str) -> (int, int):
    k = k.upper()
    a = ord(k[0]) - ord('A') + 1
    b = int(k[1])
    return (a, b)


with open('INPUT.TXT', 'r') as input:
    s = input.readline().strip().split()

# for i in range(2, 33):
#   point[i] = symbolsToIntCoord(s[i])


root = Tk()
root.geometry("1000x700")

canvas = Canvas(root, width=1000, height=700)
canvas.pack()
black = {}
white = {}


def drawDesk(white, black):
    recSize = 60
    x1 = 230
    y1 = 600
    x2 = x1 + recSize
    y2 = y1 + recSize
    for g in range(1, 9):
        # rec = canvas.create_rectangle(x1, y1 - recSize * g, x2, y2 - recSize * g)
        for i in range(1, 9):
            rec = canvas.create_rectangle(x1 + recSize * i, y1 - recSize * g, x2 + recSize * i, y2 - recSize * g)
            figurePoint = (i, g)
            drawFigure(figurePoint, white, black, recSize, x1, y1)


def drawFigure(figurePoint, white, black, recSize, x1, y1):
    i = figurePoint[0]
    g = figurePoint[1]
    if figurePoint in black:
        figureName = black[figurePoint]
        drawLabel(figureName, 'black', x1 + recSize * i + 22, y1 - recSize * g + 20)
    if figurePoint in white:
        figureName = white[figurePoint]
        drawLabel(figureName, "red", x1 + recSize * i + 22, y1 - recSize * g + 20)


def drawLabel(text, colour, x, y):
    label = Label(canvas, text=text)
    label.configure(font="Helvetica 15 bold", fg=colour)
    label.place(x=x, y=y)


with open('INPUT.TXT', 'r', encoding="UTF-8") as input:
    points = []
    for i in range(2):
        s = input.readline().strip().split()
        kFigure = len(s)
        if i == 0:
            print("WHITE:")
        else:
            print("BLACK:")
        for word in s:
            name, pos = word.split(":")
            point = symbolsToIntCoord(pos)
            print(f" Figure {name} is on cell {point}")
            if i == 0:
                white[point] = name
            else:
                black[point] = name
print(white)
print("________________________")
print(black)
# for i in range(2, 33):
#  points[i] = symbolsToIntCoord(s[i])

drawDesk(white, black)

# for i1 in range(1, 9):
#   canvas.create_rectangle(x1 + recSize, x2, y1, 0)
#  for i2 in range(1, 9):
#     canvas.create_rectangle(x + recSize, 0, y, 0)


root.mainloop()
