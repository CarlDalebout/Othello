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

######################################################
# Function: get_board_state
# Used to generate a regular array board state
# for testing purposes, since that will be the
# input provided to our get_move method
######################################################
def get_array_board_state(board, n):
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
# Function: set_piece
######################################################
def set_piece(board, n, space, val):
    idx = space[0] * n + space[1]
    board[idx] = val

######################################################
# Function: play_move
######################################################
def play_move(board, n, player, brain, player_time, opponent_time):
    print("-----%s's Turn-----" % ("Black" if player == 'B' else "White"))

    # return remaining time
    remaining_time = player_time
    
    if brain == 'player':
        if len(get_actions(board, n, player)) == 0:
            return False
        row = int(input("row: "))
        col = int(input("col: "))

        while True:
            
            # validate move
            is_valid = is_valid_move(board, player, tuple_to_bit((row, col), n))

            if is_valid:
                break
            else:
                print("Invalid move. Try again.\n")
                row = int(input("row: "))
                col = int(input("col: "))
    elif brain == 'ai':
        print("AI is thinking...")
        board_state = get_array_board_state(board, n)
        val = get_move(n, board_state, player, player_time, opponent_time)
        if val == None:
            return False
        else:
            row,col = val[0]
            remaining_time = val[1]
            
        
    ##### Play Move on Board

    # Determine captured pieces
    pieces_to_flip = get_pieces_to_flip(board, player, tuple_to_bit((row, col), n))
    
    # Step 1: Place Piece
    player_color_board = board.black_board if player == 'B' else board.white_board
    opponent_color_board = board.white_board if player == 'B' else board.black_board
    set_piece(player_color_board, n, (row, col), 1)
    
    # Step 2: Flip Enemy Pieces
    opponent_color_board ^= pieces_to_flip
    player_color_board |= pieces_to_flip

    return remaining_time

# Tests:
# "bit shifting" --> tests masking and bit operations
# "board operations" --> tests is_valid_move, etc.
# "game" --> tests functional AI
TEST = "game"

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
    elif TEST == "game":
        n = None
        ns = None
        while n == None:
            n_input = int(input("n (6 or 8 or 10): "))
            if n_input == 6 or n_input == 8 or n_input == 10:
                n = n_input
                ns = n * n
            else:
                print("Bad input.")

        player_black = input("player1 (player/ai): ")
        player_white = input("player2 (player/ai): ")

        if (player_white != 'player' and player_white != 'ai') or (player_black != 'player' and player_black != 'ai'):
            raise Exception("Bad input. Players must be identified as 'player' or 'ai'.")

        # Initalize Board
        white_board = BitArray(uint=0, length=ns)
        black_board = BitArray(uint=0, length=ns)
        w1 = (n // 2 - 1, n // 2 - 1)
        w2 = (n // 2, n // 2)
        b1 = (n // 2 - 1, n // 2)
        b2 = (n // 2, n // 2 - 1)
        white_board[w1[0] * n + w1[1]] = 1
        white_board[w2[0] * n + w2[1]] = 1
        black_board[b1[0] * n + b1[1]] = 1
        black_board[b2[0] * n + b2[1]] = 1
        board = Board(size=n, white_board=white_board, black_board=black_board)

        # initalize players' time
        if n == 6:
            player_black_time = 6
            player_white_time = 6
        elif n == 8:
            player_black_time = 10
            player_white_time = 10
        elif n == 10:
            player_black_time = 16
            player_white_time = 16
            

        # play game
        turn = 'B'
        while True:
            current_player = player_black if turn == "B" else player_white
            print_board(board, n)
            flag = play_move(board, n, turn, current_player, player_black_time, player_white_time)
            if flag:
                if turn == 'B':
                    player_black_time = flag
                else:
                    player_white_time = flag
                turn = 'B' if turn == 'W' else 'W'
                print("Remaining Time: ", player_black_time, player_white_time)
            else:
                break

        print("Game over!")
        white_score = sum(board.white_board)
        black_score = sum(board.black_board)

        # Player could not move before game ended
        if white_score + black_score != ns:
            turn = "Black" if turn == "B" else "White"
            print("%s lost since they could not make a move." % turn)
        else:
            print("white_score: ", white_score)
            print("black_score: ", black_score)
            if white_score == black_score:
                print("It is a tie!")
            elif white_score > black_score:
                print("White wins!")
            else:
                print("Black wins!")
        
        
        
