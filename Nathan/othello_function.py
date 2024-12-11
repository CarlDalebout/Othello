# File : Othello.py
# Location: Othello/Nathan
# Made by Carl and Nathan; Nathan's version

######################################################
# Libraries
######################################################
from bitstring import BitArray # for bit array
import copy # for copy.deepcopy
import random # for randomness
import resource # for time

######################################################
# Helper Functions & Variables
######################################################
MAX_DEPTH = 1
COLOR = 'B'

# first heuristics table for a 10x10 board
heuristic_table10x10 = [[100, -30,  8,  6,  2,  2,  6,  8, -30, 100],
                        [-30, -50,  6,  0,  0,  0,  0,  6, -50, -30],
                        [  8,   6,  0,  0,  0,  0,  0,  0,   6,   8],
                        [  6,   0,  0,  0,  0,  0,  0,  0,   0,   6],
                        [  2,   0,  0,  0,  3,  3,  0,  0,   0,   2],
                        [  2,   0,  0,  0,  3,  3,  0,  0,   0,   2],
                        [  6,   0,  0,  0,  0,  0,  0,  0,   0,   6],
                        [  8,   6,  0,  0,  0,  0,  0,  0,   6,   8],
                        [-30, -50,  0,  0,  0,  0,  0,  6, -50, -30],
                        [100, -30,  8,  6,  2,  2,  6,  8, -30, 100]]

# first heuristics table for a 8x8 board
heuristic_table8x8  = [[100, -30,  6,  2,  2,  6, -30, 100],
                       [-30, -50,  0,  0,  0,  0, -50, -30],
                       [  6,   0,  0,  0,  0,  0,   0,   6],
                       [  2,   0,  0,  3,  3,  0,   0,   2],
                       [  2,   0,  0,  3,  3,  0,   0,   2],
                       [  6,   0,  0,  0,  0,  0,   0,   6],
                       [-30, -50,  0,  0,  0,  0, -50, -30],
                       [100, -30,  6,  2,  2,  6, -30, 100]]

# first heuristics table for a 6x6 board
heuristic_table6x6  = [[100, -30,  6,  6, -30, 100],
                       [-30, -50,  0,  0, -50, -30],
                       [  6,   0,  3,  3,   0,   6],
                       [  6,   0,  3,  3,   0,   6],
                       [-30, -50,  0,  0, -50, -30],
                       [100, -30,  6,  6, -30, 100]]

# determine later
H_TABLE = None

def gettime():
    rs = resource.getrusage(resource.RUSAGE_SELF)
    return rs[0] + rs[1]

# takes a space as a tuple space=(i, j)
# and generates a bit array (int)
# that we can use for bit math
def tuple_to_bit(space, n):
    space_bit = BitArray(length=len(board))
    space_bit[space[0] * n + space[1]] = 1
    return space_bit

def bit_to_tuple(bit, n):
    # Ensure the bit is of correct length for an n x n board (n*n bits)
    if len(bit) != n * n:
        raise ValueError(f"Bit must be a {n}x{n} board (i.e., {n * n} bits).")

    # Iterate over the n*n bits to find the 1-bit
    for i in range(len(bit)):
        if bit[i] == 1:
            row = i // n 
            col = i % n  
            return (row, col)

    # If no 1-bit is found, return None
    print("No 1-bit found.")
    return None

def bit_to_tuple2(index, n):
    row = index // n
    col = index % n
    return (row, col)

# Mask to prevent wraparounds when shifting left
def LEFT_MASK(shift, board_size):
    return BitArray(uint=((1 << shift) - 1) << (board_size - shift), length=board_size)


# Mask to prevent wraparounds when shifting right
def RIGHT_MASK(shift, board_size):
    return BitArray(uint=(1 << shift) - 1, length=board_size)

# shifts a bit board
def shift(board, direction):
    n = len(board)
    if direction == 'W':  
        return (board << 1) & LEFT_MASK(1, n)
    elif direction == 'E': 
        return (board >> 1) & RIGHT_MASK(1, n) 
    elif direction == 'N': 
        return board << n
    elif direction == 'S': 
        return board >> n
    elif direction == 'NW':
        return (board << (n+1)) & LEFT_MASK(1, n) 
    elif direction == 'NE': 
        return (board << (n-1)) & RIGHT_MASK(1, n)
    elif direction == 'SW': 
        return (board >> (n-1)) & LEFT_MASK(1, n) 
    elif direction == 'SE': 
        return (board >> (n+1)) & RIGHT_MASK(1, n)

######################################################
# Function: print_board
######################################################
def print_board(board, n):
    # initalize result string
    ret = ""
    for i in range(n):
        ret += '+' + '-+'*n + "\n"
        for j in range(n):
            if is_occupied(board.white_board, n, (i, j)):
                ret += "|W"
            elif is_occupied(board.black_board, n, (i, j)):
                ret += "|B"
            else:
                ret += "| "
        ret += '|\n'
    ret += '+' + '-+'*n + '\n'
    print(ret)

######################################################
# Class: Board
# Used for storing board states
######################################################
class Board:
    def __init__(self, size=None, white_board=None,black_board=None):  
        self.__size = int(size)
        self.__white_board = white_board if white_board != None else BitArray(length=(self.__size*self.__size))
        self.__black_board = black_board if black_board != None else BitArray(length=(self.__size*self.__size))

    def get_white_board(self):
        return self.__white_board

    def get_black_board(self):
        return self.__black_board

    def set_white_board(self, board):
        self.__white_board = board

    def set_black_board(self, board):
        self.__black_board = board

    # define external properties
    white_board = property(get_white_board, set_white_board)
    black_board = property(get_black_board, set_black_board)

    def get_size(self):
        return self.__size
    
    def __len__(self):
        return self.__size * self.__size

######################################################
# Function: is_valid_move
# Used for determining the validity of a given move
# player = whose turn it is
# black_board, white_board = bit arrays modeling where the black/white pieces are
# move = bit array with a signle bit set for the move being checked
# n = board dimension
######################################################
def is_valid_move(board, player, move):
    black_board = board.black_board
    white_board = board.white_board
    n = board.get_size()
    
    # space is already taken 
    if move.uint & (black_board.uint | white_board.uint) != 0:
        return False

    directions = ['W', 'E', 'N', 'S', 'NW', 'NE', 'SW', 'SE']

    player_board = white_board if player == 'W' else black_board
    opponent_board = black_board if player == 'W' else white_board

    # walk in each direction (via shifting)
    # and see if the move is valid
    for direction in directions:
        # current space
        space = move
        # captured pieces
        captured = BitArray(uint=0, length=len(space))

        #print("initial space: ", bit_to_tuple(space, n))
        
        # keep searching until we validate the move as valid/invalid
        while True:
            print("Direction: ", direction)
            print("Space Before: ", space.bin)
            
            space = shift(space, direction)
            print("Space: ", space.bin)
            
            # found opponent
            if (space & opponent_board).uint != 0:
                captured |= space
            # found player
            elif (space & player_board).uint != 0:
                # if we've found pieces to capture, the move is valid!
                if captured.uint != 0:
                    return True  # Valid move if a bracket is found
                break
            else:
                break
    
    return False

######################################################
# Function: get_moves_to_flip
# Precondition: A move has been verified as valid
# Postcondition: Returns a list of spaces to flip
######################################################
def get_pieces_to_flip(board, player, move):
    black_board = board.black_board
    white_board = board.white_board
    n = board.get_size()
    
    # space is already taken 
    if move.uint & (black_board.uint | white_board.uint) != 0:
        return False

    directions = ['W', 'E', 'N', 'S', 'NW', 'NE', 'SW', 'SE']

    player_board = white_board if player == 'W' else black_board
    opponent_board = black_board if player == 'W' else white_board
    
    captured_pieces = BitArray(uint=0, length=len(board))

    for direction in directions:
        space = move
        captured = BitArray(uint=0, length=len(space))
    
        while True:
            space = shift(space, direction)
    
            if (space & opponent_board).uint != 0:
                captured |= space
            elif (space & player_board).uint != 0:
                if captured.uint != 0:
                    captured_pieces |= captured
                break
            else:
                break
    
    return captured_pieces


######################################################
# Function: set_space
# Postcondition: returns a new bit-array
######################################################
def set_space(board, n, space, value):
    idx = space[0] * n + space[1] 
    move_bit = BitArray(uint=value << idx, length=len(board)) 
    return board | move_bit

######################################################
# Function: is_occupied
######################################################
def is_occupied(board, n, space):
    idx = space[0] * n + space[1]
    return board[idx]

######################################################
# Function: set_piece
######################################################
def set_piece(board, n, space, val):
    idx = space[0] * n + space[1]
    board[idx] = val


######################################################
# Function: get_board_state
######################################################
def get_board_state(board, n):
    b = []
    for i in range(n):
        b.append([])
        for j in range(n):
            if is_occupied(board.white_board, n, (i, j)):
                b[i].append('W')
            elif is_occupied(board.black_board, n, (i, j)):
                b[i].append('B')
            else:
                b[i].append(' ')
    return b

######################################################
# Function: h --> heuristic
######################################################
def h(space, H_TABLE):
    return H_TABLE[space[0]][space[1]]

######################################################
# Function: score
# calculates a score for a player based on a given board state
######################################################
def score(state, color, h, H_TABLE):
    n = state.get_size()
    s = 0
    
    if color == 'W':
        for idx,bit in enumerate(state.white_board):
            i = idx // n
            j = idx % n
            if bit == 1: s += h((i, j), H_TABLE)
    else:
        for idx,bit in enumerate(state.black_board):
            i = idx // n
            j = idx % n
            if bit == 1: s += h((i, j), H_TABLE)
            
    return s

######################################################
# Class: SearchNode
######################################################
class SearchNode:
    def __init__(self, state, depth):
        self.state = state
        self.depth = depth

def extract_bits(bit_array):
    extracted = []
    for index, bit in enumerate(bit_array):
        if bit:
            single_bit_array = BitArray(uint=1 << (len(bit_array) - index - 1), length=len(bit_array))
            extracted.append(single_bit_array)
    return extracted
        
# TODO: valid moves
# Research: Maybe optimize this?
# Strategy
# FOR EACH DIRECTION:
#    new_opponent_board = Copy opponent's board and shift in that direction
#    new_opponent_board = new_opponent_board XOR (old_opponent_board | old_player_board)
#    fringe = new_opponent_board | fringe
# Filter fringe using is_valid_move() and return valid moves
def get_actions(board, n, current_player):
    # Step 1: Identify player and opponent boards
    player_board = board.white_board if current_player == 'W' else board.black_board
    opponent_board = board.black_board if current_player == 'W' else board.white_board
    occupied = player_board | opponent_board  # All occupied spaces

    # Step 2: Define directions
    directions = [
        -n, +n,  # North, South
        -1, +1,                   # West, East
        -n-1, -n+1, +n-1, +n+1  # NW, NE, SW, SE
    ]
    
    # Initialize valid moves
    valid_moves = BitArray(uint=0, length=len(player_board))

    # Step 3: Iterate over directions
    for direction in directions:
        if direction > 0:
            # Shift bits to the left for positive directions
            shifted = (opponent_board << direction) & ~LEFT_MASK(direction, n*n)
        else:
            # Shift bits to the right for negative directions
            shifted = (opponent_board >> -direction) & ~RIGHT_MASK(-direction, n*n)
    
        # Compute potential new moves
        potential_moves = shifted & ~occupied  # New positions must be unoccupied

        # Update valid moves
        valid_moves |= potential_moves

    # Step 4: Extract valid bits; array of bitarrays
    valid_bits = extract_bits(valid_moves)

    # Step 5: Filter valid moves using is_valid_move
    # Here you can refine valid_moves using your existing `is_valid_move()` method
    fringe = [b for b in valid_bits if is_valid_move(board, current_player, b)]
    
    return fringe

# returns a new board state
def perform_action(board, n, player, action):
    board = copy.deepcopy(board)
    player_color_board = board.black_board if player == 'B' else board.white_board
    opponent_color_board = board.white_board if player == 'B' else board.black_board
    
    # determine captured pieces
    pieces_to_flip = get_pieces_to_flip(board, player, action)

    # place move
    player_color_board |= action
    # flip enemy pieces
    opponent_color_board ^= pieces_to_flip
    player_color_board |= pieces_to_flip

    return board

# returns [(action1, board1), ...]
def get_successors(board, player):
    n = board.get_size()
    actions = get_actions(board, n, player)

    new_boards = []
    for action in actions:
        new_board = perform_action(board, n, player, action)
        new_boards.append((action, new_board))

    return new_boards
    

######################################################
# Function: min-max algorithm + alpha-beta pruning
######################################################
def mm(s, player, color, H_TABLE, minMax=None):
    # calculate successors
    o_color = "W" if color == "B" else "B"
    color = color if player == "MAX" else o_color
    successors = get_successors(s.state, color)

    # TERMINAL TEST
    # we reached max depth limit
    # OR there are no child states
    if (not (s.depth < MAX_DEPTH)) or len(successors) == 0:
        # CALCULATE TERMINAL VALUE
        terminal_value = score(s.state, COLOR, h, H_TABLE)
        
        return (None, terminal_value)
    # ELIF do MAX
    elif player == "MAX":
        # initalized to small threshold ("infinitely small")
        # change as needed
        maxValue = -999999
        # action used to get to the max value
        # only important if this is initial call of mm()
        maxAction = None
                
        # determine MAX of the values at the next level
        # if they are not terminal values, use MIN to determine
        # values for next layer's nodes
        for action,state in successors:
            # keep track of action used to get successor state
            a = action
            # pass current maxValue into minMax to use for
            # alpha-beta pruning at the next layer
            # returns value to check for current MAX layer
            new_node = SearchNode(state=state, depth=s.depth+1)
            
            v = mm(new_node, "MIN", color, H_TABLE, maxValue)[1]
            
            # update current layer's MAX value
            if v > maxValue:
                maxValue = v
                maxAction = a
                
            # perform alpha-beta pruning
            if minMax != None and v > minMax:
                break
                
        return (maxAction, maxValue)
    # ELSE do MIN
    else:
        # initalized to large threshold ("infinitely large")
        # change as needed
        minValue = 999999
        # action used to get the min value
        # only important if this is initial call of mm()
        minAction = None
        
        # determine MIN of the values at the next level in tree
        # if they are not terminal values, use MAX to determine
        # values for the next layer's nodes
        for action,state in successors:
            a = action
            new_node = SearchNode(state=state, depth=s.depth+1)
            v = mm(new_node, "MAX", color, H_TABLE, minValue)[1]
            
            
            # update current layer's MIN value
            if v < minValue:
                minValue = v
                minAction = a
                
            # perform alpha-beta pruning
            if minMax != None and v < minMax:
                break
                    
        return (minAction, minValue)

######################################################
# board_size = board_size(n)
# board_state = 2D array of 'W, 'B', ' '
# turn = color 'W' or 'B'
# time_left = time left (int) in milliseconds
# opponent_time_left = opponent's time left (int) in milliseconds
######################################################
def get_move(board_size, board_state, turn,
             time_left, opponent_time_left):
    # define heuristic table based on board size
    if board_size == 6:
        H_TABLE = heuristic_table6x6
    elif board_size == 8:
        H_TABLE = heuristic_table8x8
    elif board_size == 10:
        H_TABLE = heuristic_table10x10
    # create bitboards from board state
    ns = board_size * board_size # n-squared
    white_board = BitArray(length=ns)
    black_board = BitArray(length=ns)
    
    for row_idx, row in enumerate(board_state):
        for col_idx, item in enumerate(row):
            if item == 'W':
                white_board[row_idx*board_size + col_idx] = 1
            elif item == 'B':
                black_board[row_idx*board_size + col_idx] = 1                
    
    # Create Board from bit boards
    board = Board(size=board_size, white_board=white_board, black_board=black_board)
    
    # Determine Move:
    val = mm(SearchNode(board, 0), "MAX", turn, H_TABLE)[0]
    if val == None:
        print("TESTING ERROR: ")
        print("Testing actions: ")
        actions = get_actions(board, board_size, turn)
        for a in actions:
            print(a)
        print("Testing successors: ")
        successors = get_successors(board, turn)
        for s in successors:
            print_board(s, s.get_size())
    row,col = bit_to_tuple(val, board_size)

    # Return Move:
    return (row, col)

    
######################################################
# Function: play_move
######################################################
def play_move(board, n, player, brain, player_time, opponent_time):
    print("-----%s's Turn-----" % ("Black" if player == 'B' else "White"))
    
    if brain == 'player':
        row = int(input("row: "))
        col = int(input("col: "))

        while True:
            
            # validate move
            is_valid = is_valid_move(board, player, tuple_to_bit((row, col), n))

            if is_valid:
                pieces_to_flip = get_pieces_to_flip(board, player, tuple_to_bit((row, col), n))
                break
            else:
                print("Invalid move. Try again.\n")
                row = int(input("row: "))
                col = int(input("col: "))
    elif brain == 'ai':
        print("AI is thinking...")
        board_state = get_board_state(board, n)
        row,col = get_move(n, board_state, player, player_time, opponent_time )
        pieces_to_flip = get_pieces_to_flip(board, player, tuple_to_bit((row, col), n))
        
    ##### Play Move on Board
    
    # Step 1: Place Piece
    player_color_board = board.black_board if player == 'B' else board.white_board
    opponent_color_board = board.white_board if player == 'B' else board.black_board
    set_piece(player_color_board, n, (row, col), 1)
    
    # Step 2: Flip Enemy Pieces
    opponent_color_board ^= pieces_to_flip
    player_color_board |= pieces_to_flip
    

if __name__ == "__main__":
    print("Testing othello_function.py...")
    n = 6
    board = Board(size=n)
    # player time & opponent time
    player_time = 6
    opponent_time = 6

    # initalize board
    board.black_board = set_space(board.black_board, n, (2, 2), 1)
    board.black_board = set_space(board.black_board, n, (3, 3), 1)
    board.white_board = set_space(board.white_board, n, (2, 3), 1)
    board.white_board = set_space(board.white_board, n, (3, 2), 1)

    is_valid = is_valid_move(board, 'W', tuple_to_bit((1, 2), n))
    print_board(board, n)
    print(is_valid)
    input("Pause...")
    
    ## TESTING ##
    '''board_state = [
        [" ", "B", "B", "B", "B", "B", "B", "B"],
        ["B", "B", "B", "W", "B", "B", "B", "B"],
        ["B", "B", "W", "B", "W", "B", "W", "B"],
        ["B", "W", "W", "B", "B", "W", "W", "B"],
        ["B", "W", "B", "B", "W", "B", "W", "B"],
        ["B", "W", "B", "W", "W", "W", "W", "B"],
        ["B", "W", "W", "B", "B", "W", "W", "B"],
        ["B", "W", " ", " ", " ", " ", " ", " "]
    ]

    # create color boards
    for i,row in enumerate(board_state[::-1]):
        for j,item in enumerate(row[::-1]):
            if item == "B":
                board.black_board = set_space(board.black_board, n, (i, j), 1)
            elif item == "W":
                board.white_board = set_space(board.white_board, n, (i, j),1)'''

    # test game
    turn = 'W'
    while True:
        print_board(board, n)
        starttime = gettime()
        play_move(board, n, turn, 'ai', player_time, opponent_time)
        endtime = gettime()
        timespent = (endtime - starttime)
        # arbitrarily pick black as main player
        if turn == 'B':
            player_time -= timespent
        else:
            opponent_time -= timespent
        turn = 'B' if turn == 'W' else 'W'
        COLOR = turn

    
