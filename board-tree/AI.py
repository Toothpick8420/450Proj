from copy import deepcopy

# ========================= BOARD HELPER FUNCTIONS =========================== #
white = "W"
black = "B"
free = " " #open space
computer = black #default computer to be black moves
human = white #default human to be white moves


# Make board n x n
def make_board(n):
    
    board = [[' ' for _ in range(n)] for _ in range(n)]
    board[n//2-1][n//2-1] = "W"
    board[n//2][n//2-1]   = "B"
    board[n//2-1][n//2]   = "B"
    board[n//2][n//2]     = "W"

    return board

# Print the board
def print_board(b):
    l = len(b) * '+-' + '+'
    print(l)
    for row in b:
        print('|' + '|'.join([str(_) for _ in row]) + '|')
        print(l)
    return


def valid_moves(b, p):
    #b is board, p is what palyer it is
    #returns a list of valid moves for that player
    #numba << look into this 
    n = len(b)
    ret = []
    for r, row in enumerate(b):
        for c, val in enumerate(row):
            if val == p:
                #look in all 8 "cardinal" directions
                for (dr, dc) in [(+0, +1), (-1, +1), (-1, +0), (-1, -1),
                                 (+0, -1), (+1, -1), (+1, +0), (+1, +1)]:
                    r0, c0 = r + dr, c + dc
                    flag = False #to make sure it goes through while loop
                    while 0 <= r0 < n and 0 <= c0 < n and \
                          b[r0][c0] != free and b[r0][c0] != p: 
                        #detected valid direction, continue until free spot
                        r0, c0 = r0 + dr, c0 + dc
                        flag = True
                    if 0 <= r0 < n and 0 <= c0 < n and b[r0][c0] == free and flag: 
                        ret.append((r0,c0))
                        #else:
                        #    print("r:",r0,"c:",c0)
    return ret


#n is board size, b board state, p turn, move is (r, c) of move to do
def move(n, b, p, move):
    #b is board, p is player
    #changes board and returns void
    r, c = move
    b[r][c] = p
    for (dr, dc) in [(+0, +1), (-1, +1), (-1, +0), (-1, -1),
                     (+0, -1), (+1, -1), (+1, +0), (+1, +1)]:
        r0, c0 = r + dr, c + dc
        flag = False #to make sure it goes through while loop
        while 0 <= r0 < n and 0 <= c0 < n and \
              b[r0][c0] != free and b[r0][c0] != p: 
            #detected valid direction, continue until free spot
            r0, c0 = r0 + dr, c0 + dc
            flag = True
            if 0 <= r0 < n and 0 <= c0 < n and b[r0][c0] == p and flag:
                #print("between rows",r,r0, "between col",c,c0)
                r1, c1 = r, c
                while r1 != r0 or c1 != c0:
                    #print("r1:",r1,"c1:",c1)
                    b[r1][c1] = p
                    r1, c1 = r1 + dr, c1 + dc
    return


# ======================== BOARD NODE ======================================== #

# Used in construction to make sure we don't just build every possible board 
# because the branch factor gets large
MAX_DEPTH = 3
# Used in print but I wanted to be able to have variablity from just \t
TAB_STRING = '    '


class BoardNode():

    def __init__(self, board=[], turn=None, parent_move=None, depth=0):
        self.action=parent_move;

        self.board = board
        self.n = len(self.board)

        self.white_next_states=[]
        self.black_next_states=[]

        self.terminal = True

        if (depth < MAX_DEPTH):
            self.terminal = False
            both = True if turn == None else False
            # White moves
            if (turn == white or both):
                for mv in valid_moves(self.board, white):
                    new_board = deepcopy(self.board)
                    move(self.n, new_board, white, mv)
                    self.white_next_states.append(BoardNode(new_board, black, mv, depth + 1))

            # Black moves
            if(turn == black or both):
                for mv in valid_moves(self.board, black):
                    new_board = deepcopy(self.board)
                    move(self.n, new_board, black, mv)
                    self.black_next_states.append(BoardNode(new_board, white, mv, depth + 1))


    # Return the board state 
    def state(self):
        return self.board

    # Is this a leaf in the tree
    def is_terminal(self, turn): 
        if (turn == white):
            return len(self.white_next_states) == 0
        else:
            return len(self.black_next_states) == 0

   
    # get the child states from this board based on what turn you want
    def successors(self, turn):
        if turn == white:
            return self.white_next_states
        else:
            return self.black_next_states


    # get the action that lead to this current state
    def get_action(self):
        return self.action

heuristic8x8 = [[100, -10,   8,   6,   6,   8, -10, 100],
             [-10, -25,  -4,  -4,  -4,  -4, -25, -10],
             [  8,  -4,   6,   4,   4,   6,  -4,   8],
             [  6,  -4,   4,   0,   0,   4,  -4,   6],
             [  6,  -4,   4,   0,   0,   4,  -4,   6],
             [  8,  -4,   6,   4,   4,   6,  -4,   8],
             [-10, -25,  -4,  -4,  -4,  -4, -25, -10],
             [100, -10,   8,   6,   6,   8, -10, 100]]

heuristic6x6 =  [[100, -20,   8,   8, -20, 100],
                 [-20,  -6,   4,   4,  -6, -20],
                 [  8,   4,   0,   0,   4,   8],
                 [  8,   4,   0,   0,   4,   8],
                 [-20,  -6,   4,   4,  -6, -20],
                 [100, -20,   8,   8, -20, 100]]

# Score a board state, turn == max -> other == min player
def score_board(boardNode, turn):
    max_player = turn 
    min_player = white if turn == black else black

    board = boardNode.state()
    n = len(board)
    
    # the value of the board
    score = 0

    # Heuristics 

    if (n == 8):
        for r, row in enumerate(board):
            for c, spot in enumerate(row):
                if spot == max_player:
                    score += heuristic8x8[r][c];
                else:
                    score -= heuristic8x8[r][c];
    elif (n == 6):
        for r, row in enumerate(board):
            for c, spot in enumerate(row):
                if spot == max_player:
                    score += heuristic6x6[r][c];
                else:
                    score -= heuristic6x6[r][c];
    '''
    n = len(board) - 1

    # Corners
    # Having a corner is a bonus, the areas directly around them are bad
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
        if board[r][c] == max_player:
            score += corner_weight
        elif board[r][c] == free:
            for sr, sc in surrounding:
                if board[sr][sc] == max_player:
                    score -= (corner_weight - 1)
                elif board[sr][sc] == min_player:
                    score += (corner_weight - 1)

    '''

    # mobility
    score += len(boardNode.successors(max_player))
    score -= len(boardNode.successors(min_player))
   
    # value based on hesutrics 
    return score 


# Min_max function with alpha beta pruning
def min_max_ab(boardNode, max_player, min_player, turn, alpha, beta):
    


    player = max_player if turn == "MAX" else min_player

    # terminal state
    if (boardNode.is_terminal(player)):
        return (boardNode.get_action(), score_board(boardNode, max_player))


    # Max player
    if turn == "MAX":

        max = None
        max_action = None


        for node in boardNode.successors(max_player):

            a, v = min_max_ab(node, max_player, min_player, "MIN", alpha, beta)

            if (max == None or v > max):
                max = v 
                max_action = node.get_action()
            
            if v >= beta: return (max_action, max)

            alpha = alpha if alpha > v else v

        return (max_action, max)

    # Min player
    else:
        min = None 
        min_action = None 

        for node in boardNode.successors(min_player):
            a, v = min_max_ab(node, max_player, min_player, "MAX", alpha, beta)

            if (min == None or v < min):
                min = v 
                min_action = node.get_action()
            
            if v <= alpha: return (min_action, min)

            beta = beta if beta < v else v

        return (min_action, min)

# ============================ GET MOVE ====================================== #


# ab get move 
def get_move(board_size, board_state, turn,
                time_left=0, opponent_time_left=0):

    node = BoardNode(board=board_state, turn=turn)
 
    inf = float('inf')
    neg_inf = float('-inf')

    max_player = turn 
    min_player = white if turn == black else black

    ab_move, val = min_max_ab(node, max_player, min_player, "MAX", neg_inf, inf)
    if (ab_move == None):
        return None

    move(board_size, board_state, turn, ab_move)

    return ab_move


