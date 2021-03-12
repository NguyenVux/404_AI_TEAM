import itertools, random

from init import Board

corner = ['a1', 'a8', 'h1', 'h8']
h_weight = [[80, -26, 24, -1,-5, 28, -18, 76],
              [-23, -39, -18, -9, -6, -8, -39, -1],
              [46, -16, 4, 1, -3, 6, -20, 52],
              [-13, -5, 2, -1, 4, 3, -12, -2],
              [-5, -6, 1, -2, -3, 0, -9, -5],
              [48, -13, 12, 5, 0, 5, -24, 41],
              [-27, -53, -11, -1, -11, -16, -58, -15],
              [87, -25, 27, -1, 5, 36, -3, 100]]


def getRowId(numeric_character):
    return ord(numeric_character) - ord('1')

def getColumnId(alphabet_character):
    return ord(alphabet_character) - ord('a')

def getTakenVCell(victory_cell, cell):
    count = 0
    v_b = v_w = 0
    for c in victory_cell:
        if cell.getValue(c) == '@':
            count += 1
            v_b += 1
        if cell.getValue(c) == 'O':
            count += 1
            v_w += 1
    return v_b, v_w

def getWeight(valid_moves):
    weight=0
    for i in valid_moves:
        alphabet_character, numeric_character = tuple(i)
        row=getRowId(numeric_character)
        col=getColumnId(alphabet_character)
        weight+=h_weight[row][col]
    return weight

def is_end(victory_cells, cell, color):
    v_b = v_w = 0
    count = 0

    v_b, v_w = getTakenVCell(victory_cells, cell)
    if v_b == 5:
        return "BLACK"
    if v_w == 5:
        return "WHITE"

    if count == 5:
        if v_w > v_b:
            return "WHITE"
        return "BLACK"

    color_op = '@' if color == 'WHITE' else 'O'
    check_playable = cell.isPlayable(color)
    if not check_playable:
        return "BLACK" if color == 'O' else '@'
    return None


def Heuristic(victory_cell, cell, color, max=True):
    op_color = '@' if color != '@' else 'O'
    coinv, op_coinv = 0, 0
    cornerv, op_cornerv=0,0
    weight, op_weight=0,0
    hcoin = 0
    hstep = 0
    hcorner = 0
    hweight=0

    if color == '@':
        coinv, op_coinv = getTakenVCell(victory_cell, cell)
    else:
        op_coinv, coinv = getTakenVCell(victory_cell, cell)

    stepv = validSteps(cell, color)
    op_stepv = validSteps(cell, op_color)

    weight=getWeight(stepv)
    op_weight=getWeight(op_stepv)
    cornerv = len(set(corner) & set(stepv))
    op_cornerv=len(set(corner) & set(op_stepv))

    if coinv + op_coinv!=0:
        hcoin = 100 * (coinv - op_coinv) / (coinv + op_coinv)
    if len(stepv) + len(op_stepv)!=0:
        hstep = 100 * (len(stepv)-len(op_stepv)) / (len(stepv) + len(op_stepv))
    if cornerv+op_cornerv!=0:
        hcorner=100*(cornerv-op_cornerv)/(cornerv+op_cornerv)
    if weight+op_weight!=0:
        hweight=100*(weight-op_weight)/(weight+op_weight)
    score = 25.5*hstep+25*hcoin+10*hweight + 27*hcorner
    score=-score if not max else score
    return score, None, None

def maxBot(victory_cell, cell_line, you, alpha, beta, depth):
    cell = Board()
    cell.update(cell_line)

    color = '@' if you == "BLACK" else 'O'
    result = is_end(victory_cell, cell, color)
    if depth == 0:
        return Heuristic(victory_cell, cell, color)
    elif result != None and result != you:
        return -999998, None, None
    elif result==you:
        return 999999, None, None

    maxv = -999999

    px = None
    py = None

    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(y + x, color):
            new_cell = Board()
            new_cell.update(cell_line)
            new_cell.place(y + x, color)

            new_state = new_cell.getCellLineLst()
            competitior = 'BLACK' if you != "BLACK" else 'WHITE'
            (m, min_x, min_y) = minBot(victory_cell, new_state, competitior, alpha, beta, depth - 1)
            if m > maxv:
                maxv = m
                px = x
                py = y
            if maxv >= beta:
                return (maxv, px, py)

            if maxv > alpha:
                alpha = maxv
    return maxv, px, py


def minBot(victory_cell, cell_line, you, alpha, beta, depth):
    cell = Board()
    cell.update(cell_line)

    color = '@' if you == "BLACK" else 'O'
    result = is_end(victory_cell, cell, color)
    if depth == 0:
        return Heuristic(victory_cell, cell, color, False)
    elif result != None and result != you:
        return 999998, None, None
    elif result==you:
        return -999999, None, None

    minv = 999999

    px = None
    py = None

    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(y + x, color):
            new_cell = Board()
            new_cell.update(cell_line)
            new_cell.place(y + x, color)

            new_state = new_cell.getCellLineLst()
            competitior = 'BLACK' if you != "BLACK" else 'WHITE'
            (m, max_x, max_y) = maxBot(victory_cell, new_state, competitior, alpha, beta, depth - 1)
            if m < minv:
                minv = m
                px = x
                py = y
            if minv <= alpha:
                return (minv, px, py)

            if minv < beta:
                beta = minv
    return minv, px, py


def callBot(game_info):
    lines = game_info.split('\n')
    victory_cell = lines[1].split(' ')
    you = lines[-2]
    lines = lines[3:11]
    (m, px, py) = maxBot(victory_cell, lines, you, -999999, 999999, 3)
    if px == None or py == None:
        return "NULL"
    return py + px


def validSteps(cell, color):
    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    return posible_positions
