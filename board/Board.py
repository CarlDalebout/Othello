# File: Board.py
# Dir: Othello/board
# Author: Carl

# if "bitstring" is not working you will need to do "pip install bitstring"

import sys
from ColorBoard import ColorBoard
sys.path.append('..')
import GLOBALS as g

class Board:
  def __init__(self, size=6, fringe={}, closed_list=[], whiteBoard=None,blackBoard=None,copy=False):  
    self.__size = int(size)
    if copy:
      self.whiteBoard = whiteBoard
      self.blackBoard = blackBoard
      self.fringe = fringe
      self.closed_list = closed_list
    else:
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
      self.closed_list = [
        (n // 2 - 1, n // 2 - 1),
        (n // 2, n // 2 - 1),
        (n // 2 - 1, n // 2),
        (n // 2, n // 2)
      ]
      self.fringe = {}
      x0 = y0 = n // 2 - 1
      for x in range(0, n):
        for y in range(0, n):
          if x >= x0-1 and x < x0+3 and y >= y0-1 and y < y0+3 and (x, y) not in closed_list:
            self.fringe[(x, y)] = True

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
      pieces_to_flip = []

      # Traverse in the given direction
      #print(0 <= i < self.__size, 0 <= j < self.__size)
      #print(i, j)
      while 0 <= i < self.__size and 0 <= j < self.__size:
        # check if the space is an opponent's piece
        if opponentBoard.is_occupied((i, j)):
          found_opponent = True
          pieces_to_flip.append((i, j))
        elif currentBoard.is_occupied((i, j)):
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

  def duplicate(self):
    return Board(self.__size, self.fringe.copy(), self.closed_list.copy(), self.whiteBoard.duplicate(), self.blackBoard.duplicate(), True)
  
  # generates list of sucecssor states
  def successors(self, player):

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
      yield board

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
        elif g.DEBUGGING and self.is_in_fringe((i, j)):
          ret += "|#"
        else:
          ret += "| "
      ret += '|\n'
    ret += '+' + '-+'*self.__size + '\n'
    return ret


if __name__ == '__main__':
  print("Testing Board.py...")
  board = Board(6)
  s = board.successors('W')
  print(board)
  
  for b in s:
    print(b)
  
