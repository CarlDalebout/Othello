import bitstring as bitstring

import sys
sys.path.append('..')
sys.path.append('../board')
from board.Board import Board
from board.Board import ColorBoard




if __name__ == "__main__":
  a = Board()
  print(a)
  a.set_black((3,4))
  a.set_white((4,4))
  print(a.blackBoard)
  print(a.whiteBoard.shift('not'))