#global defaults
white = "w"
black = "b"
free = " " #open space
computer = black #default computer to be black moves
human = white #default human to be white moves


def init_board(n):
    b = [[' ' for _ in range(n)] for _ in range(n)]
    b[n//2][n//2] = white
    b[n//2-1][n//2-1] = white
    b[n//2-1][n//2] = black
    b[n//2][n//2-1] = black
    return b


def print_board(b):
    l = len(b) * '+-' + '+'
    print(l)
    for row in b:
        print('|' + '|'.join([str(_) for _ in row]) + '|')
        print(l)
    return


def valid_moves(b, p):
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


def move(b, p):
    vm = valid_moves(b, p)
    if vm == []:
        return
    if p == computer:
        (r, c) = vm[0]
    else:
        r = int(input("row: "))
        c = int(input("col: "))
        #going to assume they moved correctly...
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
            print("between rows",r,r0, "between col",c,c0)
            r1, c1 = r, c
            while r1 != r0 or c1 != c0:
                print("r1:",r1,"c1:",c1)
                b[r1][c1] = p
                r1, c1 = r1 + dr, c1 + dc
    return

        
def win(b): #returns who won (free if tie) or false if no winner yet
    if valid_moves(b, white) == [] and valid_moves(b, black) == []:
        w_c = 0
        b_c = 0
        n = len(b)
        for row in b:
            w_c += row.count(white)
            b_c += row.count(black)
        if w_c > b_c:
            return white
        elif w_c < b_c:
            return black
        else:
            return free
    return False


if __name__ == "__main__":
    n = int(input("board size (even): "))
    b = init_board(n)
    print_board(b)
    while not win(b):
        print(valid_moves(b, white))
        move(b, white)
        move(b, black)
        print_board(b)
    print("the winner was:",win(b))
