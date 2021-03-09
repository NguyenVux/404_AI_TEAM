import itertools, random

from init import Board


def maxBot(victory_cell, cur_state, you, alpha, beta, depth):

    cell = Board()
    cell.update(cur_state)

    color = 'B' if you == "BLACK" else 'W'
    maxv = -2
    if depth == 0:
        result=is_end(victory_cell, cell, color, True)
    else:
        result = is_end(victory_cell, cell, color)

    px = None
    py = None

    if result == you:
        return (1, None, None)
    elif result != 'DRAW' and result != None:
        return (-1, None, None)
    elif result == 'DRAW':
        return (0, None, None)

    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(y + x, color):
            new_cell = Board()
            new_cell.update(cur_state)
            new_cell.place(y + x, color)

            new_state = new_cell.getCellLineLst()
            competitior = 'BLACK' if you != "BLACK" else 'WHITE'
            (m, min_x, min_y) = minBot(victory_cell, new_state, competitior, alpha, beta, depth-1)
            if m > maxv:
                maxv = m
                px = x
                py = y
            if maxv >= beta:
                return (maxv, px, py)

            if maxv > alpha:
                alpha = maxv
    return maxv, px, py


def minBot(victory_cell, cur_state, you, alpha, beta, depth):
    cell = Board()
    cell.update(cur_state)

    color = 'B' if you == "BLACK" else 'W'
    minv = 2
    if depth == 0:
        result = is_end(victory_cell, cell, color, True)
    else:
        result = is_end(victory_cell, cell, color)

    px = None
    py = None

    if result == you:
        return (-1, None, None)
    elif result != 'DRAW' and result != None:
        return (1, None, None)
    elif result == 'DRAW':
        return (0, None, None)

    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(y + x, color):
            new_cell = Board()
            new_cell.update(cur_state)
            new_cell.place(y + x, color)

            new_state = new_cell.getCellLineLst()

            competitior = 'BLACK' if you != "BLACK" else 'WHITE'
            (m, max_x, max_y) = maxBot(victory_cell, new_state, competitior, alpha, beta, depth-1)
            if m < minv:
                minv = m
                px = x
                py = y
            if minv <= alpha:
                return (minv, px, py)

            if minv < beta:
                beta = minv

    return minv, px, py


def is_end(victory_cells, cell, color, force=False):
    v_b = v_w = 0
    for c in victory_cells:
        v_b += 1 if cell.getValue(c) == 'B' else 0
        v_w += 1 if cell.getValue(c) == 'W' else 0
    if v_b == 5:
        return "BLACK"
    if v_w == 5:
        return "White"

    color = 'B' if color == 'WHITE' else 'W'
    check_playable=False
    if not force:
        check_playable= cell.isPlayable(color)
    if not check_playable:
        b, w = cell.getResult()
        if b > w:
            return "BLACK"
        elif b < w:
            return "WHITE"
        if b == w:
            if v_b > v_w:
                return "BLACK"
            elif v_b < v_w:
                return "WHITE"
            else:
                return "DRAW"

    return None


def callBot(game_info):
    lines = game_info.split('\n')
    victory_cell = lines[1].split(' ')
    you = lines[-2]
    lines = lines[3:11]
    (m, px, py) = maxBot(victory_cell, lines, you, -2, 2, 8)
    if px == None or py == None:
        return "NULL"
    return py + px


def validSteps(game_info):
    lines = game_info.split('\n')

    victory_cell = lines[1].split(' ')

    cell = Board()
    cell.update(lines[3:11])

    you = lines[12]

    color = 'B' if you == "BLACK" else 'W'

    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    return posible_positions
