# File : AI.py
# Location: Othello/agent

from Agent import Agent
import random

class AI(Agent):
    def __init__(self, closed_list, fringe):
        Agent.__init__(self, closed_list, fringe)
        
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
