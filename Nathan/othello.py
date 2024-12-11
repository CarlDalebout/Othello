######################################################
######################################################
######################################################
# File: Othello.py
# Authors: Nathan Cochran and Carl Dalebout
# Purpose: Provides a get_move() method, acting as an
#          AI, that takes a board state and outputs a
#          logical move
######################################################
######################################################
######################################################

######################################################
# Libraries
######################################################
from bitstring import BitArray
import copy
import random
import resource
import math

######################################################
# Helper Functions
######################################################
# Generates a timestamp
def gettime():
    rs = resource.getrusage(resource.RUSAGE_SELF)
    return rs[0] + rs[1]

# (i, j) --> BitArray
def tuple_to_bit(space, n):
    space_bit = BitArray(length=n*n)
    space_bit[space[0] * n + space[1]] = 1
    return space_bit

# BitArray --> (i, j)
def bit_to_tuple(bit, n):
    if len(bit) != n * n:
        raise ValueError(f"Bit must be a {n}x{n} board (i.e., {n * n} bits).")

    for i in range(len(bit)):
        if bit[i] == 1:
            row = i // n 
            col = i % n  
            return (row, col)

    print("No 1-bit found.")
    return None

# Index of Bit Position --> (i, j)
def bit_to_tuple2(index, n):
    row = index // n
    col = index % n
    return (row, col)

# Mask to prevent wraparounds when shifting left
def LEFT_MASK(shift, board_size):
    return BitArray(uint=((1 << (board_size - shift)) - 1) << shift, length=board_size)*board_size

# Mask to prevent wraparounds when shifting right
def RIGHT_MASK(shift, board_size):
    return BitArray(uint=(1 << (board_size - shift)) - 1, length=board_size)*board_size

# Shifts a bit board towards a specific direction
# board = bitarray for color board (white/black)
# direction = W/E/N/S/NW/NE/SW/SE
# n = board_size
def shift(board, direction, n):
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

# Used for extract single (one) bit arrays
# from a bit array full of 1's
def extract_bits(bit_array):
    extracted = []
    for index, bit in enumerate(bit_array):
        if bit:
            single_bit_array = BitArray(uint=1 << (len(bit_array) - index - 1), length=len(bit_array))
            extracted.append(single_bit_array)
    return extracted

######################################################
# Heuristic Tables
######################################################
heuristic_table10x10= [[100,   0,  8,  6,  2,  2,  6,  8,   0, 100],
                       [  0,   0,  6,  1,  1,  1,  1,  6,   0,   0],
                       [  8,   6,  1,  1,  1,  1,  1,  1,   6,   8],
                       [  6,   1,  1,  1,  1,  1,  1,  1,   1,   6],
                       [  2,   1,  1,  1,  3,  3,  1,  1,   1,   2],
                       [  2,   1,  1,  1,  3,  3,  1,  1,   1,   2],
                       [  6,   1,  1,  1,  1,  1,  1,  1,   1,   6],
                       [  8,   6,  1,  1,  1,  1,  1,  1,   6,   8],
                       [  0,   0,  1,  1,  1,  1,  1,  6,   0,   0],
                       [100,   0,  8,  6,  2,  2,  6,  8,   0, 100]]

# first heuristics table for a 8x8 board
heuristic_table8x8 = [[100,   0,  6,  2,  2,  6,   0, 100],
                      [  0,   0,  1,  1,  1,  1,   0,   0],
                      [  6,   1,  1,  1,  1,  1,   1,   6],
                      [  2,   1,  1,  3,  3,  1,   1,   2],
                      [  2,   1,  1,  3,  3,  1,   1,   2],
                      [  6,   1,  1,  1,  1,  1,   1,   6],
                      [  0,   0,  1,  1,  1,  1,   0,   0],
                      [100,   0,  6,  2,  2,  6,   0, 100]]

# first heuristics table for a 6x6 board
heuristic_table6x6 = [[100,   0,  6,  6,   0, 100],
                      [  0,   0,  1,  1,   0,   0],
                      [  6,   1,  3,  3,   1,   6],
                      [  6,   1,  3,  3,   1,   6],
                      [  0,   0,  1,  1,   0,   0],
                      [100,   0,  6,  6,   0, 100]]

######################################################
######################################################
######################################################
# BOARD LOGIC
######################################################
######################################################
######################################################

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
#   - player = whose turn it is
#   - board = board state
#   - black_board, white_board = bit arrays modeling where the black/white pieces are
#   - move = bit array with a single bit set for the move being checked
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
        
        # keep searching until we validate the move as valid/invalid
        while True:
            space = shift(space, direction, n)
            
            # found opponent
            if (space & opponent_board).uint != 0:
                captured |= space
            # found player
            elif (space & player_board).uint != 0:
                # if we've found pieces to capture, the move is valid!
                if captured.uint != 0:
                    return True
                break
            else:
                break
    
    return False

######################################################
# Function: get_moves_to_flip
# Precondition: A move has been verified as valid
# Postcondition: Returns a list of spaces to flip
# Note: returns a bitarray where a 1 indicates a space
# should be flipped
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
            space = shift(space, direction, n)
    
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
# Function: get_actions
# Returns a list of valid moves, given a board state
# Strategy:
# FOR EACH DIRECTION:
#    new_opponent_board = Copy opponent's board and shift in that direction
#    new_opponent_board = new_opponent_board XOR (old_opponent_board | old_player_board)
#    fringe = new_opponent_board | fringe
# Filter fringe using is_valid_move() and return valid moves
######################################################
def get_actions(board, n, current_player):
    # Step 1: Identify player and opponent boards
    player_board = board.white_board if current_player == 'W' else board.black_board
    opponent_board = board.black_board if current_player == 'W' else board.white_board
    # All occupied spaces
    occupied = player_board | opponent_board

    
    directions = ['W', 'E', 'N', 'S', 'NW', 'NE', 'SW', 'SE']
    
    # Initialize valid moves
    valid_moves = BitArray(uint=0, length=len(player_board))

    # Step 3: Iterate over directions
    for direction in directions:
        shifted = shift(opponent_board, direction, n)
    
        # Compute potential new moves
        # (must be unoccupied: ~occupied)
        potential_moves = shifted & ~occupied

        # Update valid moves
        valid_moves |= potential_moves

    # Step 4: Extract valid bits; array of bitarrays
    valid_bits = extract_bits(valid_moves)

    # Step 5: Filter valid moves using is_valid_move
    # Here you can refine valid_moves using your existing `is_valid_move()` method
    fringe = [b for b in valid_bits if is_valid_move(board, current_player, b)]
    
    return fringe

######################################################
# Function: perform_action
# Performs an action on a board state, returning a
# new board state
######################################################
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

######################################################
# Function: get_successors
# returns [(action1, board1), ...]
######################################################
def get_successors(board, player):
    n = board.get_size()
    actions = get_actions(board, n, player)

    new_boards = []
    for action in actions:
        new_board = perform_action(board, n, player, action)
        new_boards.append((action, new_board))

    return new_boards


######################################################
######################################################
######################################################
# BRAIN OF THE AI
######################################################
######################################################
######################################################

######################################################
# Class: SearchNode
# Used for generating min-max search tree
######################################################
class SearchNode:
    def __init__(self, state, depth):
        self.state = state
        self.depth = depth

######################################################
# Function: h --> heuristic
######################################################
def h(space, H_TABLE):
    return H_TABLE[space[0]][space[1]]

######################################################
# Function: score
# Calculates a score for a player based on a given
# board state
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
# Function: min_max
# Creates a custom min_max algorithm for the
# othello problem
######################################################
def min_max(BOARD, COLOR, H_TABLE, MAX_DEPTH):
    def mm(s, player, minMax=None):
        # calculate successors
        o_color = "W" if COLOR == "B" else "B"
        color = COLOR if player == "MAX" else o_color
        successors = get_successors(s.state, COLOR)

        # TERMINAL TEST
        # we reached max depth limit
        # OR there are no child states
        if (not (s.depth < MAX_DEPTH)) or len(successors) == 0:
            # CALCULATE TERMINAL VALUE
            if len(successors) == 0:
                # this accounts for scenarios where the player
                # wants to avoid making moves that would make them
                # lose because they can't make moves later on
                terminal_value = -99999 if player == "MAX" else 99999
            else:
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
                
                v = mm(new_node, "MIN", maxValue)[1]
                
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
                v = mm(new_node, "MAX", minValue)[1]
                
                
                # update current layer's MIN value
                if v < minValue:
                    minValue = v
                    minAction = a
                    
                # perform alpha-beta pruning
                if minMax != None and v < minMax:
                    break
                    
            return (minAction, minValue)
        
    # return customized min max algorithm
    return mm(SearchNode(state=BOARD, depth=0), "MAX")


######################################################
# board_size = board_size(n)
# board_state = 2D array of 'W, 'B', ' '
# turn = color 'W' or 'B'
# time_left = time left (int) in milliseconds
# opponent_time_left = opponent's time left (int) in milliseconds
######################################################
def get_move(board_size, board_state, turn,
             time_left, opponent_time_left):
    
    # 1. Define heuristic table based on board size
    if board_size == 6:
        H_TABLE = heuristic_table6x6
    elif board_size == 8:
        H_TABLE = heuristic_table8x8
    elif board_size == 10:
        H_TABLE = heuristic_table10x10
        
    # 2. Create bitboards from board state
    ns = board_size * board_size # n-squared
    white_board = BitArray(length=ns)
    black_board = BitArray(length=ns)
    total_moves = 0
    
    for row_idx, row in enumerate(board_state):
        for col_idx, item in enumerate(row):
            if item == 'W':
                white_board[row_idx*board_size + col_idx] = 1
                total_moves += 1
            elif item == 'B':
                black_board[row_idx*board_size + col_idx] = 1
                total_moves += 1
    
    # 3. Create board from color bit boards
    board = Board(size=board_size, white_board=white_board, black_board=black_board)

    # 4. Determine Time for Turn
    turns_to_take = math.ceil((ns - total_moves) / 2)
    if turns_to_take == 0:
        return None
    # leave some extra buffer time
    buffer_time = time_left * 0.2
    # multiply by 0.8 to give a little buffer per turn as well,
    # because iterative deepening will often cause overflow
    time_per_turn = ((time_left - buffer_time) / turns_to_take) * 0.75

    # 5. Determine move
    # use iterative deepening until time runs out
    start_time = gettime()
    spent_time = 0
    for MAX_DEPTH in range(1, 10):
        val = min_max(board, turn, H_TABLE, MAX_DEPTH)[0]
        end_time = gettime()
        spent_time = end_time - start_time
        if spent_time > time_per_turn:
            break
        
    
    if val == None:
        return None
    else:   
        row,col = bit_to_tuple(val, board_size)
        # IMPORTANT! CHANGE FOR SUBSMISSION TO THE FOLLOWING:
        # return (row, col)
        return ((row, col), time_left - spent_time)
