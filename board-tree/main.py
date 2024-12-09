import random
from board_helper import *
from board_tree import *

# turn is player whose turn it is, B or W
def get_move(board_size, board_state,
             turn, time_left=0, opponent_time_left=0):

    moves = valid_moves(board_state, turn)
    if (moves == []):
        return None

    random_move = random.choice(moves)
    move(board_size, board_state, turn, random_move)
    #board_state[random_move[0]][random_move[1]] = turn
    return random_move

# min_max get move
def min_max_get_move(board_size, board_state, turn, 
                    time_left=0, opponent_time_left=0):

    node = BoardNode(board=board_state, turn=turn)
    
    mm_move, val = min_max(node, turn)
    if (mm_move == None):
        return None

    move(board_size, board_state, turn, mm_move)

    return mm_move


if __name__ == "__main__":
    print("Wrong file to run...")
