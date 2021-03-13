import itertools, random
import numpy as np
from init import Board

H = np.array([[80, -26, 24, -1, -5, 28, -18, 76],
              [-23, -39, -18, -9, -6, -8, -39, -1],
              [46, -16, 4, 1, -3, 6, -20, 52],
              [-13, -5, 2, -1, 4, 3, -12, -2],
              [-5, -6, 1, -2, -3, 0, -9, -5],
              [48, -13, 12, 5, 0, 5, -24, 41],
              [-27, -53, -11, -1, -11, -16, -58, -15],
              [87, -25, 27, -1, 5, 36, -3, 100]]
             )
stone = {1: '@',
         0: 'O'}

col = {0: 'a',
       1: 'b',
       2: 'c',
       3: 'd',
       4: 'e',
       5: 'f',
       6: 'g',
       7: 'h'
       }

row = {0: '1',
       1: '2',
       2: '3',
       3: '4',
       4: '5',
       5: '6',
       6: '7',
       7: '8'}


def get_color_enemy(you):
    if you == 'BLACK':
        return 'O'
    else:
        return '@'


def get_enemy(you):
    if you == 'BLACK':
        return 'WHITE'
    else:
        return "BLACK"


def get_color(you):
    if you == 'BLACK':
        return '@'
    else:
        return 'O'


def memcpy_toTemp(cell, temp_cell):
    for i in range(0, 8):
        for j in range(0, 8):
            temp_cell[i][j] = cell.getValue(col[j] + row[i])
    return temp_cell


def BackUpCell(cell, temp_cell):
    for i in range(0, 8):
        for j in range(0, 8):
            cell.place(str(col[j]) + str(row[i]), str(temp_cell[i][j]))


# calculate the number of pieces when you occupied the corner of board game

def Stability(cell, me):
    k = 0
    num = 0
    a = 0
    b = 0
    c = 0
    d = 0
    i = 0
    j = 0

    if (cell.getValue(col[j] + row[i]) == me):
        num += 1
        ok_a = False
        ok_d = False
        for k in range(1, 8):
            if cell.getValue(col[j] + row[i + k]) != me:
                ok_a = True
                break
            num += 1
        if k == 7 and ok_a is False:
            a += 1

        for k in range(1, 8):
            if cell.getValue(col[j + k] + row[i]) != me:
                ok_d = True
                break
            num += 1
        if k == 7 and ok_d is False:
            d += 1

    i = 7
    j = 0

    if cell.getValue(col[j] + row[i]) == me:
        num += 1
        ok_aa = False
        ok_bb = False
        for k in range(1, 8):
            if cell.getValue(col[j] + row[i - k]) != me:
                ok_aa = True
                break

            num += 1
        if k == 7 and ok_aa is False:
            a += 1

        for k in range(1, 8):
            if cell.getValue(col[j + k] + row[i]) != me:
                ok_bb = True
                break
            num += 1
        if k == 7 and ok_bb is False:
            b += 1

    i = 0
    j = 7

    if (cell.getValue(col[j] + row[i]) == me):
        ok_ccc = False
        ok_ddd = False
        num += 1
        for k in range(1, 8):
            if cell.getValue(col[j] + row[i + k]) != me:
                ok_ccc = True
                break
            num += 1
        if k == 7 and ok_ccc is False:
            c += 1

        for k in range(1, 8):
            if cell.getValue(col[j - k] + row[i]) != me:
                ok_ddd = True
                break
            num += 1
        if k == 7 and ok_ddd is False:
            d += 1

    i = 7
    j = 7

    if (cell.getValue(col[j] + row[i]) == me):
        ok_cccc = False
        ok_bbbb = False
        num += 1
        for k in range(1, 8):
            if cell.getValue(col[j] + row[i - k]) != me:
                ok_cccc = True
                break
            num += 1
        if k == 7 and ok_cccc is False:
            c += 1

        for k in range(1, 8):
            if cell.getValue(col[j - k] + row[i]) != me:
                ok_bbbb = True
                break
            num += 1
        if k == 7 and ok_bbbb is False:
            b += 1

    if (a > 1):
        num -= 8
    if (b > 1):
        num -= 8
    if (c > 1):
        num -= 8
    if (d > 1):
        num -= 8
    return num


def search_fake(victory_cell, cell, you):
    color = '@' if you == "BLACK" else 'O'

    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)

    max_g = -9999999999
    pos = None

    temp_cell = [['_' for _ in range(0, 8)] for i in range(0, 8)]
    memcpy_toTemp(cell, temp_cell)

    cnt = 0

    for pos_victory in victory_cell:
        if pos_victory in temp_cell:
            cnt += 1

    if len(posible_positions) > 0:
        for value in posible_positions:
            c, r = tuple(value)

            if cnt == 4 and value in victory_cell:
                return value
            g = Compute_Grade(cell, you) + H[cell.getRowId(r)][cell.getColumnId(c)]
            if g > max_g:
                pos = value
                max_g = g

        return pos
    else:
        return "NULL"


def Compute_Grade(cell, you, num_occupied):
    posible_positions = []
    posible_positions_enemy = []

    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, get_color(you)):
            posible_positions.append(c + r)
        if cell.isPlaceable(c + r, get_color_enemy(you)):
            posible_positions_enemy.append(c + r)

    SU = Stability(cell, you)
    SE = Stability(cell, get_color_enemy(you))
    NU = (len(posible_positions))
    ME = len(posible_positions_enemy)

    if (NU + ME == 0):
        return 20 * ((SU - SE)) + 35 * (NU - ME)
    elif (num_occupied >= 46):
        return 20 * ((SU - SE)) + 100 * (NU - ME) / (NU + ME)  # 40 ms la 50
    elif (25 <= num_occupied <= 45):
        return 20 * ((SU - SE)) + 50 * (NU - ME) / (NU + ME)
    else:
        return 20 * ((SU - SE)) + 40 * (NU - ME) / (NU + ME)


def checkGameOver(victory_cell, board, you):
    v_b, v_w = 0, 0
    for cell in victory_cell:
        v_b += 1 if board.getValue(cell) == '@' else 0
        v_w += 1 if board.getValue(cell) == 'O' else 0
    if v_b == 5:
        return True
    if v_w == 5:
        return True
    color = get_color_enemy(you)  # set next turn
    if not board.isPlayable(color):
        return True
    return False


def MaxPlayer(cell, victory_cell, depth, you, alpha, beta):
    px = 0
    py = 0
    maxvalue = -999999999999999999

    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, get_color(you)):
            posible_positions.append(c + r)

    temp_cell = [['_' for _ in range(0, 8)] for i in range(0, 8)]
    temp_cell = memcpy_toTemp(cell, temp_cell)
    num_occupid = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if (temp_cell[i][j] != '-'):
                num_occupid += 1

    cnt = 0
    for pos in victory_cell:
        if pos in temp_cell and cell.getValue(pos) == you:
            cnt += 1

    if (depth == 0 or len(posible_positions) <= 0):
        return (Compute_Grade(cell, you, num_occupid), 0, 0)

    for i in range(0, 8):
        for j in range(0, 8):
            if ((col[j] + row[i]) in posible_positions):
                cell.place(col[j] + row[i], get_color(you))
                if (cnt == 4 and (col[j] + row[i]) in victory_cell):
                    return (999999999999999999999, i, j)
                # bonus = 0
                # if (col[j] + row[i]) in victory_cell and H[cell.getRowId(row[i])][cell.getColumnId(col[j])] > 0:
                #     bonus += 50
                # if (col[j] + row[i]) in victory_cell and H[cell.getRowId(row[i])][cell.getColumnId(col[j])] < 50:
                #     bonus -= 100
                (g, max_i, max_) = MinPlayer(cell, victory_cell, depth - 1, get_enemy(you), alpha, beta)

                if g + H[cell.getRowId(row[i])][cell.getColumnId(col[j])] > maxvalue:
                    maxvalue = g + H[cell.getRowId(row[i])][cell.getColumnId(col[j])]
                    px = i
                    py = j
                for ii in range(0, 8):
                    for jj in range(0, 8):
                        cell.place(col[jj] + row[ii], temp_cell[ii][jj])

                if (maxvalue >= beta):
                    return (maxvalue, px, py)

                if (maxvalue > alpha):
                    alpha = maxvalue

    return (maxvalue, px, py)


def MinPlayer(cell, victory_cell, depth, you, alpha, beta):
    minvalue = 999999999999999999
    qx = 0
    qy = 0
    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, get_color(you)):
            posible_positions.append(c + r)
    temp_cell = [['_' for _ in range(0, 8)] for i in range(0, 8)]
    temp_cell = memcpy_toTemp(cell, temp_cell)
    num_occupied = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if (temp_cell[i][j] != '-'):
                num_occupied += 1

    if (depth == 0 or len(posible_positions) <= 0):
        return (Compute_Grade(cell, you, num_occupied), 0, 0)

    cnt = 0
    for pos in victory_cell:
        if pos in temp_cell and cell.getValue(pos) == you:
            cnt += 1
    for i in range(0, 8):
        for j in range(0, 8):
            if (col[j] + row[i]) in posible_positions:
                cell.place(col[j] + row[i], get_color(you))
                if (cnt == 4 and (col[j] + row[i]) in victory_cell):
                    return (999999999999999999999, i, j)

                # + H[cell.getRowId(row[i])][cell.getColumnId(col[j])]
                (g, min_i, min_j) = MaxPlayer(cell, victory_cell, depth - 1, get_enemy(you), alpha, beta)
                if g + H[cell.getRowId(row[i])][cell.getColumnId(col[j])] < minvalue:
                    minvalue = g + H[cell.getRowId(row[i])][cell.getColumnId(col[j])]
                    qx = i
                    qy = j
                for ii in range(0, 8):
                    for jj in range(0, 8):
                        cell.place(col[jj] + row[ii], temp_cell[ii][jj])

                if minvalue <= alpha:
                    return (minvalue, qx, qy)
                if minvalue < beta:
                    beta = minvalue
    return (minvalue, qx, qy)


def bot(victory_cell, cell, you):
    global Col, Row
    search_real = True
    color = '@' if you == "BLACK" else 'O'
    if not search_real:
        return search_fake(victory_cell, cell, you)
    else:
        (g, i, j) = MaxPlayer(cell, victory_cell, 2, you, -99999999999999999999999999999, 99999999999999999999999999999)
        return col[j] + row[i]


# cd AI_Project_01


def callBot(game_info):
    lines = game_info.split('\n')

    victory_cell = lines[1].split(' ')

    cell = Board()
    cell.update(lines[3:11])

    you = lines[12]
    color = '@' if you == "BLACK" else 'O'

    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    print("_____________________________________________")
    print("You: " + str(you))
    print("Victory_cell" + str((victory_cell)))
    print("Possible position: " + str(posible_positions))
    print("a b c d e f g h")
    for i in range(8):
        for j in range(8):
            if (cell.getValue(col[j] + row[i]) == '-'):
                print("_", end=" ")
            else:
                print(cell.getValue(col[j] + row[i]), end=" ")
        print(" " + str(i + 1))
    # print("Compute grades " + str(Compute_Grade(cell, you)))

    print("_____________________________________________")

    return bot(victory_cell, cell, you)