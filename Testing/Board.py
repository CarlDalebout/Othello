import math
import copy

heuristic_table01010 = [[100,   0,  8,  6,  2,  2,  6,  8,   0, 100],
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
heuristic_table0108 = [[100,   0,  6,  2,  2,  6,   0, 100],
                       [  0,   0,  1,  1,  1,  1,   0,   0],
                       [  6,   1,  1,  1,  1,  1,   1,   6],
                       [  2,   1,  1,  3,  3,  1,   1,   2],
                       [  2,   1,  1,  3,  3,  1,   1,   2],
                       [  6,   1,  1,  1,  1,  1,   1,   6],
                       [  0,   0,  1,  1,  1,  1,   0,   0],
                       [100,   0,  6,  2,  2,  6,   0, 100]]

# first heuristics table for a 6x6 board
heuristic_table0106 = [[100,   0,  6,  6,   0, 100],
                       [  0,   0,  1,  1,   0,   0],
                       [  6,   1,  3,  3,   1,   6],
                       [  6,   1,  3,  3,   1,   6],
                       [  0,   0,  1,  1,   0,   0],
                       [100,   0,  6,  6,   0, 100]]

heuristic_table0104 = [[50,  0,  0, 50],
                       [ 0,  3,  3,  0],
                       [ 0,  3,  3,  0],
                       [50, 0 , 0 , 50]]
                       

class Board:
  def __init__(self, size=6):
    self.__size = size
    self.__board = [[' ' for r in range(size)] for c in range(size)]
    
    #setting white pieces
    self.__board[size // 2 - 1][size // 2 - 1] = "W"
    self.__board[size // 2    ][size // 2    ] = "W"

    #setting black pieces
    self.__board[size // 2 - 1][size // 2    ] = "B"
    self.__board[size // 2    ][size // 2 - 1] = "B"

    #setting closed list
    self.__closed_list = [
        (self.__size // 2 - 1, self.__size // 2 - 1),
        (self.__size // 2, self.__size // 2 - 1),
        (self.__size // 2 - 1, self.__size // 2),
        (self.__size // 2, self.__size // 2)
      ]

    self.__fringe = {}
    x0 = y0 = self.__size // 2 - 1
    for x in range(0, self.__size):
      for y in range(0, self.__size):
        if x >= x0-1 and x < x0+3 and y >= y0-1 and y < y0+3 and (x, y) not in self.__closed_list:
          self.__fringe[(x, y)] = True
          self.set_space((x,y), "#")

  def get_space(self, space):
    return self.__board[space[0]][space[1]]

  def set_space(self, space, color=' '):
    self.__board[space[0]][space[1]] = color
  
  def flip_space(self, space):
    if 'B' == self.get_space(space):
      self.set_space(space, 'W')
    elif 'W' == self.get_space(space):
      self.set_space(space, 'B')
    else:
      raise Exception("Cannot flip piece of empty square!")

  def is_occupied(self, space):
    return self.__board[space[0]][space[1]] != ' '

  def validate_move(self, space, color):
    if color == 'W':
      currentBoard = 'W' 
    elif color == 'B':
      currentBoard = 'B'
    
    if color == 'W':
      opponentBoard = 'B'
    elif color == 'B':
      opponentBoard = 'W'

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
      pieces_to_flip = []

      while(0 <= i < self.__size and 0 <= j < self.__size):
         # check if the space is an opponent's piece
        if opponentBoard == self.get_space((i, j)):
          found_opponent = True
          pieces_to_flip.append((i, j))
        elif currentBoard == self.get_space((i, j)):
          # given that we've already found the opponent, then
          # the prescence of our piece means this move is valid
          if found_opponent:
            return (True, pieces_to_flip)
          
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
      # if no valid capture was found, then return False by default
    return (False, None)

  def get_moves(self, color):
    valid_moves = {}
    for space in self.__fringe.keys():
      is_valid, pieces_to_flip = self.validate_move(space, color)
      
      if is_valid:
        valid_moves[space] = pieces_to_flip

    return valid_moves
    """
      private void calculateMoves() {
      legal = 0L;
      long potentialMoves;
      long currentBoard = getCurrentBoard();
      long opponentBoard = getOpponentBoard();
      long emptyBoard = emptyBoard();
      
      // UP
      potentialMoves = (currentBoard >> SIZE) & DOWN_MASK & opponentBoard;
      while (potentialMoves != 0L) {
          long tmp = (potentialMoves >> SIZE) & DOWN_MASK;
          legal |= tmp & emptyBoard;
          potentialMoves = tmp & opponentBoard;
      }


      // DOWN
      potentialMoves = (currentBoard << SIZE) & UP_MASK & opponentBoard;
      while (potentialMoves != 0L) {
          long tmp = (potentialMoves << SIZE) & UP_MASK;
          legal |= tmp & emptyBoard;
          potentialMoves = tmp & opponentBoard;
      }


      // LEFT
      potentialMoves = (currentBoard >> 1L) & RIGHT_MASK & opponentBoard;
      while (potentialMoves != 0L) {
          long tmp = (potentialMoves >> 1L) & RIGHT_MASK;
          legal |= tmp & emptyBoard;
          potentialMoves = tmp & opponentBoard;
      }
      // RIGHT
      potentialMoves = (currentBoard << 1L) & LEFT_MASK & opponentBoard;
      while (potentialMoves != 0L) {
          long tmp = (potentialMoves << 1L) & LEFT_MASK;
          legal |= tmp & emptyBoard;
          potentialMoves = tmp & opponentBoard;
      }
      // UP LEFT
      potentialMoves = (currentBoard >> (SIZE + 1L)) & RIGHT_MASK & DOWN_MASK & opponentBoard;
      while (potentialMoves != 0L) {
          long tmp = (potentialMoves >> (SIZE + 1L)) & RIGHT_MASK & DOWN_MASK;
          legal |= tmp & emptyBoard;
          potentialMoves = tmp & opponentBoard;
      }
      // UP RIGHT
      potentialMoves = (currentBoard >> (SIZE - 1L)) & LEFT_MASK & DOWN_MASK & opponentBoard;
      while (potentialMoves != 0L) {
          long tmp = (potentialMoves >> (SIZE - 1L)) & LEFT_MASK & DOWN_MASK;
          legal |= tmp & emptyBoard;
          potentialMoves = tmp & opponentBoard;
      }
      // DOWN LEFT
      potentialMoves = (currentBoard << (SIZE - 1L)) & RIGHT_MASK & UP_MASK & opponentBoard;
      while (potentialMoves != 0L) {
          long tmp = (potentialMoves << (SIZE - 1L)) & RIGHT_MASK & UP_MASK;
          legal |= tmp & emptyBoard;
          potentialMoves = tmp & opponentBoard;
      }
      // DOWN RIGHT
      potentialMoves = (currentBoard << (SIZE + 1L)) & LEFT_MASK & UP_MASK & opponentBoard;
      while (potentialMoves != 0L) {
          long tmp = (potentialMoves << (SIZE + 1L)) & LEFT_MASK & UP_MASK;
          legal |= tmp & emptyBoard;
          potentialMoves = tmp & opponentBoard;
      }
      moves.clear();

      Possible class route
#==================================================================================================================
    private MoveFinder[] finders = new MoveFinder[] {new UpFinder(), new DownFinder(), new LeftFinder(),
        new RightFinder(), new UpLeftFinder(), new UpRightFinder(), new DownLeftFinder(), new DownRightFinder()};

    private void calculateMoves() {
        legal = 0L;
        long potentialMoves;
        long currentBoard = getCurrentBoard();
        long opponentBoard = getOpponentBoard();
        long emptyBoard = emptyBoard();
        for (MoveFinder finder : finders) {
            potentialMoves = finder.next(currentBoard) & opponentBoard;
            while (potentialMoves != 0L) {
                long tmp = finder.next(potentialMoves);
                legal |= tmp & emptyBoard;
                potentialMoves = tmp & opponentBoard;
            }
        }
        moves.clear();
    }

    private interface MoveFinder {
        long next(long next);
    }

    private class UpFinder implements MoveFinder {
        @Override
        public long next(long n) {
            return (n >> SIZE) & DOWN_MASK;
        }
    }

    private class DownFinder implements MoveFinder {
        @Override
        public long next(long n) {
            return (n << SIZE) & UP_MASK;
        }
    }

    // and so on for the rest of the moves (LeftFinder, RightFinder, etc).

    """
  
  # Checks and updates the current board with the provided piece
  def play_move(self, space, color):
        
        validity, pieces_to_flip = self.validate_move(space, color)

        if validity:
          # Step 1: Place Piece
          self.set_space(space, color)
          
          # Step 2: Flip Enemy Pieces
          for piece in pieces_to_flip:
              self.flip_space(piece)

          # Step 3: Updated Closed List & Respace
          # placed piece from the fringe
          self.__closed_list.append(space)
          del self.__fringe[(space[0], space[1])]

          # Step 4: Update Fringe
          for x in range(space[0]-1, space[0]+2):
              for y in range(space[1]-1, space[1]+2):
                  if 0 <= x < len(self.__board) and 0 <= y < len(self.__board) and (x, y) not in self.__fringe and (x, y) not in self.__closed_list:
                      self.__fringe[(x, y)] = True
                      self.set_space((x,y), '#')

        else:
          print("Error Invalid move please provide valid move")
          row = int(input("Row:"))
          col = int(input("Col:"))
          self.play_move((row, col), color)

  # creates an instence of the board where the move has been played
  def make_move(self, space, color):
    board = copy.deepcopy(self)
    board.play_move(space, color)
    return board

  def score(self, color):
    white_score = 0
    black_score = 0
    
    for r, row in enumerate(self.__board):
      for c, col in enumerate(row):        
        if self.__size == 6:
          if col == "W":
            white_score += heuristic_table0106[r][c]
            # print("White:", heuristic_table0106[r][c])
          elif col == "B":
            black_score += heuristic_table0106[r][c]
            # print("Black:", heuristic_table0106[r][c])
        elif self.__size == 8:
          if col == "W":
            white_score += heuristic_table0108[r][c]
            # print("White:", heuristic_table0108[r][c])
          elif col == "B":
            black_score += heuristic_table0108[r][c]
            # print("Black:", heuristic_table0108[r][c])
        elif self.__size == 10:
          if col == "W":
            white_score += heuristic_table01010[r][c]
            # print("White:", heuristic_table01010[r][c])
          elif col == "B":
            black_score += heuristic_table01010[r][c]
            # print("Black:", heuristic_table01010[r][c])
        else:
          if col == "W":
            white_score += 1
            # print("White:", 1)
          elif col == "B":
            black_score += 1
            # print("Black:", 1)

    if color == "W":
      return white_score - black_score
    else:
      return black_score - white_score

  def __str__(self): 
    ret = ""
    line = self.__size * '+-' + '+\n'

    for row in self.__board:
        ret += line
        ret += '|' + ('|'.join([str(_) for _ in row])) + '|\n'

    ret += line
    return ret


def minMax(board, depth, Player = True, alpha = [None, -9999999], beta = [None, 99999999]):
  if depth == 0: # or whiteBoard & blackBoard = 2^size*size
    if Player:
      w = board.score("W")
      print("white:", w)
      return (None, w)
    else:
      b = board.score("B")
      print("Black:", b)
      return (None, b)
    
  if Player: # Max
    maximum = -99999999
    maximum_action = None
    for move in board.get_moves("W"):
      new_board = board.make_move(move, "W")
      action, value = minMax(new_board, depth-1, False, alpha, beta)
      if value > maximum:
          maximum = value
          maximum_action = [move, action]
      if maximum > alpha[1]:
          alpha[1] = maximum
          alpha[0] = maximum_action
      if beta[1] <= alpha[1]:
        break
    return (maximum_action, maximum)
  
  else: # Min
    minimum = 9999999999
    minimum_action = None
    for move in board.get_moves("B"):
      new_board = board.make_move(move, "B")
      action, value = minMax(new_board, depth-1, True, alpha, beta)
      if value < minimum:
        minimum = value
        minimum_action = [move, action]
      if minimum < beta[1]:
        beta[1] = minimum
        beta[0] = minimum_action
      if beta[1] <= alpha[1]:
        break
    return (minimum_action, minimum)


if __name__ == "__main__":
  # a = Board()
  # a.play_move((2, 1), "W")
  # print(a)
  # print(a.is_occupied((2, 2)))

  # a.set_space((0, 0,), 'W')
  # print(a)
  # score = a.score()
  # print("White Score:", score[0])
  # print("Black Score:", score[1])

  # a.set_space((0, 0,), 'B')
  # print(a)
  # score = a.score()
  # print("White Score:", score[0])
  # print("Black Score:", score[1])
  
  
  n = int(input("Size: "))
  a = Board(n)
  player = input("Player:")

  while(True):
    print("_____________________White Turn_________________")
    print(a)
    if player in ['W', 'w', 'White', 'white']:
      print(a.score("W"), a.score("B"))
      moves = a.get_moves("W")
      print(moves)
      if moves == {}:
        pass
      row = int(input("row: "))
      col = int(input("col: "))
      a.play_move((row, col), "W")
    else:
      print(a.score("W"), a.score("B"))
      moves = a.get_moves("W")
      print(moves)
      if moves == {}:
        pass
      actions, score = minMax(a, 4)
      print(actions, score) 
      print(actions[0]) 
      a.play_move((actions[0][0], actions[0][1]), "W")
    print("_____________________Black Turn_________________")
    print(a)
    if player in ['B', 'b', 'Black', 'black']:
      print(a.score("W"), a.score("B"))
      moves = a.get_moves("B")
      print(moves)
      if moves == {}:
        pass
      row = int(input("row: "))
      col = int(input("col: "))
      a.set_space((row, col,), "B")
    else:
      print(a.score("W"), a.score("B"))
      moves = a.get_moves("B")
      print(moves)
      if moves == {}:
        pass
      actions, score = minMax(a, 4, False)
      print(actions, score)
      print(actions[0]) 
      a.play_move((actions[0][0], actions[0][1]), "B")
