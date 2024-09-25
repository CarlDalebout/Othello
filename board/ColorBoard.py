# File : ColorBoard.py
# Location: Othello/board

import bitstring

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
    self.__board = bitstring.BitArray(int=0, length=self.__len)

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
    index = self.__size*row + col
    if index < 0 or index > self.__len:
      raise Exception("Given space does not exist in ColorBoard.")
    else:
      return self.__board[index] == 1

  # sets space to either being occupied (value=1) or
  # unoccupied (value=0) by this color
  def set_space(self, space, value):
    row = space[0]
    col = space[1]
    index = self.__size*row + col
    if index < 0 or index > self.__len:
      raise Exception("Given space does not exist in ColorBoard.")
    else:
      self.__board[index] = value

  # for printing color board
  def __str__(self):
    ret = ""
    for i in range(self.__size):
      ret += '+' + '-+'*self.__size + "\n"
      for j in range(self.__size):
        if self.__board[i*self.__size + j] == 1:
          ret += "|W"
        else:
          ret += "| "
      ret += '|\n'

    ret += '+' + '-+'*self.__size
    return ret

    # for printing color board
    def print(self):
      print(self)

if __name__ == '__main__':
  print('Testing ColorBoard.py...')
  colorBoard = ColorBoard(5)
  colorBoard.set_space((0, 0), 1)
  print(colorBoard.is_occupied((0, 0)))
  print(colorBoard.is_occupied((1, 1)))
  print(colorBoard)