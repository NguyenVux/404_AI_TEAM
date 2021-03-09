import itertools, random
import numpy
from init import Board

def validSteps(cell, color):
    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    return posible_positions

def evaluated(victory_cells, cell, color, force=False):
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
        check_playable = cell.isPlayable(color)
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


def heuristic(victory_cell, cell, color, max=True):
    result= evaluated(victory_cell, cell, color)
    opponent = 'B' if color != "BLACK" else 'W'
    result = 'B' if result == "BLACK" else 'W'
    if len(validSteps(cell, opponent)) == 0:
        return 9999 if max else -9999
    if result != color and result!=None:
        return -9999 if max else 9999

    m = 0
    num_steps = len(validSteps(cell, color))
    op_num_steps = len(validSteps(cell, opponent))
    m = num_steps - op_num_steps
    return m if max else -m


def minimax(victory_cell, cur_state, you, depth, isMax):
    game = Board()
    game.update(cur_state)

    color = 'B' if you == "BLACK" else 'W'

    if depth == 0:
        score = heuristic(victory_cell, game, color)
        return score
    else:
        score = evaluated(victory_cell, game, color)

    if score == you:
        return 100
    if score != 'DRAW' and score != None:
        return -100
    if score == 'DRAW':
        return 0

    if(isMax):
        best = -9999
        for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
            if game.isPlaceable(y + x, color):
                new_game = Board()
                new_game.update(cur_state)
                new_game.place(y + x, color)
                new_state= new_game.getCellLineLst()
                best = max(best, minimax(victory_cell, new_state, you, depth-1, not isMax))
        return best
    else:
        best = 9999
        for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
            if game.isPlaceable(y + x, color):
                new_game = Board()
                new_game.update(cur_state)
                new_game.place(y + x, color)
                new_state= new_game.getCellLineLst()
                best = min(best, minimax(victory_cell, new_state, you, depth-1, not isMax))
        return best

def BestMove(victory_cell, cur_state, you, depth):
    game = Board()
    game.update(cur_state)
    color = 'B' if you == "BLACK" else 'W'
    px = None
    py = None
    bestVal = -1000
    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if game.isPlaceable(y + x, color):
            new_game = Board()
            new_game.update(cur_state)
            new_game.place(y + x, color)
            new_state = new_game.getCellLineLst()
            moveVal = minimax(victory_cell, new_state, you, depth, True)
            if moveVal > bestVal:
                px = x
                py = y
                bestVal = moveVal
    return px, py

def callBot(game_info):
    lines = game_info.split('\n')
    victory_cell = lines[1].split(' ')
    you = lines[-2]
    lines = lines[3:11]
    (px, py) = BestMove(victory_cell, lines, you, 4)
    if px == None or py == None:
        return "NULL"
    return py + px
