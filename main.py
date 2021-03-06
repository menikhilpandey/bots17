import p1, p2


# Main.py -  main function of this project, all functions to be defined here.
class DisjointSet:
    def __init__(self):
        self.Arr = []
        self.Size = []

    def initialize(self):
        for i in range(169):
            self.Arr.append(i)
            self.Size.append(1)

        for i in range(12):
            self.Arr[1 + i], self.Arr[156 + i] = 1, 156  # Top and Bottom virtual cells.

        for i in range(1, 12):
            self.Arr[13 * i], self.Arr[13 * i + 12] = 13, 25  # Left and Right virtual cells.

    def calc_id(self, x, y):
        return x * 13 + y

    def root(self, i):
        if self.Arr[i] != i:
            self.Arr[i] = self.root(self.Arr[i])
        return self.Arr[i]

    def merge(self, a, b):
        root_a, root_b = self.root(a), self.root(b)
        if root_a != root_b:
            if self.Size[root_a] < self.Size[root_b]:
                self.Arr[root_a], self.Size[root_b] = self.Arr[root_b], self.Size[root_b] + self.Size[root_a]
            else:
                self.Arr[root_b], self.Size[root_a] = self.Arr[root_a], self.Size[root_a] + self.Size[root_b]

    def find_set(self, a, b):
        return self.root(a) == self.root(b)


ds = DisjointSet()
ds.initialize()

# Board (13 * 13 matrix) initialized with 'U' --13x13 for virtual nodes
board = [['U' for j in range(13)] for i in range(13)]


# Function to fill in values for board
def initialize_board():
    for i in range(1, 12):
        board[i][0] = 'R'
        board[i][12] = 'R'
    board[0][1:12] = ['B'] * 11
    board[12][0:11] = ['B'] * 11
    board[0][0] = board[0][12] = board[12][0] = board[12][12] = 'O'  # virtual corners not required

# This function checks whether a new piece can be placed or not.
def is_valid_move(r, c):
    if 0 <= r < 11 and 0 <= c < 11 and board[r + 1][c + 1] == 'U':
        return True
    else:
        return False


rvals = [0, 1, 0, -1, -1, 1]
cvals = [-1, -1, 1, 1, 0, 0]


def check_in_range(x, y):
    if x < 0 or x > 12 or y < 0 or y > 12:
        return False
    return True


def get_connected_components(x, y):
    global board
    ret, color = [], board[x][y]
    for k in range(6):
        a, b = x + cvals[k], y + rvals[k]
        if check_in_range(a, b):
            if board[a][b] == color:
                ret.append((a, b))
    return ret


# This functions first checks for validity of new move and then update Board with new move.
def move(r, c, color):
    global board
    if is_valid_move(r, c):
        r, c = r + 1, c + 1
        board[r][c] = color
        conn_comps = get_connected_components(r, c)
        id0 = ds.calc_id(r, c)
        for cell in conn_comps:
            x, y = cell
            id1 = ds.calc_id(x, y)
            ds.merge(id0, id1)


# This function checks if any player is winning or not.
def check_winning():
    if ds.find_set(1, 156):
        return 'B'
    elif ds.find_set(13, 25):
        return 'R'
    return None

def print_board():
    # Only supported in python2 and not in python3
    global board
    space = 0
    for i in board:
        print space*' ',
        for j in i:
            print j,
        space+=1
        print
        
# This function drives the program and plays the game.
def main():
    global board
    initialize_board()

    reverse = False  # Var for storing swap rule implemented or not.
    
    player = p1
    color = 'R'
    x, y = player.move([i[1:-1] for i in board[1:-1]])  # For giving 11X11 matrix
    move(x, y, color)

    player = p2
    color = 'B'
    x, y = player.move([i[1:-1] for i in board[1:-1]])  # For giving 11X11 matrix

    # player 2 will return x='.' and y='.' for swap of moves i.e. (x,y) = ('.','.')
    if (x, y) == ('.', '.'):
        player = p1
        x, y = player.move([i[1:-1] for i in board[1:-1]])  # For giving 11X11 matrix
        reverse = True
    move(x, y, color)

    while not check_winning():
        if player == p1:
            player = p2
            color = 'B' if not reverse else 'R'
        elif player == p2:
            player = p1
            color = 'R' if not reverse else 'B'

        x, y = player.move([i[1:-1] for i in board[1:-1]])  # For giving 11X11 matrix
        move(x, y, color)

    print(check_winning())

main()
