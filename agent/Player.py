# File : player.py
# Location : Othello/agent

from Agent import Agent

class Player(Agent):
    def __init__(self, board, color):
        Agent.__init__(self, board, color)

    def get_move(self):
        row = int(input("row: "))
        col = int(input("col: "))

        while True:
            # make sure piece is on the fringe (edge)
            if (row, col) not in self.board.fringe:
                print("Invalid move. Try again.\n")
                row = int(input("row: "))
                col = int(input("col: "))
                continue
            
            # validate move
            is_valid,pieces_to_flip = self.board.validate_move((row, col), self.color)

            if is_valid:
                self.pieces_to_flip = pieces_to_flip
                break
            else:
                print("Invalid move. Try again.\n")
                row = int(input("row: "))
                col = int(input("col: "))

        return (row, col)

    def __str__(self):
        return "<Player %s>" % id(self)


if __name__ == "__main__":
    print("Testing Player.py...")
