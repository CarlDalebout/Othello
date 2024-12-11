"""
- All of the code in here is supplementary code to the othello.py file
- to help thoroughly test everything.
"""

######################################################
# Libraries
######################################################
from othello import *

######################################################
# Function: is_occupied
######################################################
def is_occupied(board, n, space):
    idx = space[0] * n + space[1]
    return board[idx]

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

# Tests: "bit shifting", "board operations", 
TEST = "board operations"

if __name__ == '__main__':
    print("Testing othello.py...")
    if TEST == "bit shifting":
        n = 6
        white_board = BitArray(bin='000000000000000100001000000000000000')
        black_board = BitArray(bin='000000000000001000000100000000000000')
        board = Board(size=n, white_board=white_board, black_board=black_board)
        print("-----Testing Masks-----")
        
        left_mask = LEFT_MASK(1, n)
        print("left_mask: ", left_mask.bin)
        right_mask = RIGHT_MASK(1, n)
        print("right_mask:", right_mask.bin)

        print("-----Testing Shifting-----")

        print_board(board, n)

        # Try for each direction: E/W/N/S/NW/NE/SW/SE
        print("original white_board:")
        new_board = white_board
        print(new_board.bin)
        for i in range(3):
            new_board = shift(new_board, 'SE', n)
            print(new_board.bin)
            b = Board(size=n, white_board=new_board, black_board=black_board)
            print_board(b, n)

    elif TEST == "board operations":
        n = 6
        white_board = BitArray(bin='000000000000000100001000000000000000')
        black_board = BitArray(bin='000000000000001000000100000000000000')
        board = Board(size=n, white_board=white_board, black_board=black_board)

        print_board(board, n)

        # Testing is_valid_move() and get_pieces_to_flip()
        print("-----Testing is_valid_move() and get_pieces_to_flip()-----")
        player = 'B'
        valid_moves = []
        for i in range(n):
            for j in range(n):
                tuple_move = (i, j)
                bit_move = tuple_to_bit(tuple_move, n)
                is_valid = is_valid_move(board, player, bit_move)
                if is_valid:
                    valid_moves.append(bit_move)

        for move in valid_moves:
            print("Testing Valid Moves for move (%s,%s)" % bit_to_tuple(move, n))
            pieces_to_flip = get_pieces_to_flip(board, player, move)
            print("Pieces captured: ")
            bits = extract_bits(pieces_to_flip)
            for captured_piece in bits:
                print(bit_to_tuple(captured_piece, n))

        # Testing get_actions()
        print("-----Testing get_actions()-----")
        actions = get_actions(board, n, player)
        for action in actions:
            print(bit_to_tuple(action, n))

        # Testing perform_action()
        print("-----Testing perform_action()-----")
        player = 'B'
        for action in actions:
            print("The result of action (%s,%s) is :" % bit_to_tuple(action, n))
            result = perform_action(board, n, player, action)
            print_board(result, n)

        # Testing get_successors()
        print("-----Testing get_successors()-----")
        player = 'B'
        successors = get_successors(board, player)
        for action,board_state in successors:
            print("The result of action (%s,%s) is :" % bit_to_tuple(action, n))
            print_board(board_state, n)
        
