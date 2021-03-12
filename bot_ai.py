import itertools, random

from init import Board,Game

#clone_state = None
def bot(victory_cell, cell, you,step = 0,prev = None,origin = None):
    #global clone_state
    color = 'B' if you == "BLACK" else 'W'
    
    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    

def callBot(game_info):
    lines = game_info.split('\n')

    victory_cell = lines[1].split(' ')

    cell = Board()
    cell.update(lines[3:11])

    you = lines[12]

    _,__  =  bot(victory_cell, cell, you,0,you)
    return  _
