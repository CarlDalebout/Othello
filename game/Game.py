# File : Game.py
# Location: Othello/Game

# make root directory (Othello) and other useful subdirectories
# to be able to be referenced as modules
import sys
sys.path.append('..')
sys.path.append('../board')
sys.path.append('../agent')
sys.path.append('../ai')
from Board import Board
from Player import Player
from AI import AI


class Game:
    def __init__(self, board_size):
        n = board_size
        self.board = Board(n)
        # black starts first
        self.__currentPlayer = 'B'
        self.black = Player(self.board, 'B')
        self.white = AI(self.board, 'W')

    def current_player(self):
        return self.__currentPlayer

    def show_board(self):
        print(self.board)

    def play_turn(self):
        if self.__currentPlayer == 'B':
            print("-----Black's Turn-----")
            move = self.black.get_move()
            self.black.play_move(move)
            self.__currentPlayer = 'W'
        else:
            print("-----White's Turn-----")
            move = self.white.get_move_(2)
            print(move)
            self.white.play_move(move)
            self.__currentPlayer = 'B'

    def play_game(self):
        game_completed = False
        while not game_completed:
            self.show_board()
            self.play_turn()
            


if __name__ == '__main__':
    print("Testing Game.py...")
    game = Game(6)
    game.play_game()
    
    
