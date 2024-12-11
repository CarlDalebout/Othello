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

import resource

def gettime():
    rs = resource.getrusage(resource.RUSAGE_SELF)
    return rs[0] + rs[1]

class Game:
    def __init__(self, board_size):
        n = board_size
        self.board = Board(n)
        # black starts first
        self.__currentPlayer = 'B'
        self.black = AI(self.board, 'B')
        self.times = []
        self.white = AI(self.board, 'W')
        # how much time each player has left to think
        self.black_time = 6
        self.white_time = 6
        self.game_over = False
        self.winner = None

    def current_player(self):
        return self.__currentPlayer

    def show_board(self):
        print(self.board)

    def get_winner(self):
        # if there are still moves to play
        # that means game ended prematurely
        # because one of the players can't play,
        # in which that player loses
        if len(self.board.fringe) > 0:
            return 'Black' if self.__currentPlayer == 'W' else 'White'
        # else calculate points and return winner
        else:
            white_score = 0
            black_score = 0
            
            for space in self.board.whiteBoard.getSpaces():
                if space[1] == 1: white_score += 1
                
            for space in self.board.blackBoard.getSpaces():
                if space[1] == 1: black_score += 1

            if black_score > white_score:
                winner = 'B'
            elif white_score > black_score:
                winner = 'W'
            else:
                winner = None

            return (winner, white_score, black_score)
        

    def play_turn(self):
        if self.__currentPlayer == 'B':
            print("-----Black's Turn-----")
            starttime = gettime()
            move = self.black.get_move(self.black_time)
            endtime = gettime()
            self.black_time -= (endtime - starttime)
            self.times.append(endtime - starttime)
            print("Move: ", move)
            if move == None:
                self.game_over = True
                return
            self.black.play_move(move)
            self.__currentPlayer = 'W'
        else:
            print("-----White's Turn-----")
            starttime = gettime()
            move = self.white.get_move(self.white_time)
            endtime = gettime()
            self.white_time -= (endtime - starttime)
            self.times.append(endtime - starttime)
            print("Move: ", move)
            if move == None:
                self.game_over = True
                return
            self.white.play_move(move)
            self.__currentPlayer = 'B'

    def play_game(self):
        while not self.game_over:
            self.show_board()
            self.play_turn()

            print("Time: ", self.white_time, self.black_time)

        # else display winner!
        winner = self.get_winner()
        if type(winner) == str:
            print("Player %s won because the opponent couldn't move!" % winner)
        else:
            print("White scored %s points: " % winner[1])
            print("Black scored %s points: " % winner[2])
            print("Player %s won!" % winner[0])

        print("Average time taken each turn: ", sum(self.times)/len(self.times))


if __name__ == '__main__':
    print("Testing Game.py...")
    game = Game(6)
    game.play_game()
    
    
