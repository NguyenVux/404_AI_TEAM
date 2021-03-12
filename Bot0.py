import itertools, random

from init import Board

corner = ['a1', 'a8', 'h1', 'h8']
h_weight = [[4, -3, 2, 2, 2, 2, -3, 4],
            [-3, -4, -1, -1, -1, -1, -4, -3],
            [2, -1, 1, 0, 0, 1, -1, 2],
            [2, -1, 0, 1, 1, 0, -1, 2],
            [2, -1, 0, 1, 1, 0, -1, 2],
            [2, -1, 1, 0, 0, 1, -1, 2],
            [-3, -4, -1, -1, -1, -1, -4, -3],
            [4, -3, 2, 2, 2, 2, -3, 4]]


def getTakenVCell(victory_cell, cell):
    count = 0
    v_b = v_w = 0
    for c in victory_cells:
        if cell.getValue(c) == 'B':
            count += 1
            v_b += 1
        if cell.getValue(c) == 'W':
            count += 1
            v_w += 1
    return v_b, v_w


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

    color_op = 'B' if color == 'WHITE' else 'W'
    check_playable = cell.isPlayable(color)
    if not check_playable:
        return "BLACK" if color == 'W' else 'B'
    return None


def Heuristic(victory_cell, cell, color, max=True):
    op_color = 'B' if color != 'B' else 'W'
    coinv, op_coinv = 0, 0

    if color == 'B':
        coinv, op_coinv = getTakenVCell(victory_cell, cell)
    else:
        op_coinv, coinv = getTakenVCell(victory_cell, cell)

    stepv = len(validSteps(cell, color))
    op_stepv = len(validSteps(cell, op_color))

    hcoin = 100 * (coinv - op_coinv) / (coinv + op_coinv)
    hstep = 100 * (color - op_color) / (color + op_color)
    score = 25,6*hstep+24,4*hcoin
    return score if max else -score    

def maxBot(victory_cell, cell_line, you, alpha, beta, depth):
    cell = Board()
    cell.update(cell_line)

    color = 'B' if you == "BLACK" else 'W'
    result = is_end(victory_cell, cell, color)
    if depth == 0:
        return Heuristic(victory_cell, cell, color)
    elif result != None and result != you:
        return -9998, None, None

    maxv = -9999

    px = None
    py = None

    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(y + x, color):
            new_cell = Board()
            new_cell.update(cur_state)
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


def minBot(victory_cell, lines, you, alpha, beta, depth):
    cell = Board()
    cell.update(cell_line)

    color = 'B' if you == "BLACK" else 'W'
    result = is_end(victory_cell, cell, color)
    if depth == 0:
        return Heuristic(victory_cell, cell, color, False)
    elif result != None and result != you:
        return 9998, None, None

    minv = 9999

    px = None
    py = None

    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(y + x, color):
            new_cell = Board()
            new_cell.update(cur_state)
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
    (m, px, py) = maxBot(victory_cell, lines, you, -9999, 9999, 5)
    if px == None or py == None:
        return "NULL"
    return py + px


def validSteps(cell, color):
    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    return posible_positions
