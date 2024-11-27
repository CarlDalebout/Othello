import math

heuristic_table01010 = [[100, -30,  8,  6,  2,  2,  6,  8, -30, 100],
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
heuristic_table0108 = [[100, -30,  6,  2,  2,  6, -30, 100],
                       [-30, -50,  0,  0,  0,  0, -50, -30],
                       [  6,   0,  0,  0,  0,  0,   0,   6],
                       [  2,   0,  0,  3,  3,  0,   0,   2],
                       [  2,   0,  0,  3,  3,  0,   0,   2],
                       [  6,   0,  0,  0,  0,  0,   0,   6],
                       [-30, -50,  0,  0,  0,  0, -50, -30],
                       [100, -30,  6,  2,  2,  6, -30, 100]]

# first heuristics table for a 6x6 board
heuristic_table0106 = [[100, -30,  6,  6, -30, 100],
                       [-30, -50,  0,  0, -50, -30],
                       [  6,   0,  3,  3,   0,   6],
                       [  6,   0,  3,  3,   0,   6],
                       [-30, -50,  0,  0, -50, -30],
                       [100, -30,  6,  6, -30, 100]]

class Board:
  def __init__(self, size=6):
    self.__size = size
    self.__board = [[' ' for r in range(size)] for c in range(size)]
    
    self.__board[size // 2 - 1][size // 2 - 1] = "W"
    self.__board[size // 2    ][size // 2    ] = "W"

    self.__board[size // 2 - 1][size // 2    ] = "B"
    self.__board[size // 2    ][size // 2 - 1] = "B"
  
  def get_space(self, space):
    return self.__board[space[0]][space[1]]

  def set_space(self, space, color=' '):
    self.__board[space[0]][space[1]] = color

  def is_occupied(self, space):
    return self.__board[space[0]][space[1]] != ' '

  # [TODO] Need a way to create a list of moves a player can make at a given time
  def get_moves(self, color):
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
    pass
  
  def score(self):
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

    return (white_score, black_score)

  def __str__(self): 
    ret = ""
    line = self.__size * '+-' + '+\n'

    for row in self.__board:
        ret += line
        ret += '|' + ('|'.join([str(_) for _ in row])) + '|\n'

    ret += line
    return ret


def minMax(board, depth, alpha = -9999999, beta = 99999999, player = True):
  if depth == 0: # or whiteBoard & blackBoard = 2^size*size
    return board.eval()
  if player:
    maxEval = -999999999
    for move in board.getmoves("W"):
      eval = minMax(move, depth-1, alpha, beta, False)
      maxEval = max(maxEval, eval)
      alpha = max(alpha, eval)
      if beta <= alpha:
        break
    return maxEval
  
  else:
    minEval = 999999999
    for move in board.getmoves("B"):
      eval = minMax(move, depth-1, alpha, beta, True)
      minEval = min(minEval, eval)
      beta = min(beta, eval)
      if beta <= alpha:
        break
    return minEval


if __name__ == "__main__":
  # a = Board()
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

  b = Board(6)
  print(b)
  
  b.set_space((0, 0), "W")
  b.set_space((0, 1), "W")
  b.set_space((0, 2), "W")
  b.set_space((0, 3), "W")
  b.set_space((0, 4), "W")

  b.set_space((1, 0), "B")
  b.set_space((1, 1), "B")
  b.set_space((1, 2), "B")
  b.set_space((1, 3), "B")
  b.set_space((1, 4), "B")
  b.set_space((1, 5), "B")
  b.set_space((2, 0), "B")

  print(b)
  score = b.score()
  print("White Score:", score[0])
  print("Black Score:", score[1])