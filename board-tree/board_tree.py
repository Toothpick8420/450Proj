
from copy import deepcopy
from board_helper import *


# Used in construction to make sure we don't just build every possible board 
# because the branch factor gets large
MAX_DEPTH = 3
# Used in print but I wanted to be able to have variablity from just \t
TAB_STRING = '    '


# FIXME: Change the way min_max works so that it isn't just black negative
# white positive but that its based on turn, whoevers turn is max  


# Black is negative numbers 
# White is positive numbers
# Combined will show advantage, if positive white is advantage and vice versa

# A Node that contains a board and all successors 
class BoardNode():
    
    def __init__(self, board=[], turn=None, parent_move=None, depth=0):
        next_turn = white if turn == black else black

        self.board = board
        self.n = len(self.board)
        self.children = []
        self.value = score_board(board, turn)
        self.moves = valid_moves(self.board, turn)
        self.parent_move = parent_move
        self.turn = turn
        self.next_turn = next_turn


        if (depth < MAX_DEPTH):
            # Generate the next available boards for each move
            for mv in self.moves:
                next_board = deepcopy(self.board) # Make a deep copy of the board
                move(self.n, next_board, turn, mv)

                # Toggle the turn so that its not just repeatedly making white 
                # moves, it actually builds out the tree back and forth
                self.children.append(BoardNode(next_board, next_turn, mv, depth+1))

        return # Explicit return for printing


    # Misc helper functions

    # Return true if this is a terminal node, aka no chilren or children == []
    def is_terminal(self):
        return len(self.children) == 0

    # Return the value of the board
    def get_value(self):
        return score_board(self.board, self.next_turn)

    # Return the list of children
    def successors(self):
        return self.children

    # Action is the move that results in this state, aka parent_move
    def action(self):
        return self.parent_move


    # Pretty printing of the tree
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
        print((TAB_STRING * depth) + str(self.value) + " " + str(self.parent_move))
        print()

        # print all children 1 level deeper
        for child in self.children: 
            child.print(depth+1)

        return # Explicit return for printing


# Determines the value of the board 
# Takes in a board and turn 
# Calculates the score of the board from the view of the turn 
# so if its 
def score_board(board, turn):
    # Represents the value of the board
    score = 0

    # heuristics
    # I don't know what to do for weights but we will put like 5 on corners
    n = len(board) - 1
    corners = {
            (0, n) : [(0, n-1), (1, n-1), (1, n)], 
            (n, n) : [(n-1, n), (n-1, n-1), (n, n-1)], 
            (n, 0) : [(n-1, 0), (n-1, 1), (n, 1)], 
            (0, 0) : [(1,1), (0,1), (1,0)],

    }
    corner_weight = 5
    
    # Check corners
    for corner, surrounding in corners.items():
        r, c = corner
        if board[r][c] == turn:
            score += corner_weight
        elif board[r][c] == free:
            for sr, sc in surrounding:
                if board[sr][sc] == turn:
                    score -= (corner_weight - 1)
                elif board[sr][sc] == turn:
                    score += (corner_weight - 1)

    # mobility
    score += len(valid_moves(board, turn))
   
    # value based on hesutrics 
    return score 


# Minmax function ab 
global ab_states_processed
ab_states_processed = 0

def min_max_ab(boardNode, turn, alpha, beta):
    global ab_states_processed 
    ab_states_processed += 1

    if (boardNode.is_terminal()):

        return (boardNode.action(), boardNode.get_value())

    # White = Max
    if turn == "MAX":
        max = None
        max_action = None

        for node in boardNode.successors():


            action_value = min_max_ab(node, "MIN", alpha, beta)

            a, v = action_value
        
         
            if (max == None or v > max):
                max = v
                max_action = node.action()

            if v >= beta: return (max_action, max)

            alpha = alpha if alpha > v else v
        

        return (max_action, max)

    else: # Black = Min
        min = None
        min_action = None

        for node in boardNode.successors():
            action_value = min_max_ab(node, "MAX", alpha, beta)

            a, v = action_value

            if (min == None or v < min):
                min = v
                min_action = node.action()

            if v <= alpha: return (min_action, min)

            beta = beta if beta < v else v

        return (min_action, min)


global mm_states_processed 
mm_states_processed = 0

def min_max(boardNode, turn):
    global mm_states_processed 
    mm_states_processed += 1

    if (boardNode.is_terminal()):

        return (boardNode.action(), boardNode.get_value())

    # White = Max
    if turn == "MAX":
        max = None
        max_action = None

        for node in boardNode.successors():


            action_value = min_max(node, "MIN")

            a, v = action_value
        
         
            if (max == None or v > max):
                max = v
                max_action = node.action()

        return (max_action, max)

    else: # Black = Min
        min = None
        min_action = None

        for node in boardNode.successors():
            action_value = min_max(node, "MAX")

            a, v = action_value

            if (min == None or v < min):
                min = v
                min_action = node.action()

        return (min_action, min)





if __name__ == "__main__":


    board_state = make_board(8)

    node = BoardNode(board=board_state, turn=white, depth=0)

    node.print()

    print(min_max_ab(node, white, -10000000, 10000000))
    print(min_max(node, white))

    print(ab_states_processed)
    print(mm_states_processed)
