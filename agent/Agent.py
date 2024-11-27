# File : Agent.py
# Location : Othello/agent

class Agent:
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.pieces_to_flip = []

    # get the move that the agent will perform
    # for Player, this will be by input()
    # for AI, this will be by its algorithm
    def get_move(self):
        raise NotImplementedError

    # Precondition: move has already been validated
    def play_move(self, move):
        # Step 1: Place Piece
        if self.color == 'B':
            self.board.set_black(move)
        elif self.color == 'W':
            self.board.set_white(move)
        else:
            raise Exception("Player does not exist!")
        
        # Step 2: Flip Enemy Pieces
        for piece in self.pieces_to_flip:
            self.board.flip_piece(piece)

        # Step 3: Updated Closed List & Remove
        # placed piece from the fringe
        self.board.closed_list.append(move)
        del self.board.fringe[(move[0], move[1])]

        # Step 4: Update Fringe
        for x in range(move[0]-1, move[0]+2):
            for y in range(move[1]-1, move[1]+2):
                if x > -1 and x < len(self.board) and y > -1 and y < len(self.board) and (x, y) not in self.board.fringe and (x, y) not in self.board.closed_list:
                    self.board.fringe[(x, y)] = True
        

    def _str(self):
        return "<Agent %s>" % id(self)


if __name__ == '__main__':
    print("Testing Agent.py...")


    
