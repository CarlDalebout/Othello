# File : Game.py
# Location: Othello/Game

# make root directory (Othello) and other useful subdirectories
# to be able to be referenced as modules
import sys
sys.path.append('..')
sys.path.append('../board')
from Board import Board

class Game:
    def __init__(self):
        self.board = Board(6)
        # black starts first
        self.__currentPlayer = 'B'

    # TODO: update play_white method
    def play_white(self, space):
        self.board.set_white(space)
        self.board.flip_pieces(space, 'W')

    # TODO: update play_black method
    def play_black(self, space):
        self.board.set_black(space)
        self.board.flip_pieces(space, 'B')

    def current_player(self):
        return self.__currentPlayer

    def show_board(self):
        print(self.board)

    def play_turn(self):
        if self.__currentPlayer == 'B':
            print("-----Black's Turn-----")
            row = int(input("row: "))
            col = int(input("col: "))

            while True:
                if self.board.is_valid((row, col), self.__currentPlayer):
                    break;
                else:
                    print("Invalid move. Try again.\n")
                    row = int(input("row: "))
                    col = int(input("col: "))
                    
            self.play_black((row, col))
            self.__currentPlayer = 'W'
        else:
            print("-----White's Turn-----")
            row = int(input("row: "))
            col = int(input("col: "))

            while True:
                if self.board.is_valid((row, col), self.__currentPlayer):
                    break;
                else:
                    print("Invalid move. Try again.\n")
                    row = int(input("row: "))
                    col = int(input("col: "))
                    
            self.play_white((row, col))
            self.__currentPlayer = 'B'

    def play_game(self):
        game_completed = False
        while not game_completed:
            game.show_board()
            game.play_turn()
            


if __name__ == '__main__':
    print("Testing Game.py...")
    game = Game()
    game.play_game()
    
    
