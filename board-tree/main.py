import random
from board_helper import *
from BoardNode import *

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

# ab get move 
def ab_get_move(board_size, board_state, turn,
                time_left=0, opponent_time_left=0):

    node = BoardNode(board=board_state)
 
    inf = float('inf')
    neg_inf = float('-inf')

    max_player = turn 
    min_player = white if turn == black else black

    ab_move, val = min_max_ab(node, max_player, min_player, "MAX", neg_inf, inf)
    if (ab_move == None):
        return None

    move(board_size, board_state, turn, ab_move)

    return ab_move

if __name__ == "__main__":
    print("Wrong file to run...")
