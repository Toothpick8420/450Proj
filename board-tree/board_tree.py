
from copy import deepcopy
from main import *

'''
Notes:
 - This is not optimized at all currently 
 - Not memory efficient and not time complexity efficient
 - Does not go more than 1 level deep -> just the next available moves stored   
    * This is what I will be working on, making it an actual tree where we can 
    scan a set depth ahead from any given move / state 
 - A tree class that I plan to make next will have the root node and build out the 
 tree from there I think, still not 100% on implementation details yet 

Ideas:


'''

# Used in construction to make sure we don't just build every possible board 
# because the branch factor gets large
MAX_DEPTH = 15
# Used in print but I wanted to be able to have variablity from just \t
TAB_STRING = '    '

# A Node that contains a board and all successors 
class BoardNode():
    
    def __init__(self, board=[], turn=None, depth=0):
        self.board = board
        self.n = len(self.board)
        self.children = []
        self.moves = valid_moves(self.board, turn)

        if (depth < MAX_DEPTH):
            # Generate the next available boards for each move
            for mv in self.moves:
                next_board = deepcopy(self.board) # Make a deep copy of the board
                move(self.n, next_board, turn, mv)

                next_turn = white if turn == black else black
                self.children.append(BoardNode(next_board, next_turn, depth+1))

    def print(self, depth=0):
        # Helper function -> prints board adding indent level infront of it
        def print_board_(self, depth_):
            indent = TAB_STRING * depth_

            l = indent + self.n * '+-' + '+'
            print(l)
            for row in self.board:
                print(indent + '|' + '|'.join([str(_) for _ in row]) + '|')
                print(l)

        
        # print the current states board
        print_board_(self, depth)
        # print all children 1 level deeper
        for child in self.children: 
            child.print(depth+1)


if __name__ == "__main__":
    ## Replace with whatever board size you want to run on
    board_state = [[' ', ' ', ' ', ' '],
                   [' ', 'W', 'B', ' '],
                   [' ', 'B', 'W', ' '],
                   [' ', ' ', ' ', ' ']]

    node = BoardNode(board=board_state, turn=white, depth=0)
    node.print()
