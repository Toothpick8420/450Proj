
from copy import deepcopy
from main import *


# Used in construction to make sure we don't just build every possible board 
# because the branch factor gets large
MAX_DEPTH = 15
# Used in print but I wanted to be able to have variablity from just \t
TAB_STRING = '    '


# Black is negative numbers 
# White is positive numbers
# Combined will show advantage, if positive white is advantage and vice versa

# A Node that contains a board and all successors 
class BoardNode():
    
    def __init__(self, board=[], turn=None, depth=0):
        # If its whites turn the last turn was black -> used to set whose 
        # board this is for score 
        # when we score the board we need to make sure that its scored as our turn
        last_turn = white if turn == black else black

        self.board = board
        self.n = len(self.board)
        self.children = []
        self.value = score_board(board, last_turn)
        self.moves = valid_moves(self.board, turn)

        if (depth < MAX_DEPTH):
            # Generate the next available boards for each move
            for mv in self.moves:
                next_board = deepcopy(self.board) # Make a deep copy of the board
                move(self.n, next_board, turn, mv)

                # Toggle the turn so that its not just repeatedly making white 
                # moves, it actually builds out the tree back and forth
                next_turn = white if turn == black else black
                self.children.append(BoardNode(next_board, next_turn, depth+1))

        return # Explicit return for printing


    def print(self, depth=0):
        # Helper function -> prints board adding indent level infront of it
        def print_board_(self, depth_):
            indent = TAB_STRING * depth_

            l = indent + self.n * '+-' + '+'
            print(l)
            for row in self.board:
                print(indent + '|' + '|'.join([str(_) for _ in row]) + '|')
                print(l)

        
        # print the current states board and its score
        print_board_(self, depth)
        print((TAB_STRING * depth) + str(self.value))

        # print all children 1 level deeper
        for child in self.children: 
            child.print(depth+1)

        return # Explicit return for printing


# Determines the value of the board 
# Takes in a board and turn 
# Calculates the score of the board from the view of the turn 
# so if its 
def score_board(board, turn):
    max_player = turn 
    min_player = white if turn == black else black

    # Represents the value of the board
    score = 0

    # Iterate over the board checking
    for row in board:
        for col in row:
            if col == max_player:
                score += 1
            elif col == min_player:
                score -= 1

    # add scores to get the difference between them 
    return score 


if __name__ == "__main__":
    ## Replace with whatever board size you want to run on
    board_state = [[' ', ' ', ' ', ' '],
                   [' ', 'W', 'B', ' '],
                   [' ', 'B', 'W', ' '],
                   [' ', ' ', ' ', ' ']]

    node = BoardNode(board=board_state, turn=white, depth=0)
    node.print()
