import itertools, random

from init import Board,Game

def bot(victory_cell, cell, you):
    color = 'B' if you == "BLACK" else 'W'

    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    
    heuristic_othello_board(cell,victory_cell,color)
    if len(posible_positions) > 0:
        return random.choice(posible_positions)
    else:
        return "NULL"

def callBot(game_info):
    lines = game_info.split('\n')

    victory_cell = lines[1].split(' ')

    cell = Board()
    cell.update(lines[3:11])

    you = lines[12]

    return bot(victory_cell, cell, you)

def valid_positions(cell,color):
    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    return posible_positions

coef = (0.5,0.5,1,1)
def heuristic_othello_board(board: Board, victory_cell, you):
    opponent_color = 'W' if you == 'B' else 'B'
    print(opponent_color)
    print(you)
    self_valid_move = valid_positions(board,you)
    opponent_valid_move = valid_positions(board,opponent_color)
    #self_ocurred_victory_cell
    print("Self available move: " + str(len(self_valid_move)))
    print("Opponent available move: " + str(len(opponent_valid_move)))