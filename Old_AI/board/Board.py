# File: Board.py
# Dir: Othello/board
# Author: Carl

# if "bitstring" is not working you will need to do "pip install bitstring"

import sys
from ColorBoard import ColorBoard
sys.path.append('..')
import GLOBALS as g
import copy

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
  actions = board.actions('W')
  print(board)
  print(actions)
  for a in actions:
    print(a)
