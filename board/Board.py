# File: Board.py
# Dir: Othello/board
# Author: Carl

# if "bitstring" is not working you will need to do "pip install bitstring"

from ColorBoard import ColorBoard


class Board:
  def __init__(self, size=6):
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

  # checks if a space is available for playing
  def is_occupied(self, space):
    blackOccupied = self.blackBoard.is_occupied(space)
    whiteOccupied = self.whiteBoard.is_occupied(space)
    return blackOccupied or whiteOccupied

  # checks if a space is a valid move
  def is_valid(self, space, color):
    row, col = space
    print("row, col: ", space)
    print("color: ", color)
    # if space is not on board, the move is not valid
    if row < 0 or row >= self.__size or col < 0 or col >= self.__size:
      return False
    # if space is already occupied, the move is not valid
    elif self.is_occupied(space):
      return False

    # ELSE: if move is on board and is not occupied,
    # then we now must determine if it meets the
    # other requirements of Othello for being a
    # valid move; namely, the newly placed piece
    # must sandwitch enemy piece(s), and in doing
    # so switch them to the current color

    # current player's board & opponent's board
    if color == 'W':
      currentBoard = self.whiteBoard 
    elif color == 'B':
      currentBoard = self.blackBoard
    
    if color == 'W':
      opponentBoard = self.blackBoard
    elif color == 'B':
      opponentBoard = self.whiteBoard

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
      #print("Checking direction: ", direction)
      i, j = space
      i += direction[0]
      j += direction[1]

      found_opponent = False

      # Traverse in the given direction
      #print(0 <= i < self.__size, 0 <= j < self.__size)
      #print(i, j)
      while 0 <= i < self.__size and 0 <= j < self.__size:
        # check if the space is an opponent's piece
        if opponentBoard.is_occupied((i, j)):
          found_opponent = True
        elif currentBoard.is_occupied((i, j)):
          # given that we've already found the opponent, then
          # the prescence of our piece means this move is valid
          if found_opponent:
            return True
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
    return False

  # given a valid move occurred, flip over enemy pieces
  def flip_pieces(self, space, color):
    # current player's board & opponent's board
    if color == 'W':
      currentBoard = self.whiteBoard
      opponentBoard = self.blackBoard
    elif color == 'B':
      currentBoard = self.blackBoard
      opponentBoard = self.whiteBoard
    
    # iterate over each direction
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
      #print("Checking direction: ", direction)
      i, j = space
      i += direction[0]
      j += direction[1]

      # found opponents
      # this is an array of tuples
      # representing the location
      # of found enemy pieces
      found_opponents = []

      # we want to set this to True if we find
      # a friendly piece after finding enemy pieces
      flip_pieces = False

      # Traverse in the given direction
      #print(0 <= i < self.__size, 0 <= j < self.__size)
      #print(i, j)
      while 0 <= i < self.__size and 0 <= j < self.__size:
        # check if the space is an opponent's piece
        if opponentBoard.is_occupied((i, j)):
          found_opponents.append((i, j))
        elif currentBoard.is_occupied((i, j)):
          # given that we've already found at least one opponent,
          # then set flip_pieces flag to true
          if len(found_opponents) > 0:
            flip_pieces = True
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

      # if we found pieces to flip, flip them!
      if flip_pieces:
        for piece in found_opponents:
          currentBoard.set_space(piece, 1)
          opponentBoard.set_space(piece, 0)

  # Precondition: space has already been validated as available and valid
  def set_white(self, space):
    self.whiteBoard.set_space(space, 1)

  # Precondition: space has already been validated as available and valid
  def set_black(self, space):
    self.blackBoard.set_space(space, 1)

  # returns size (dimensions) of board
  def __len__(self):
    return self.__size

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
        else:
          ret += "| "
      ret += '|\n'
    ret += '+' + '-+'*self.__size + '\n'
    return ret


if __name__ == '__main__':
  print("Testing Board.py...")
  board = Board(6)
  print(board)
  print(board.is_valid((2,2), 'B'))
  board.set_black((1, 2))
  print(board)
  board.flip_pieces((1, 2), 'B')
  print(board)
