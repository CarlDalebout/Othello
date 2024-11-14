import sys
sys.path.append('../board')

from Board import Board
from Game import Game

if __name__ == '__main__':
  game = Game()
  game.play_game()
