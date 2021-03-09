import itertools, random

from init import Board


def is_end(victory_cells, cell, color):
    v_b = v_w = 0
    count = 0

    for c in victory_cells:
        if cell.getValue(c) == 'B':
            count += 1
            v_b += 1
        if cell.getValue(c) == 'W':
            count += 1
            v_w += 1
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

def victoryCellLeft(victory_cells, cell):
    count=0
    for c in victory_cells:
        value=cell.getValue(c)
        if  value!= 'B' and value!='W':
            count += 1
    return count

def heuristic(victory_cell, cell, color, max=True):
    result= is_end(victory_cell, cell, color)
    opponent = 'B' if color != "BLACK" else 'W'
    result = 'B' if result == "BLACK" else 'W'
    if len(validSteps(cell, opponent))==0:
        return (9999, None, None) if max else (-9999, None, None)
    if result!=color and result!=None:
        return (-9999, None, None) if max else (9999, None, None)

    m = 0
    num_steps = len(validSteps(cell, color))
    op_num_steps = len(validSteps(cell, opponent))
    m = num_steps - op_num_steps
    return (m, None, None) if max else (-m, None, None)


def maxBot(victory_cell, cur_state, you, alpha, beta, depth):
    cell = Board()
    cell.update(cur_state)

    color = 'B' if you == "BLACK" else 'W'
    maxv = -9999
    if depth == 0:
        return heuristic(victory_cell, cell, color)
    else:
        result = is_end(victory_cell, cell, color)

    px = None
    py = None

    if result == you:
        return (9999, None, None)
    elif result != 'DRAW' and result != None:
        return (-9999, None, None)
    elif result == 'DRAW':
        return (0, None, None)

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


def minBot(victory_cell, cur_state, you, alpha, beta, depth):
    cell = Board()
    cell.update(cur_state)

    color = 'B' if you == "BLACK" else 'W'
    minv = 9999
    if depth == 0:
        return heuristic(victory_cell, cell, color, False)
    else:
        result = is_end(victory_cell, cell, color)

    px = None
    py = None

    if result == you:
        return (-9999, None, None)
    elif result != 'DRAW' and result != None:
        return (9999, None, None)
    elif result == 'DRAW':
        return (0, None, None)

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
<<<<<<< HEAD
    (m, px, py) = maxBot(victory_cell, lines, you, -2, 2, 3)
=======
    (m, px, py) = maxBot(victory_cell, lines, you, -9999, 9999, 5)
>>>>>>> 532467db7d5c8b2f6416d30a2a065d1b6005f54a
    if px == None or py == None:
        return "NULL"
    return py + px


def validSteps(cell, color):
    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    return posible_positions
