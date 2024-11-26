import sys
sys.path.append('../board')

from Board import Board
from Game import Game

if __name__ == '__main__':
  board_size = int(input("board size: "))
  game = Game(board_size)
  game.play_game()
