# File: board.py
# Dir: Othello/board
# Author: Carl

import bitstring  #if this is not working you will need to do "pip install bitstring"


class Board:
  
  def __init__(self, size = 6):
    self.__size = int(size)
    self.whiteBoard = bitstring.BitArray(int = 0, length=size*size)    # creating a bit array of size n*n for the white board
    
    self.whiteBoard[size*(size//2-1) + size//2-1] = 1                  # setting the top left of the starting block
    self.whiteBoard[size*(size//2) + size//2] = 1                      # setting the bottom right of the starting block

    self.blackBoard = bitstring.BitArray(int = 0, length=size*size)    # creating a bit array of size n*n for the black board
    
    self.blackBoard[size*(size//2-1) + size//2] = 1                    # setting the top right of the starting block
    self.blackBoard[size*(size//2) + size//2-1] = 1                    # setting the bottom left of the starting block

  def playWhite(self, row = None, col = None):
    index = self.__size*row + col                                      # creating the index to manipulate based on the row and col

    while self.blackBoard[index] == 1:                                 # Error check to prevent a space being placed on a already claimed black space
      print("!!!ERROR!!! can not place piece there try again")
      row = int(input("row: "))
      col = int(input("col: "))
      index = self.__size*row + col

    self.whiteBoard[index] = 1                                         # Setting bit to 1 
  
  def printWhite(self):
    ret = ""
    for i in range(self.__size):
      ret += '+' + '-+'*self.__size + "\n"
      for j in range(self.__size):
        if self.whiteBoard[i*self.__size + j] == 1: ret += "|W"
        else: ret += "| "
      ret += '|\n'
    ret += '+' + '-+'*self.__size + '\n'
    return ret


  def playBlack(self, row = None, col = None):
    index = self.__size*row + col                                      # creating the index to manipulate based on the row and col
    
    while self.whiteBoard[index] == 1:                                 # Error check to prevent a space being placed on a already claimed black space
      print("!!!ERROR!!! can not place piece there try again")
      row = int(input("row: "))
      col = int(input("col: "))
      index = self.__size*row + col

    self.blackBoard[index] = 1                                         # Setting bit to 1

  def printBlack(self):
    ret = ""
    for i in range(self.__size):
      ret += '+' + '-+'*self.__size + "\n"
      for j in range(self.__size):
        if self.whiteBoard[i*self.__size + j] == 1: ret += "|W"
        else: ret += "| "
      ret += '|\n'
    ret += '+' + '-+'*self.__size + '\n'
    return ret

  def __len__(self):
    return self.__size

  def __str__(self):
    ret = ""
    for i in range(self.__size):
      ret += '+' + '-+'*self.__size + "\n"
      for j in range(self.__size):
        if self.whiteBoard[i*self.__size + j] == 1: ret += "|W"
        elif self.blackBoard[i*self.__size + j] == 1: ret += "|B"
        else: ret += "| "
      ret += '|\n'
    ret += '+' + '-+'*self.__size + '\n'
    return ret