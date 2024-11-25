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
        # initial played moves
        closed_list = [
            (n // 2 - 1, n // 2 - 1),
            (n // 2, n // 2 - 1),
            (n // 2 - 1, n // 2),
            (n // 2, n // 2)
        ]
        # initial fringe
        x0 = y0 = n // 2 - 1
        fringe = {}
        for x in range(0, n):
            for y in range(0, n):
                if x >= x0-1 and x < x0+3 and y >= y0-1 and y < y0+3 and (x, y) not in closed_list:
                    fringe[(x, y)] = True
        self.black = Player(closed_list, fringe)
        self.white = AI(closed_list, fringe)

        # set board fringe
        self.board.fringe = fringe.copy()

    def current_player(self):
        return self.__currentPlayer

    def show_board(self):
        print(self.board)

    def play_turn(self):
        if self.__currentPlayer == 'B':
            print("-----Black's Turn-----")
            move = self.black.get_move(self.board, self.__currentPlayer)
            self.black.play_move(self.board, move, self.__currentPlayer)
            self.__currentPlayer = 'W'
        else:
            print("-----White's Turn-----")
            move = self.white.get_move(self.board, self.__currentPlayer)
            self.white.play_move(self.board, move, self.__currentPlayer)
            self.__currentPlayer = 'B'

    def play_game(self):
        game_completed = False
        while not game_completed:
            self.show_board()
            self.play_turn()
            


if __name__ == '__main__':
    print("Testing Game.py...")
    game = Game()
    game.play_game()
    
    
