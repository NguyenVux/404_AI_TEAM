import itertools, random
import numpy as np

from init import Board,Game

coef = (0.5,3,3,3)

cells_score = np.array([[800, -26, 24, -1, -5, 28, -18, 76],
              [-23, -39, -18, -9, -6, -8, -39, -1],
              [46, -16, 4, 1, -3, 6, -20, 52],
              [-13, -5, 2, -1, 4, 3, -12, -2],
              [-5, -6, 1, -2, -3, 0, -9, -5],
              [48, -13, 12, 5, 0, 5, -24, 41],
              [-27, -53, -11, -1, -11, -16, -58, -15],
              [870, -25, 27, -1, 5, 36, -3, 100]])
d  =3
def botMax(cell_lines,you,alpha = None ,beta = None,depth = 8):
    board = Board()
    board.update(cell_lines)
    result = is_win(board,you)
    if result is not None:
        if result != you:
            return None,999999999999
        else:
            return None,-999999999999
    else:
        if depth == 0:
            return None, heuristic_othello_board(board,None,you)
        vmax = -999999999999999999
        valid_moves = valid_positions(board,you)
        move = ""
        for i in valid_moves:
            next_stage = Board()
            next_stage.update(cell_lines)
            next_stage.place(i,you)
            color = 'O' if you == '@' else '@'
            _,point = botMin(next_stage.getCellLineLst(),color,alpha,vmax,depth-1)
            if point > vmax:
                vmax = point
                move = i
            if alpha is not None and alpha >= point:
                return i,vmax
        
        return move, vmax

def botMin(cell_lines,you,alpha = None ,beta = None,depth = 8):
    global d
    board = Board()
    board.update(cell_lines)
    result = is_win(board,you)
    if result is not None:
        if result != you:
            return None,-999999999999
        else:
            return None,999999999999
    else:
        if depth == 0:
            return None, heuristic_othello_board(board,None,you)
        vmin = 999999999999999999
        valid_moves = valid_positions(board,you)
        
        move = ""
        for i in valid_moves:
            next_stage = Board()
            next_stage.update(cell_lines)
            next_stage.place(i,you)
            color = 'O' if you == '@' else '@'
            _,point = botMax(next_stage.getCellLineLst(),color,vmin,beta,depth-1)
            if point < vmin:
                vmin = point
                move = i
            if beta is not None and beta <= point:
                return i,vmin
        return move,vmin

def callBot(game_info, cell_score = None):
    global cells_score,d
    if cell_score is not None:
        cells_score = cell_score
    lines = game_info.split('\n')

    victory_cell = lines[1].split(' ')

    cell = Board()
    cell.update(lines[3:11])

    you = lines[12]
    you = 'O' if you == 'WHITE' else '@'
    move,point = botMax(cell.getCellLineLst(), you,depth = 5)
    if move is None:
        return "NULL"
    return move


def is_win(board,color):
    opponent_color = 'O' if color == '@' else '@'
    if len(valid_positions(board,color)) == 0:
        return opponent_color
    if len(valid_positions(board,opponent_color))==0:
        return color
    return None
def valid_positions(cell,color):
    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    return posible_positions


def heuristic_othello_board(board: Board, victory_cell, you):
    opponent_color = 'O' if you == '@' else '@'
    self_valid_move = valid_positions(board,you)
    opponent_valid_move = valid_positions(board,opponent_color)

    self_cells_score = 0
    opponent_cells_score = 0
    for i in self_valid_move:
        self_cells_score += cells_score[board.getRowId(i[1]),board.getColumnId(i[0])]
        
    
    for i in opponent_valid_move:
        opponent_cells_score += cells_score[board.getRowId(i[1]),board.getColumnId(i[0])]
        #board.place()
    

    #self_ocurred_victory_cell
    return \
        coef[0]*len(self_valid_move)-\
        coef[1]*len(self_valid_move)+\
        coef[2]*self_cells_score/10000-\
        coef[3]*opponent_cells_score/10000
