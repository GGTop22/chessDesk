from tkinter import *
from PIL import ImageTk, Image
from functools import partial
import psycopg2
from tkinter import ttk


def symbolsToIntCoord(k: str) -> (int, int):
    k = k.upper()
    a = ord(k[0]) - ord('A') + 1
    b = int(k[1])
    return (a, b)


def selectAndDrawTask():
    k = int(combo.get())
    white, black = selectTask(k)
    clearDesk()
    drawDesk(white, black)

def clearDesk():
    global btnList
    for b in btnList:
        b.destroy()


root = Tk()
root.geometry("1000x700")

canvas = Canvas(root, width=1000, height=700)
canvas.pack()
btnList = []
#заполнить список значений combo результатами запроса (select номер from задачи order by номер)

combo = ttk.Combobox(canvas,values=["1","2","3"],textvariable="1")
combo.place(x=50,y=75)


load_button = Button(canvas, text="Загрузить", command=selectAndDrawTask)
load_button.place(x=50, y=150)


def isKnightJump(p1: (int, int), p2: (int, int)) -> bool:
    return (abs(p1[0] - p2[0]) == 2 and abs(p1[1] - p2[1]) == 1) or (
            abs(p1[0] - p2[0]) == 1 and abs(p1[1] - p2[1]) == 2)


def isBishopJump(p1: (int, int), p2: (int, int)) -> bool:
    return (abs(p1[0] - p2[0])) == (abs(p1[1] - p2[1]))


def isQueenJump(p1: (int, int), p2: (int, int)) -> bool:
    return isBishopJump(p1, p2) or isRookJump(p1, p2)


def isRookJump(p1: (int, int), p2: (int, int)) -> bool:
    return (p1[0] == p2[0]) or (p1[1] == p2[1])


def isKingJump(p1: (int, int), p2: (int, int)) -> bool:
    return (abs(p1[0] - p2[0])) <= 1 and (abs(p1[1] - p2[1])) <= 1


def isPawnJump(p1: (int, int), p2: (int, int), colour) -> bool:  # Не больше 1 /бить по диоганали
    # если пешка белая то ,если она на второй линии то она может идти на 2 поля вперёд,иначе на 1 поле вперёд
    if colour == "red":
        if p1[1] == 2:  # истина это если не изменился столбец ,а строка увеличилась либо на 1 или на 2
            return (p1[0] == p2[0]) and (p2[1] - p1[1]) in (1, 2)
        else:  # #истина это если не изменился столбец ,а строка увеличилась на 1
            return (p1[0] == p2[0]) and (p2[1] - p1[1]) == 1
    else:
        if p1[
            1] == 7:  # если пешка чёрная то ,если она на 7 линии то она может идти на 2 поля вперёд,иначе на 1 поле вперёд
            return (p1[0] == p2[0]) and (p2[1] - p1[1]) in (
                -1, -2)  # истина это если не изменился столбец ,а строка уменьшилась либо на -1 или на -2
        else:
            return (p1[0] == p2[0]) and (
                    p2[1] - p1[1]) == -1  # истина это если не изменился столбец ,а строка  уменьшилась на -1


def drawDesk(white, black):
    recSize = 60
    x1 = 230
    y1 = 600
    x2 = x1 + recSize
    y2 = y1 + recSize
    clearPossibleMoves()
    for g in range(1, 9):
        # rec = canvas.create_rectangle(x1, y1 - recSize * g, x2, y2 - recSize * g)
        for i in range(1, 9):
            rec = canvas.create_rectangle(x1 + recSize * i, y1 - recSize * g, x2 + recSize * i, y2 - recSize * g,tags="black_rec")
            figurePoint = (i, g)
            drawFigure(figurePoint, white, black, recSize, x1, y1)


def drawFigure(figurePoint, white, black, recSize, x1, y1):
    i = figurePoint[0]
    g = figurePoint[1]
    if figurePoint in black:
        figureName = black[figurePoint]
        drawLabel(figureName, 'black', x1 + recSize * i + 22, y1 - recSize * g + 20, figurePoint)
    if figurePoint in white:
        figureName = white[figurePoint]
        drawLabel(figureName, "red", x1 + recSize * i + 22, y1 - recSize * g + 20, figurePoint)


def drawLabel(text, colour, x, y, figPoint):
    if text == "кр":
        file = "King"
    if text == "ф":
        file = "Queen"
    if text == "с":
        file = "Bishop"
    if text == "к":
        file = "Knight"
    if text == "л":
        file = "Rook"
    if text == "п":
        file = "Pawn"
    file = "img/" + colour.title() + file + ".jpg"

    img = ImageTk.PhotoImage(Image.open(file).resize((55, 55), Image.BICUBIC))
    btn = Button(canvas, image=img, command=partial(click, text, figPoint, colour))
    btn.photo = img
    btn.config(height=55, width=55)

    # label.configure(font="Helvetica 15 bold", fg=colour)
    btn.place(x=x - 21, y=y - 19)
    global btnList
    btnList.append(btn)


# load_button = Button(root, text="Загрузить", command=load_task)
# load_button.pack()

# def load_task():
# selected_move_coord = selected_move.get()  # Получите выбранный ход из выпадающего меню
# if selected_move_coord = "Выберите ход":
#   print(f"Загрузка задачи с ходом: {selected_move_coord}")


# список для хранения возможных координат ходов
possible_moves_list = []

# StringVar для хранения выбранного хода
selected_move = StringVar(root)
selected_move.set("Выберите ход")

move_dropdown = OptionMenu(root, selected_move, possible_moves_list)
move_dropdown.pack()

# def drawMoveDots():
# dots=canvas.create_oval(coords,outline="greena",fill="green",width=3)
figure = None  # Глобальная переменная для хранения выбранной фигуры


def click(text, figPoint, colour):
    global figure
    figure = (text, figPoint, colour)
    print("click click" + "  " + colour + "  " + text + "  " + str(figPoint))
    spisok = []
    for i1 in range(1, 9):
        for i2 in range(1, 9):
            p = (i1, i2)
            if text == "ф" and isQueenJump(figPoint, p) and figPoint != p:
                spisok.append(p)
            if text == "л" and isRookJump(figPoint, p) and figPoint != p:
                spisok.append(p)
            if text == "к" and isKnightJump(figPoint, p) and figPoint != p:
                spisok.append(p)
            if text == "с" and isBishopJump(figPoint, p) and figPoint != p:
                spisok.append(p)
            if text == "кр" and isKingJump(figPoint, p) and figPoint != p:
                spisok.append(p)
            if text == "п" and isPawnJump(figPoint, p, colour) and figPoint != p:
                spisok.append(p)
    clearPossibleMoves()
    drawPossibleMoves(spisok)
    print(spisok)


def drawPossibleMoves(possible_moves):
    global possible_moves_list
    possible_moves_list = possible_moves  # Обновите список возможных ходов
    for move in possible_moves:
        i, g = move
        x = 230 + 60 * i
        y = 600 - 60 * g
        canvas.create_oval(x, y, x + 60, y + 60, outline="green", width=3, tags="green_oval")


def clearPossibleMoves():
    canvas.delete("green_oval")


# Создайте выпадающее меню для отображения возможных ходов


# Обновление выпадающего меню с возможными ходами
# move_dropdown['menu'].delete(0, 'end')  # Очистите существующие варианты
# for move in spisok:
#  i, g = move
# move_coord = f"{chr(64 + i)}{g}"
# move_dropdown['menu'].add_command(label=move_coord, command=partial(select_move, move_coord))


def inputTask(fileName):
    black = {}
    white = {}
    with open(fileName, 'r', encoding="UTF-8") as input:
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
    return (white, black)


def selectTask(number):
    black = {}
    white = {}
    con = psycopg2.connect(database="chess", user="postgres", password="tolstik.1", host="localhost", port="5432")
    cursor_obj = con.cursor()
    cursor_obj.execute(
        f"select название,\"адрес_поля\" from \"фигура на позиции\" join фигуры on \"фигура на позиции\".id_фигуры = фигуры.id where номер_задачи = {number} and  цвет ='чёрный'")
    result = cursor_obj.fetchall()
    print(result)
    for stroka in result:
        figName = stroka[0]
        pos = stroka[1]
        point = symbolsToIntCoord(pos)
        black[point] = figName
    cursor_obj.execute(
        f"select название,\"адрес_поля\" from \"фигура на позиции\" join фигуры on \"фигура на позиции\".id_фигуры = фигуры.id where номер_задачи = {number} and  цвет ='белый'")
    result = cursor_obj.fetchall()
    for stroka in result:
        figName = stroka[0]
        pos = stroka[1]
        point = symbolsToIntCoord(pos)
        white[point] = figName
    return (white, black)


#selectAndDrawTask()

root.mainloop()
