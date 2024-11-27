# File : ColorBoard.py
# Location: Othello/board

import bitstring
import copy

#####################################################
# Class: ColorBoard
# Used for representing where the colored pieces
# of one of the players (white/black) is located
#####################################################
class ColorBoard:
  def __init__(self, size=6):
    # initalize size of square color board
    self.__size = int(size)
    # length of bit array
    self.__len = self.__size * self.__size
    # initalize bit array to represent the sizexsize color board
    self.__board = [bitstring.BitArray(int=0, length=self.__size) for s in range(self.__size)]

    
  def duplicate(self):
    new_board = ColorBoard(self.__size)
    new_board.__board = [b.copy() for b in self.__board]
    return new_board

  # count the # of pieces in our color board
  # effectively counts the # of 1's in out bit array
  def count_items(self):
    count = 0
    for item in self.__board:
      if item == 1: count += 1
    return count

  # given that "space" is a tuple, (i, j), then
  # this method determines if that space
  # on our color board is occupied or not
  def is_occupied(self, space):
    row = space[0]
    col = space[1]
    if not (0 <= row < self.__size and 0 <= col < self.__size):
      raise Exception("Given space does not exist in ColorBoard.")
    else:
      return self.__board[row][col] == 1

  # sets space to either being occupied (value=1) or
  # unoccupied (value=0) by this color
  def set_space(self, space, value = 1):
    row = space[0]
    col = space[1]
    if not (0 <= row < self.__size and 0 <= col < self.__size):
      raise Exception("Given space does not exist in ColorBoard.")
    else:
      self.__board[row][col] = value

  # shift the current bits based on the value given
  # up = 0, down = 1, left = 2, right = 3, not = 4
  def shift(self, direction = None):
    temp = copy.deepcopy(self)
    if direction == None:
      raise Exception("Error no dirrection given in shift function.")
    else:
      match direction:
        case 0: # up
          for row in range(len(temp.__board)-1):
            temp.__board[row] = temp.__board[row+1]
          temp.__board[len(temp.__board)-1] = bitstring.BitArray(int=0, length=self.__size)
        case 'up':
          for row in range(len(temp.__board)-1):
            temp.__board[row] = temp.__board[row+1]
          temp.__board[len(temp.__board)-1] = bitstring.BitArray(int=0, length=self.__size)
        
        case 1: # down
          for row in range(len(temp.__board)-1, 0, -1):
            temp.__board[row] = temp.__board[row-1]
          temp.__board[0] = bitstring.BitArray(int=0, length=self.__size)
        case 'down':
          for row in range(len(temp.__board)-1, 0, -1):
            temp.__board[row] = temp.__board[row-1]
          temp.__board[0] = bitstring.BitArray(int=0, length=self.__size)
        
        case 2: # left
          for row in range(len(temp.__board)):
            temp.__board[row] <<= 1
        case 'left':
          for row in range(len(temp.__board)):
            temp.__board[row] <<= 1
        
        case 3: # right
          for row in range(len(temp.__board)):
            temp.__board[row] >>= 1
        case 'right':
          for row in range(len(temp.__board)):
            temp.__board[row] >>= 1
        
        case 4: # not
          for row in range(len(temp.__board)):
            temp.__board[row].invert()
        case 'not':
          for row in range(len(temp.__board)):
            temp.__board[row].invert()

        case _: # default
          raise Exception("incorrect shift type needs to be [0-4]")
      return temp
 
  # for printing color board
  def __str__(self):
    ret = ""
    for r in range(self.__size):
      ret += '+' + '-+'*self.__size + "\n"
      for c in range(self.__size):
        ret += "|" + str(int(self.__board[r][c]))
      ret += '|\n'
    ret += '+' + '-+'*self.__size
    return ret

if __name__ == '__main__':
  print('Testing ColorBoard.py...')
  n = int(input('n: '))
  colorBoard = ColorBoard(n)
  print(colorBoard)
  colorBoard.set_space((0, 0), 1)
  print(colorBoard.is_occupied((-1, 0)))
  print(colorBoard.is_occupied((1, 1)))
  print(colorBoard)
