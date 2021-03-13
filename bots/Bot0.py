import itertools, random

from init import Board

corner = ['a1', 'a8', 'h1', 'h8']
h_weight = [[120, -20, 20, 5, 5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20, 5, 5, 20, -20, 120]]


def getRowId(numeric_character):
    return ord(numeric_character) - ord('1')


def getColumnId(alphabet_character):
    return ord(alphabet_character) - ord('a')


def getTakenVCell(victory_cell, cell):
    v_b = v_w = 0
    for c in victory_cell:
        if cell.getValue(c) == '@':
            v_b += 1
        if cell.getValue(c) == 'O':
            v_w += 1
    return v_b, v_w


def getWeightSquares(cell, color):
    cell_lines = cell.getCellLineLst()
    total = 0
    for i in range(8):
        cell_lines[i]=cell_lines[i].replace(' ','')
        for j in range(8):
            if cell_lines[i][j] == color:
                total += h_weight[i][j]
            elif cell_lines[i][j]!='-':
                total -= h_weight[i][j]
    return total


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

    check_playable = cell.isPlayable(color)
    if not check_playable:
        return "BLACK" if color == 'O' else 'WHITE'
    return None


def Heuristic(victory_cell, cell, color, max=True):
    op_color = '@' if color != '@' else 'O'
    coinv, op_coinv = 0, 0
    cornerv, op_cornerv = 0, 0
    hstep = 0
    hcorner = 0
    hcoin = 0
    hweight = getWeightSquares(cell, color)

    if color == '@':
        coinv, op_coinv = getTakenVCell(victory_cell, cell)
    else:
        op_coinv, coinv = getTakenVCell(victory_cell, cell)
    if coinv + op_coinv != 0:
        hcoin = 100 * (coinv - op_coinv) / (coinv + op_coinv)
        if hcoin!=100:
            hcoin=0
    stepv = validSteps(cell, color)
    op_stepv = validSteps(cell, op_color)

    cornerv = len(set(corner) & set(stepv))
    op_cornerv = len(set(corner) & set(op_stepv))

    if len(stepv) + len(op_stepv) != 0:
        hstep = 100 * (len(stepv) - len(op_stepv)) / (len(stepv) + len(op_stepv))
        if hstep==100:
            hstep*=4
    if cornerv + op_cornerv != 0:
        hcorner = 100 * (cornerv - op_cornerv) / (cornerv + op_cornerv)
    score = 4 * hstep + hweight + hcorner * 9 + 11 * hcoin
    score = -score if not max else score
    return score, None, None


def maxBot(victory_cell, cell_line, you, alpha, beta, depth):
    cell = Board()
    cell.update(cell_line)

    color = '@' if you == "BLACK" else 'O'
    result = is_end(victory_cell, cell, color)
    if depth == 0 or result != None and result != you:
        return Heuristic(victory_cell, cell, color)
    # elif result != None and result != you:
    #     return -999998, None, None
    elif result == you:
        return 999998, None, None

    maxv = -999999

    px = None
    py = None
    cur_weight = getWeightSquares(cell, color)

    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(y + x, color):
            new_cell = Board()
            new_cell.update(cell_line)
            new_cell.place(y + x, color)

            new_state = new_cell.getCellLineLst()
            competitior = 'BLACK' if you != "BLACK" else 'WHITE'
            (m, min_x, min_y) = minBot(victory_cell, new_state, competitior, alpha, beta, depth - 1)
            m += cur_weight
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
    if depth == 0 or result != None and result != you:
        return Heuristic(victory_cell, cell, color, False)
    # elif result != None and result != you:
    #     return 999998, None, None
    elif result == you:
        return -999998, None, None

    minv = 999999

    px = None
    py = None
    cur_weight = getWeightSquares(cell, color)

    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(y + x, color):
            new_cell = Board()
            new_cell.update(cell_line)
            new_cell.place(y + x, color)

            new_state = new_cell.getCellLineLst()
            competitior = 'BLACK' if you != "BLACK" else 'WHITE'
            (m, max_x, max_y) = maxBot(victory_cell, new_state, competitior, alpha, beta, depth - 1)
            m -= cur_weight
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
    (m, px, py) = maxBot(victory_cell, lines, you, -999999, 999999, 2)
    if px == None or py == None:
        return "NULL"
    return py + px


def validSteps(cell, color):
    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    return posible_positions
