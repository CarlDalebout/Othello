# File : Othello.py
# Location: Othello/Nathan
# Made by Carl and Nathan; Nathan's version

######################################################
# Libraries
######################################################
import bitstring # for bit array
import copy # for copy.deepcopy
import random # for randomness
import resource # for time

######################################################
# Helper Functions & Variables
######################################################
def gettime():
    rs = resource.getrusage(resource.RUSAGE_SELF)
    return rs[0] + rs[1]

DEBUGGING = False

######################################################
# Class: ColorBoard
# Used for representing  the location of the colored
# pieces of one of the players (white/black)
######################################################
class ColorBoard:
    def __init__(self, size=6):
        # initalize size of square color board
        self.__size = int(size)
        # length of bit array
        self.__len = self.__size * self.__size
        # initalize bit array to represent the sizexsize color board
        self.__board = bitstring.BitArray(length=self.__len)

    # generates 
    def getSpaces(self):
        for idx in range(self.__len):
            row,col = divmod(idx, self.__size)
            yield ((row, col), self.__board[idx])
            
    def duplicate(self):
        new_board = ColorBoard(self.__size)
        new_board.__board = self.__board.copy()
        return new_board

    # count the # of pieces in our color board
    # effectively counts the # of 1's in out bit array
    def count_items(self):
        return self.__board.count(True)

    # given that "space" is a tuple, (i, j), then
    # this method determines if that space
    # on our color board is occupied or not
    def is_occupied(self, space):
        row,col = space
        if not (0 <= row < self.__size and 0 <= col < self.__size):
            raise Exception("Given space does not exist in ColorBoard.")
        else:
            idx = row * self.__size + col
            return self.__board[idx]

    # sets space to either being occupied (value=1) or
    # unoccupied (value=0) by this color
    def set_space(self, space, value=1):
        row,col = space
        if not (0 <= row < self.__size and 0 <= col < self.__size):
            raise Exception("Given space does not exist in ColorBoard.")
        else:
            idx = row * self.__size + col
            self.__board[idx] = bool(value)

    # shifts bitboard
    def shift(self, direction=None):
        temp = self.duplicate()
        if direction is None:
            raise Exception("Error: no direction given in shift function.")
        elif direction in (0, 'up'):
            temp.__board <<= self.__size
        elif direction in (1, 'down'):
            temp.__board >>= self.__size
        elif direction in (2, 'left'):
            for i in range(self.__size):
                start = i * self.__size
                end = start + self.__size
                temp.__board[start:end] <<= 1
        elif direction in (3, 'right'):
            for i in range(self.__size):
                start = i * self.__size
                end = start + self.__size
                temp.__board[start:end] >>= 1
        elif direction in (4, 'not'):
            temp.__board.invert()
        else:
            raise Exception("Incorrect shift type, needs to be [0-4].")
        return temp
 
    # for printing color board
    def __str__(self):
        ret = ""
        for r in range(self.__size):
            ret += '+' + '-+'*self.__size + "\n"
            for c in range(self.__size):
                idx = r * self.__size + c
                ret += "|" + str(int(self.__board[idx]))
            ret += '|\n'
        ret += '+' + '-+'*self.__size
        return ret

######################################################
# Class: Board
# Used for modeling an Othello board; utilizes two
# ColorBoard instances, one for each players' pieces
######################################################
class Board:
    def __init__(self, size=6, fringe={}, closed_list=[], whiteBoard=None,blackBoard=None):  
        self.__size = int(size)
        self.whiteBoard = ColorBoard(self.__size)
        self.blackBoard = ColorBoard(self.__size)
    
        # set top left starting block for white
        self.whiteBoard.set_space((size // 2 - 1, size // 2 - 1), 1)
        # set bottom right starting block for white
        self.whiteBoard.set_space((size // 2, size // 2), 1)
    
        # set top right starting block for black
        self.blackBoard.set_space((size // 2 - 1, size // 2), 1)
        # set bottom left starting block for black
        self.blackBoard.set_space((size // 2, size // 2 - 1), 1)
    
        # keeps track of fringe (edges) around the pieces
        n = size
        # center squares
        s1, s2, s3, s4 = (
            (n // 2 - 1, n // 2 - 1),
            (n // 2, n // 2 - 1),
            (n // 2 - 1, n // 2),
            (n // 2, n // 2)
        )
        self.closed_list = [s1, s2, s3, s4]
        self.fringe = {}
        x0 = y0 = n // 2 - 1
        for x in range(0, n):
            for y in range(0, n):
                if x >= x0-1 and x < x0+3 and y >= y0-1 and y < y0+3 and (x, y) not in closed_list:
                    self.fringe[(x, y)] = True
    
        # delete four center squares from the fringe
        del self.fringe[s1]
        del self.fringe[s2]
        del self.fringe[s3]
        del self.fringe[s4]
          
    # checks if a space is available for playing
    def is_occupied(self, space):
        blackOccupied = self.blackBoard.is_occupied(space)
        whiteOccupied = self.whiteBoard.is_occupied(space)
        return blackOccupied or whiteOccupied

    # checks if a space is a valid move
    # returns a tuple: (is_move_valid, [list_of_tiles_to_flip_if_move_is_performed])
    def validate_move(self, space, color):
        row, col = space
        # if space is not on board, the move is not valid
        if row < 0 or row >= self.__size or col < 0 or col >= self.__size:
            return (False, None)
        # if space is already occupied, the move is not valid
        elif self.is_occupied(space):
            return (False, None)

        # ELSE: if move is on board and is not occupied,
        # then we now must determine if it meets the
        # other requirements of Othello for being a
        # valid move; namely, the newly placed piece
        # must sandwitch enemy piece(s), and in doing
        # so switch them to the current color

        # current player's board & opponent's board
        currentBoard = self.whiteBoard if color == 'W' else self.blackBoard
        opponentBoard = self.blackBoard if color == 'W' else self.whiteBoard

        is_valid = False
        pieces_to_flip = []

        #print("Checking validity...")
        # Check each direction for a valid move
        for direction in [
            (-1, 0),   # North
            (-1, 1),   # Northeast
            (0, 1),    # East
            (1, 1),    # Southeast
            (1, 0),    # South
            (1, -1),   # Southwest
            (0, -1),   # West
            (-1, -1)   # Northwest
        ]:
            i, j = space
            i += direction[0]
            j += direction[1]

            found_opponent = False
            pieces_to_flip_temp = []

            # Traverse in the given direction
            #print(0 <= i < self.__size, 0 <= j < self.__size)
            #print(i, j)
            while 0 <= i < self.__size and 0 <= j < self.__size:
                # check if the space is an opponent's piece
                if opponentBoard.is_occupied((i, j)):
                    found_opponent = True
                    pieces_to_flip_temp.append((i, j))
                elif currentBoard.is_occupied((i, j)):
                    # given that we've already found the opponent, then
                    # the prescence of our piece means this move is valid
                    if found_opponent:
                        pieces_to_flip.extend(pieces_to_flip_temp)
                        is_valid = True
                        break
                    # if we found our piece in the current direction,
                    # but we have not found an enemy piece yet, then
                    # there is no valid capture in this direction, so
                    # we stop searching this direction
                    else:
                        break
                # if the space is not occupied, then stop searching that direction
                else:
                    break

                # Move to the next position in the current direction
                i += direction[0]
                j += direction[1]

        if is_valid:
            return (True, pieces_to_flip)
        else:
            # if no valid capture was found, then return False by default
            return (False, None)

    def duplicate(self):
        return copy.deepcopy(self)
  
    # generates a list of actions
    # move1, move2, move3, etc.
    def actions(self, player):
        valid_moves = {}
        for move in self.fringe.keys():
            is_valid,pieces_to_flip = self.validate_move(move, player)
            
            if is_valid:
                valid_moves[move] = pieces_to_flip

        return valid_moves
  
    # generates list of available actions states
    # (move1, result_state1), (move2, result_state2), ...
    def successors(self, player):
        s = []

        # generate successor board state for each valid action
        for move in self.fringe.keys():
            # Step 1: Duplicate Board
            board = self.duplicate()
      
            # Step 2: Validate move
            is_valid,pieces_to_flip = board.validate_move(move, player)

            # Skip invalid moves!!!
            if not is_valid:
                continue

            # Step 3: Place Piece on new board
            if player == 'B':
                board.set_black(move)
            elif player == 'W':
                board.set_white(move)
            else:
                raise Exception("Player does not exist!")
    
            # Step 4: Flip Enemy Pieces
            for piece in pieces_to_flip:
                board.flip_piece(piece)
      
            # Step 5: Updated Closed List & Remove
            # placed piece from the fringe
            board.closed_list.append(move)
            del board.fringe[(move[0], move[1])]
      
            # Step 6: Update Fringe
            for x in range(move[0]-1, move[0]+2):
                for y in range(move[1]-1, move[1]+2):
                    if x > -1 and x < len(board) and y > -1 and y < len(board) and (x, y) not in board.fringe and (x, y) not in board.closed_list:
                        board.fringe[(x, y)] = True

            # Step 7: Yield Board State
            s.append((move, board))
        return s
      

    def flip_piece(self, space):
        if self.blackBoard.is_occupied(space):
            self.whiteBoard.set_space(space, 1)
            self.blackBoard.set_space(space, 0)
        elif self.whiteBoard.is_occupied(space):
            self.whiteBoard.set_space(space, 0)
            self.blackBoard.set_space(space, 1)
        else:
            raise Exception("Cannot flip piece of empty square!")

    # Precondition: space has already been validated as available and valid
    def set_white(self, space):
        self.whiteBoard.set_space(space)

    # Precondition: space has already been validated as available and valid
    def set_black(self, space):
        self.blackBoard.set_space(space)

    # returns size (dimensions) of board
    def __len__(self):
        return self.__size

    # determines if the space is on the fringe
    def is_in_fringe(self, space):
        return space in self.fringe and self.fringe[space]

    # prints board
    def __str__(self):
        # initalize result string
        ret = ""
        for i in range(self.__size):
            ret += '+' + '-+'*self.__size + "\n"
            for j in range(self.__size):
                if self.whiteBoard.is_occupied((i, j)):
                    ret += "|W"
                elif self.blackBoard.is_occupied((i, j)):
                    ret += "|B"
                elif DEBUGGING and self.is_in_fringe((i, j)):
                    ret += "|#"
                else:
                    ret += "| "
            ret += '|\n'
        ret += '+' + '-+'*self.__size + '\n'
        return ret


######################################################
# Class: Agent
# Used for modeling an entity that will "play moves"
# into an instance of the Board class
######################################################
class Agent:
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.pieces_to_flip = []

    # get the move that the agent will perform
    # for Player, this will be by input()
    # for AI, this will be by its algorithm
    # time_left is only used by AI
    def get_move(self, time_left):
        raise NotImplementedError

    # Precondition: move has already been validated
    def play_move(self, move):
        # Step 1: Place Piece
        if self.color == 'B':
            self.board.set_black(move)
        elif self.color == 'W':
            self.board.set_white(move)
        else:
            raise Exception("Player does not exist!")
        
        # Step 2: Flip Enemy Pieces
        for piece in self.pieces_to_flip:
            self.board.flip_piece(piece)

        # Step 3: Updated Closed List & Remove
        # placed piece from the fringe
        self.board.closed_list.append(move)
        del self.board.fringe[(move[0], move[1])]

        # Step 4: Update Fringe
        for x in range(move[0]-1, move[0]+2):
            for y in range(move[1]-1, move[1]+2):
                if x > -1 and x < len(self.board) and y > -1 and y < len(self.board) and (x, y) not in self.board.fringe and (x, y) not in self.board.closed_list:
                    self.board.fringe[(x, y)] = True
        

    def _str(self):
        return "<Agent %s>" % id(self)

######################################################
# Class: SearchNode
# Used for building a tree of nodes in the min-max
# algorihtm
######################################################
class SearchNode:
    def __init__(self, state, depth):
        self.state = state
        self.depth = depth

######################################################
# Heuristic Tables for the AI
######################################################
heuristic_table10x10 = [[100,   0,  8,  6,  2,  2,  6,  8,   0, 100],
                        [  0,   0,  6,  1,  1,  1,  1,  6,   0,   0],
                        [  8,   6,  1,  1,  1,  1,  1,  1,   6,   8],
                        [  6,   1,  1,  1,  1,  1,  1,  1,   1,   6],
                        [  2,   1,  1,  1,  3,  3,  1,  1,   1,   2],
                        [  2,   1,  1,  1,  3,  3,  1,  1,   1,   2],
                        [  6,   1,  1,  1,  1,  1,  1,  1,   1,   6],
                        [  8,   6,  1,  1,  1,  1,  1,  1,   6,   8],
                        [  0,   0,  1,  1,  1,  1,  1,  6,   0,   0],
                        [100,   0,  8,  6,  2,  2,  6,  8,   0, 100]]

heuristic_table8x8 = [[100,   0,  6,  2,  2,  6,   0, 100],
                      [  0,   0,  1,  1,  1,  1,   0,   0],
                      [  6,   1,  1,  1,  1,  1,   1,   6],
                      [  2,   1,  1,  3,  3,  1,   1,   2],
                      [  2,   1,  1,  3,  3,  1,   1,   2],
                      [  6,   1,  1,  1,  1,  1,   1,   6],
                      [  0,   0,  1,  1,  1,  1,   0,   0],
                      [100,   0,  6,  2,  2,  6,   0, 100]]

heuristic_table6x6 = [[100,   0,  6,  6,   0, 100],
                      [  0,   0,  1,  1,   0,   0],
                      [  6,   1,  3,  3,   1,   6],
                      [  6,   1,  3,  3,   1,   6],
                      [  0,   0,  1,  1,   0,   0],
                      [100,   0,  6,  6,   0, 100]]

heuristic_table4x4 = [[50,  0,  0, 50],
                      [ 0,  3,  3,  0],
                      [ 0,  3,  3,  0],
                      [50,  0, 0 , 50]]

######################################################
# Class: AI
# Used for modeling AIs that will make moves
# based on "board states" (instances of the Board class)
# and a defined set of heuristics
######################################################
class AI(Agent):
    def __init__(self, board, color):
        Agent.__init__(self, board, color)
        if len(board) == 4:
            self.h_table = heuristic_table4x4
        elif len(board) == 6:
            self.h_table = heuristic_table6x6
        elif len(board) == 8:
            self.h_table = heuristic_table8x8
        elif len(board) == 10:
            self.h_table = heuristic_table10x10


        # number of remaining moves needed
        # used for time scheduling purposes
        self.num_turns_left = (pow(len(board), 2) - 4) / 2
        self.turns_taken = 0


    # return heuristic value for the given space
    def h(self, space):
        return self.h_table[space[0]][space[1]]
        
    # score function
    # calculates a score for a player based on a given board state
    def score(self, state, color, h):
        s = 0

        if color == 'W':
            for space in state.whiteBoard.getSpaces():
                if space[1] == 1: s += h(space[0])
        else:
            for space in state.blackBoard.getSpaces():
                if space[1] == 1: s += h(space[0])

        return s

    # customizes min max for othello
    def min_max(self, max_depth):

        # s = search node (state, depth)
        # player = MIN/MAX
        # minMax = used for alpha-beta pruning
        def mm(s, player, minMax=None):
            # calculate successors
            o_color = "W" if self.color == "B" else "B"
            color = self.color if player == "MAX" else o_color
            successors = s.state.successors(color)
            
            # TERMINAL TEST
            # we reached max depth limit
            # OR there are no child states
            if (not (s.depth < max_depth)) or len(successors) == 0:
                # CALCULATE TERMINAL VALUE
                terminal_value = self.score(s.state, self.color, self.h)
                
                return (None, terminal_value)
            # ELIF do MAX
            elif player == "MAX":
                # initalized to small threshold ("infinitely small")
                # change as needed
                maxValue = -999999
                # action used to get to the max value
                # only important if this is initial call of abmm()
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
                # only important if this is initial call of abmm()
                minAction = None
                
                # determine MIN of the values at the next level in tree
                # if they are not terminal values, use MAX to determine
                # values for the nexxt layer's nodes
                for action,state in successors:
                    a = action
                    new_node = SearchNode(state=state, depth=s.depth+1)
                    v = mm(new_node, "MAX")[1]
                    
                    
                    # update current layer's MIN value
                    if v < minValue:
                        minValue = v
                        minAction = a
                
                    # perform alpha-beta pruning
                    if minMax != None and v < minMax:
                        break
                    
                return (minAction, minValue)
            
        # return value
        return mm(SearchNode(self.board, 0), "MAX")

    # get_move is the brain of the AI; largely based on minmax to make its decision
    # state = board
    # max_depth = how far to search
    # timeLeft = total time left for playing game
    def get_move(self, time_left):
        #print("AI is thinking...")
        # return none if board is full
        if self.num_turns_left == 0:
            return None
        # make a random move on first move
        # (only counts for black)
        elif self.turns_taken == 0 and self.color == 'B':
            cList = self.board.closed_list
            s1, s2, s3, s4 = (cList[0], cList[2], cList[1], cList[3])
            moves = [(s1[0]-1,s1[1]), (s1[0],s1[1]-1), (s4[0],s4[1]+1), (s4[0]+1, s4[1])]

            choice = random.choice(moves)
            validation = self.board.validate_move(choice, self.color)
            print("validation: ", validation)
            self.pieces_to_flip = validation[1]
            # we made a move!
            self.num_turns_left -= 1
            self.turns_taken += 1
            return choice

        # calculate how much time we can spend per turn on average
        buffer_time = 0.15
        time_per_turn = (time_left - buffer_time) / self.num_turns_left
        #print("Time left: ", time_left)
        #print("Turns Left: ", self.num_turns_left)
        #print("Time to spend per turn: ", self.time_per_turn)

        starttime = gettime()
        threshold_time = 0.75 * time_per_turn # when to stop searching
        for i in range(0, 5):
            result = self.min_max(i)
            currenttime = gettime()
            if (currenttime - starttime > threshold_time):
                break
        
        if result[0] != None:
            self.pieces_to_flip = self.board.validate_move(result[0], self.color)[1]
            # we made a move!
            self.num_turns_left -= 1
            self.turns_taken += 1
            return result[0]
        else:
            return None

    # Random Brain AI
    def get_random_move(self):
        choices = list(self.board.fringe.keys())
        move = random.choice(choices)

        while True:
            is_valid,pieces_to_flip = self.board.validate_move(move, self.color)

            if is_valid:
                self.pieces_to_flip = pieces_to_flip
                break
            else:
                choices.remove(move)
                move = random.choice(choices)

        return move

    def __str__(self):
        return "<AI %s>" % id(self)

class Game:
    def __init__(self, board_size):
        n = board_size
        self.board = Board(n)
        # black starts first
        self.__currentPlayer = 'B'
        self.black = AI(self.board, 'B')
        self.times = []
        self.white = AI(self.board, 'W')
        # how much time each player has left to think
        self.black_time = 6
        self.white_time = 6
        self.game_over = False
        self.winner = None

    def current_player(self):
        return self.__currentPlayer

    def show_board(self):
        print(self.board)

    def get_winner(self):
        # if there are still moves to play
        # that means game ended prematurely
        # because one of the players can't play,
        # in which that player loses
        if len(self.board.fringe) > 0:
            return 'Black' if self.__currentPlayer == 'W' else 'White'
        # else calculate points and return winner
        else:
            white_score = 0
            black_score = 0
            
            for space in self.board.whiteBoard.getSpaces():
                if space[1] == 1: white_score += 1
                
            for space in self.board.blackBoard.getSpaces():
                if space[1] == 1: black_score += 1

            if black_score > white_score:
                winner = 'B'
            elif white_score > black_score:
                winner = 'W'
            else:
                winner = None

            return (winner, white_score, black_score)
        

    def play_turn(self):
        if self.__currentPlayer == 'B':
            print("-----Black's Turn-----")
            starttime = gettime()
            move = self.black.get_move(self.black_time)
            endtime = gettime()
            self.black_time -= (endtime - starttime)
            self.times.append(endtime - starttime)
            print("Move: ", move)
            if move == None:
                self.game_over = True
                return
            self.black.play_move(move)
            self.__currentPlayer = 'W'
        else:
            print("-----White's Turn-----")
            starttime = gettime()
            move = self.white.get_move(self.white_time)
            endtime = gettime()
            self.white_time -= (endtime - starttime)
            self.times.append(endtime - starttime)
            print("Move: ", move)
            if move == None:
                self.game_over = True
                return
            self.white.play_move(move)
            self.__currentPlayer = 'B'

    def play_game(self):
        while not self.game_over:
            self.show_board()
            self.play_turn()

            print("Time: ", self.white_time, self.black_time)

        # else display winner!
        winner = self.get_winner()
        if type(winner) == str:
            print("Player %s won because the opponent couldn't move!" % winner)
        else:
            print("White scored %s points: " % winner[1])
            print("Black scored %s points: " % winner[2])
            print("Player %s won!" % winner[0])

        print("Average time taken each turn: ", sum(self.times)/len(self.times))

if __name__ == "__main__":
    print("Testing othello.py...")
    game = Game(6)
    game.play_game()
