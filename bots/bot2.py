import itertools, random

from init import Board,Game

def botMax(cell_lines,you,depth = 8):
    board = Board()
    board.update(cell_lines)
    result = is_win(board,you)
    if result is not None or depth == 0:
        return None, heuristic_othello_board(board,None,you)
    else:
        vmax = -999999
        valid_moves = valid_positions(board,you)
        move = ""
        for i in valid_moves:
            next_stage = Board()
            next_stage.update(cell_lines)
            next_stage.place(i,you)
            color = 'W' if you == 'B' else 'B'
            _,point = botMin(next_stage.getCellLineLst(),color,depth-1)
            if point > vmax:
                vmax = point
                move = i
        return move, vmax

def botMin(cell_lines,you,depth = 8):
    board = Board()
    board.update(cell_lines)
    result = is_win(board,you)
    if result is not None or depth == 0:
        return None, heuristic_othello_board(board,None,you)
    else:
        vmin = 999999
        valid_moves = valid_positions(board,you)
        move = ""
        for i in valid_moves:
            next_stage = Board()
            next_stage.update(cell_lines)
            next_stage.place(i,you)
            color = 'W' if you == 'B' else 'B'
            _,point = botMax(next_stage.getCellLineLst(),color,depth-1)
            if point < vmin:
                vmin = point
                move = i
        return move,vmin

def callBot(game_info):
    lines = game_info.split('\n')

    victory_cell = lines[1].split(' ')

    cell = Board()
    cell.update(lines[3:11])

    you = lines[12]
    you = 'W' if you == 'WHITE' else 'B'
    move,point = botMax(cell.getCellLineLst(), you,3)
    print("MAX: "+ str(point))
    if move is None:
        return "NULL"
    return move


def is_win(board,color):
    opponent_color = 'W' if color == 'B' else 'B'
    if len(valid_positions(board,color)) == 0:
        return opponent_color
    return None
def valid_positions(cell,color):
    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    return posible_positions

coef = (0.5,1,0.2,1)
border_coord = list(["a1","b1","c1","d1","e1","f1","g1","h1"
                         ,"a8","b8","c8","d8","e8","f8","g8","h8"
                         ,"a2","a3","a4","a5","a6","a7"
                         ,"h2","h3","h4","h5","h6","h7"])
def heuristic_othello_board(board: Board, victory_cell, you):
    opponent_color = 'W' if you == 'B' else 'B'
    self_valid_move = valid_positions(board,you)
    opponent_valid_move = valid_positions(board,opponent_color)
    self_border_move = 0
    opponent_border_move = 0
    
    for i in self_valid_move:
        if i in border_coord:
            self_border_move += 1
    
    for i in opponent_valid_move:
        if i in border_coord:
            opponent_border_move += 1
    

    #self_ocurred_victory_cell
    return \
        coef[0]*len(self_valid_move)-\
        coef[1]*len(opponent_valid_move)+\
        coef[2]*self_border_move-\
        coef[3]*opponent_border_move
