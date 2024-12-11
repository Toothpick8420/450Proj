white = "W"
black = "B"
free = " " #open space
computer = black #default computer to be black moves
human = white #default human to be white moves

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


# Make board n x n
def make_board(n):
    
    board = [[' ' for _ in range(n)] for _ in range(n)]
    board[n//2-1][n//2-1] = "W"
    board[n//2][n//2-1]   = "B"
    board[n//2-1][n//2]   = "B"
    board[n//2][n//2]     = "W"

    return board
