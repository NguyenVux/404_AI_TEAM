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
        v_b += 1 if cell.getValue(c) == '@' else 0
        v_w += 1 if cell.getValue(c) == 'O' else 0
    if v_b == 5:
        return "BLACK"
    if v_w == 5:
        return "White"

    color = '@' if color == 'WHITE' else 'O'
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
    opponent = '@' if color != "BLACK" else 'O'
    result = '@' if result == "BLACK" else 'O'
    #if len(validSteps(cell, opponent)) == 0:
        #return 100 if max else -100
    #if result != color and result!=None:
        #return -100 if max else 100

    m = 0
    num_steps = len(validSteps(cell, color))
    op_num_steps = len(validSteps(cell, opponent))
    m = num_steps - op_num_steps
    return m if max else -m


def minimax(victory_cell, cur_state, you, depth,isMax ):
    game = Board()
    game.update(cur_state)

    color = '@' if you == "BLACK" else 'O'

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


def prior_spot(x,y,victory_cell):
    score = 0
    list_12=['a1', 'h1', 'a8', 'h8']
    list_2 =['c1', 'f1', 'c8', 'h8', 'a3', 'h3', 'a6', 'h6']
    list_1_5=['c3', 'f3', 'c6', 'f6']
    list_0_5=['a4', 'h4', 'a5', 'h5']
    list_minus0_5 = ['c2', 'd2', 'e2', 'f2', 'b3', 'b4', 'b5', 'b6', 'g3'
                     'g4', 'g5', 'g6', 'c7', 'd7', 'e7', 'f7']
    list_minus2 = ['b1', 'g1', 'b8', 'g8', 'a2', 'h8', 'a7', 'h7']
    list_minus4 = ['b2', 'g2', 'b7', 'g7']
    if y+x in list_12:
        score += 12
    elif y+x in list_2:
        score += 2
    elif y+x in list_1_5:
        score += 1.5
    elif y+x in list_minus2:
        score += -2
    elif y+x in list_minus4:
        score += -4
    elif y+x in list_0_5:
        score += 0.5
    elif y+x in list_minus0_5:
        score += -0.5
    else:
        score += 3
    return score



def BestMove(victory_cell, cur_state, you, depth):
    game = Board()
    game.update(cur_state)
    color = '@' if you == "BLACK" else 'O'
    px = None
    py = None
    bestVal = -1000
    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if game.isPlaceable(y + x, color):
            new_game = Board()
            new_game.update(cur_state)
            new_game.place(y + x, color)
            new_state = new_game.getCellLineLst()
            moveVal = minimax(victory_cell, new_state, you, depth, True) + prior_spot(x, y, victory_cell)
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
    (px, py) = BestMove(victory_cell, lines, you, 2)
    if px == None or py == None:
        return "NULL"
    return py + px
