import itertools
from init import Board
UNStable_lst = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
                       'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8',
                       'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8',
                       'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8',
                       'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8',
                       'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
                       'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8',
                       'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8']
stable_lst = [[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]

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
        cell_lines[i] = cell_lines[i].replace(' ', '')
        for j in range(8):
            if cell_lines[i][j] == color:
                total += h_weight[i][j]
            elif cell_lines[i][j] != '-':
                total -= h_weight[i][j]
    return total


def stableCount(cell, color):
    count=0
    unstable_list_fake=UNStable_lst.copy()
    stable_lst_fake=stable_lst.copy()
    for i in range(len(unstable_list_fake)):
        stable = False
        if cell.getValue(unstable_list_fake[i]) == color:
            stable = isStableVertical(unstable_list_fake[i],stable_lst_fake) and \
                     isStableHorizontal( unstable_list_fake[i],stable_lst_fake) and \
                     isStableLeftDiagonal(unstable_list_fake[i],stable_lst_fake) and \
                     isStableRightDiagonal(unstable_list_fake[i],stable_lst_fake)
            if stable:
                alphabet_character, numeric_character = tuple(unstable_list_fake[i])
                stable_lst_fake[getRowId(numeric_character)][getColumnId(alphabet_character)] = 1
                count+=1
    return count

def isStableLeftDiagonal(position, stable_lst_fake):
    alphabet_character, numeric_character = tuple(position)
    rowUP = getRowId(numeric_character) + 1
    rowDown = getRowId(numeric_character) - 1
    colUp = getColumnId(alphabet_character) + 1
    colDown = getColumnId(alphabet_character) - 1

    if (rowDown < 0 or colDown < 0):
        return True
    if (rowUP > 7 or colUp > 7):
        return True
    if (stable_lst_fake[rowDown][colDown] == 1) or (stable_lst_fake[rowUP][colUp] == 1):
        return True
    return False


def isStableRightDiagonal(position, stable_lst_fake):
    alphabet_character, numeric_character = tuple(position)
    rowUP = getRowId(numeric_character) + 1
    rowDown = getRowId(numeric_character) - 1
    colUp = getColumnId(alphabet_character) + 1
    colDown = getColumnId(alphabet_character) - 1

    if (rowDown < 0 or colUp > 7):
        return True
    if (rowUP > 7 or colDown < 0):
        return True
    if (stable_lst_fake[rowDown][colUp] == 1) or (stable_lst_fake[rowUP][colDown] == 1):
        return True
    return False


def isStableVertical(position, stable_lst_fake):
    alphabet_character, numeric_character = tuple(position)
    rowUP = getRowId(numeric_character) + 1
    rowDown = getRowId(numeric_character) -1
    col = getColumnId(alphabet_character)

    if (rowDown < 0):
        return True
    if (rowUP > 7):
        return True
    if (stable_lst_fake[rowDown][col] == 1) or (stable_lst_fake[rowUP][col] == 1):
        return True
    return False


def isStableHorizontal(position, stable_lst_fake):
    alphabet_character, numeric_character = tuple(position)
    row = getRowId(numeric_character)
    colUp = getColumnId(alphabet_character) + 1
    colDown = getColumnId(alphabet_character) - 1

    if (colUp > 7):
        return True
    if (colDown < 0):
        return True
    if (stable_lst_fake[row][colUp] == 1) or (stable_lst_fake[row][colDown] == 1):
        return True
    return False


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
    cornerv, op_cornerv = 0, 0
    stepv = validSteps(cell, color)
    op_stepv = validSteps(cell, op_color)
    if stepv == 0:
        return -9999 if max else 9999
    if op_stepv == 0:
        return 9999 if max else -9999

    my_stb=stableCount(cell,color)
    op_stb=stableCount(cell,op_color)
    hstep = 0
    hcorner = 0
    hcoin = 0
    hstb=0
    hweight = getWeightSquares(cell, color)

    if color == '@':
        coinv, op_coinv = getTakenVCell(victory_cell, cell)
    else:
        op_coinv, coinv = getTakenVCell(victory_cell, cell)
    if coinv + op_coinv != 0:
        hcoin = 100 * (coinv - op_coinv) / (coinv + op_coinv)
        if hcoin != 100 and hcoin!=-100:
            hcoin = 0

    cornerv = len(set(corner) & set(stepv))
    op_cornerv = len(set(corner) & set(op_stepv))

    if len(stepv) + len(op_stepv) != 0:
        hstep = 100 * (len(stepv) - len(op_stepv)) / (len(stepv) + len(op_stepv))
        if hstep == 100 or hstep==-100:
            hstep *= 11 / 4
    if cornerv + op_cornerv != 0:
        hcorner = 100 * (cornerv - op_cornerv) / (cornerv + op_cornerv)
    if my_stb+op_stb!=0:
        hstb=100*(my_stb-op_stb)/(my_stb+op_stb)

    score = 4 * hstep + hweight + hcorner * 10 + 8*hstb + 5*hcoin
    score = -score if not max else score
    return score

def isMovesLeft(cell, color):
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
            if cell.isPlaceable(c + r, color):
                return True
    return False

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



def minimax(victory_cell, cur_state, you, depth, isMax, alpha, beta):
    game = Board()
    game.update(cur_state)
    color = '@' if you == "BLACK" else 'O'
    opponent = "WHITE" if you == "BLACK" else 'BLACK'
    final = evaluated(victory_cell, game, you)

    if final == you:
        if isMax:
            return 9999
        else:
            return -9999
    elif final != 'DRAW' and final != None:
        if isMax:
            return -9999
        else:
            return 9999
    elif final == 'DRAW':
        return 0

    if depth == 0 and game.isPlayable(color):
        if isMax:
            return Heuristic(victory_cell, game, color, True)
        else:
            return Heuristic(victory_cell, game, color, False)
    if isMovesLeft(game,color) == False:
        return 0

    if isMax:
        best = -9999
        for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
            if game.isPlaceable(y + x, color):
                new_game = Board()
                new_game.update(cur_state)
                new_game.place(y + x, color)
                new_state = new_game.getCellLineLst()

                best = max(best, minimax(victory_cell, new_state, opponent, depth - 1, False, alpha, beta))
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best
    else:
        best = 9999
        for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
            if game.isPlaceable(y + x, color):
                new_game = Board()
                new_game.update(cur_state)
                new_game.place(y + x, color)
                new_state = new_game.getCellLineLst()

                best = min(best, minimax(victory_cell, new_state, opponent, depth - 1, True, alpha, beta))
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best

def prior_spot(spot):
    score = 0
    list_12=['a1', 'h1', 'a8', 'h8']
    list_2 =['c1', 'f1', 'c8', 'f8', 'a3', 'h3', 'a6', 'h6']
    list_1_5=['c3', 'f3', 'c6', 'f6']
    list_0_5=['a4', 'h4', 'a5', 'h5', 'd1', 'e1', 'd8', 'e8']
    list_minus0_5 = ['c2', 'd2', 'e2', 'f2', 'b3', 'b4', 'b5', 'b6', 'g3'
                     'g4', 'g5', 'g6', 'c7', 'd7', 'e7', 'f7']
    list_minus2 = ['b1', 'g1', 'b8', 'g8', 'a2', 'h8', 'a7', 'h7']
    list_minus4 = ['b2', 'g2', 'b7', 'g7']
    if spot in list_12:
        score += 120
    elif spot in list_2:
        score += 20
    elif spot in list_1_5:
        score += 15
    elif spot in list_minus2:
        score += -20
    elif spot in list_minus4:
        score += -40
    elif spot in list_0_5:
        score += 5
    elif spot in list_minus0_5:
        score += -5
    else:
        score += 3
    return score



def BestMove(victory_cell, cur_state, you, depth):
    game = Board()
    game.update(cur_state)
    color = '@' if you == "BLACK" else 'O'
    px = None
    py = None
    bestVal = -9999
    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if game.isPlaceable(y + x, color):
            new_game = Board()
            new_game.update(cur_state)
            new_game.place(y + x, color)
            new_state = new_game.getCellLineLst()
            moveVal = minimax(victory_cell, new_state, you, depth, True, -9999, 9999)
            '''print("moveVal: ", moveVal)
            print("minimax: ", minimax(victory_cell, new_state, you, depth, True))
            print("prior_spot: ", prior_spot(x, y))
            print("bestVal: ", bestVal, "\n")'''
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
