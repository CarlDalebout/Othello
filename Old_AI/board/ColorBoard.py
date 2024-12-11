# File : ColorBoard.py
# Location: Othello/board

import bitstring
import copy
import unittest

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
    self.__board = bitstring.BitArray(length=self.__len)

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

class TestColorBoardShift(unittest.TestCase):
    def setUp(self):
        """Initialize a 4x4 board for testing."""
        self.board = ColorBoard(4)
        # Set some initial positions for testing shifts
        self.board.set_space((0, 0), 1)
        self.board.set_space((1, 1), 1)
        self.board.set_space((2, 2), 1)
        self.board.set_space((3, 3), 1)

    def test_shift_up(self):
        """Test shifting the board up."""
        shifted = self.board.shift(0)
        self.assertTrue(shifted.is_occupied((0, 1)))
        self.assertTrue(shifted.is_occupied((1, 2)))
        self.assertTrue(shifted.is_occupied((2, 3)))
        self.assertFalse(shifted.is_occupied((3, 3)))

    def test_shift_down(self):
        """Test shifting the board down."""
        shifted = self.board.shift(1)
        self.assertTrue(shifted.is_occupied((1, 0)))
        self.assertTrue(shifted.is_occupied((2, 1)))
        self.assertTrue(shifted.is_occupied((3, 2)))
        self.assertFalse(shifted.is_occupied((0, 0)))

    def test_shift_left(self):
        """Test shifting the board left."""
        shifted = self.board.shift(2)
        self.assertTrue(shifted.is_occupied((1, 0)))
        self.assertTrue(shifted.is_occupied((2, 1)))
        self.assertTrue(shifted.is_occupied((3, 2)))
        self.assertFalse(shifted.is_occupied((0, 0)))

    def test_shift_right(self):
        """Test shifting the board right."""
        shifted = self.board.shift(3)
        self.assertTrue(shifted.is_occupied((0, 1)))
        self.assertTrue(shifted.is_occupied((1, 2)))
        self.assertTrue(shifted.is_occupied((2, 3)))
        self.assertFalse(shifted.is_occupied((0, 0)))

    def test_shift_not(self):
        """Test flipping all bits on the board."""
        shifted = self.board.shift(4)
        self.assertFalse(shifted.is_occupied((0, 0)))
        self.assertFalse(shifted.is_occupied((1, 1)))
        self.assertFalse(shifted.is_occupied((2, 2)))
        self.assertFalse(shifted.is_occupied((3, 3)))
        self.assertTrue(shifted.is_occupied((0, 1)))  # Previously unoccupied

if __name__ == '__main__':
    unittest.main()
  
'''if __name__ == '__main__':
  print('Testing ColorBoard.py...')
  n = int(input('n: '))
  colorBoard = ColorBoard(n)
  print(colorBoard)
  
  #colorBoard.set_space((0, 0), 1)
  #print(colorBoard.is_occupied((-1, 0)))
  #print(colorBoard.is_occupied((1, 1)))
  #print(colorBoard)
'''
