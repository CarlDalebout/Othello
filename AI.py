
# File : AI.py
# Location: Othello/agent

from Agent import Agent
import random

class AI(Agent):
    def __init__(self, closed_list, fringe):
        Agent.__init__(self, closed_list, fringe)

    # score function
    # calculates a score for a player based on a given state
    def score(self, state, player):
        # TODO: assign board spaces values, and calculate meaningful score for controlled spaces
        pass

    # heuristic function (strategy 1)
    # state = board
    # player = whose turn is it
    def h1(self, state, player):
        opponent = 'O' if player == 'X' else 'X'
        
        # TODO: try out different heuristics...
        
        # example heuristic: return difference of scores
        playerScore = self.score(state,player)
        opponentScore = self.score(state, opponent)
        return (playerScore - opponentScore)

    # calculate minmax value using heuristic function and minmax algorithm
    def minmax_value(self, state, h, original_player, current_player, max_depth):
        pass


    # TODO: calculate move using minmax algorithm
    def get_move(self, board, color):
        print("AI is thinking...")
        
        choices = list(self.fringe.keys())
        move = random.choice(choices)

        while True:
            is_valid,pieces_to_flip = board.validate_move(move, color)

            if is_valid:
                self.pieces_to_flip = pieces_to_flip
                break
            else:
                choices.remove(move)
                move = random.choice(choices)

        return move

    def __str__(self):
        return "<AI %s>" % id(self)


if __name__ == "__main__":
    print("Testing AI.py...")
