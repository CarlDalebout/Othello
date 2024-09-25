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

    directions = [
      (-1, 0),   # North
      (-1, 1),   # Northeast
      (0, 1),    # East
      (1, 1),    # Southeast
      (1, 0),    # South
      (1, -1),   # Southwest
      (0, -1),   # West
      (-1, -1)   # Northwest
    ]

  # checks if a space is available for playing
  def is_occupied(self, space):
    blackOccupied = self.blackBoard.is_occupied(space)
    whiteOccupied = self.whiteBoard.is_occupied(space)
    return blackOccupied or whiteOccupied

  # checks if a space is a valid move
  def is_valid(self, space, color):
    row, col = space
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
    currentBoard = self.whiteBoard if color == 'W' else self.blackBoard
    opponentBoard = self.blackBoard if color == 'W' else self.whiteBoard

    print("Checking validity...")
    # Check each direction for a valid move
    for direction in directions:
      print("Checking direction: ", direction)
      i, j = space
      i += direction[0]
      j += direction[1]

      found_opponent = False

      # Traverse in the given direction
      print(0 <= i < self.__size, 0 <= j < self.__size)
      print(i, j)
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

# class Board:  
#   def __init__(self, size = 6):
#     self.__size = int(size)
#     self.whiteBoard = bitstring.BitArray(int = 0, length=size*size)    # creating a bit array of size n*n for the white board
    
#     self.whiteBoard[size*(size//2-1) + size//2-1] = 1                  # setting the top left of the starting block
#     self.whiteBoard[size*(size//2) + size//2] = 1                      # setting the bottom right of the starting block

#     self.blackBoard = bitstring.BitArray(int = 0, length=size*size)    # creating a bit array of size n*n for the black board
    
#     self.blackBoard[size*(size//2-1) + size//2] = 1                    # setting the top right of the starting block
#     self.blackBoard[size*(size//2) + size//2-1] = 1                    # setting the bottom left of the starting block

#   def playWhite(self, row = None, col = None):
#     index = self.__size*row + col                                      # creating the index to manipulate based on the row and col

#     while self.blackBoard[index] == 1:                                 # Error check to prevent a space being placed on a already claimed black space
#       print("!!!ERROR!!! can not place piece there try again")
#       row = int(input("row: "))
#       col = int(input("col: "))
#       index = self.__size*row + col

#     self.whiteBoard[index] = 1                                         # Setting bit to 1 
  
#   def printWhite(self):
#     ret = ""
#     for i in range(self.__size):
#       ret += '+' + '-+'*self.__size + "\n"
#       for j in range(self.__size):
#         if self.whiteBoard[i*self.__size + j] == 1: ret += "|W"
#         else: ret += "| "
#       ret += '|\n'
#     ret += '+' + '-+'*self.__size + '\n'
#     return ret


#   def playBlack(self, row = None, col = None):
#     index = self.__size*row + col                                      # creating the index to manipulate based on the row and col
    
#     while self.whiteBoard[index] == 1:                                 # Error check to prevent a space being placed on a already claimed black space
#       print("!!!ERROR!!! can not place piece there try again")
#       row = int(input("row: "))
#       col = int(input("col: "))
#       index = self.__size*row + col

#     self.blackBoard[index] = 1                                         # Setting bit to 1

#   def printBlack(self):
#     ret = ""
#     for i in range(self.__size):
#       ret += '+' + '-+'*self.__size + "\n"
#       for j in range(self.__size):
#         if self.whiteBoard[i*self.__size + j] == 1: ret += "|W"
#         else: ret += "| "
#       ret += '|\n'
#     ret += '+' + '-+'*self.__size + '\n'
#     return ret

#   def __len__(self):
#     return self.__size

#   def __str__(self):
#     ret = ""
#     for i in range(self.__size):
#       ret += '+' + '-+'*self.__size + "\n"
#       for j in range(self.__size):
#         if self.whiteBoard[i*self.__size + j] == 1: ret += "|W"
#         elif self.blackBoard[i*self.__size + j] == 1: ret += "|B"
#         else: ret += "| "
#       ret += '|\n'
#     ret += '+' + '-+'*self.__size + '\n'
#     return ret
