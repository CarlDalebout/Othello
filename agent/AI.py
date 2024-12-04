# File : AI.py
# Location: Othello/agent

############# TODO LIST #############
# [DONE] Built SearchNode.py (Othello/library)
# [DONE] Merged minMax algorithms + added comments
# [DONE] Board Methods (Generate Successors)
# [TODO - Carl] Generate Search Tree (AI.py in AI.get_move())
# [TODO -] Create State Class; used for convenience for storing board
# [Done] Create heuristic_table (dictionary)
# [Done] Finish AI.score() and AI.h()
# [TODO -] Ginish AI.get_t() to generate terminal values for terminal nodes in search tree
# [TODO -] Update MinMax to work with the generated searchtree and terminal values
# [TODO -] Finish and test AI.get_move()

from Agent import Agent
import random
import sys
sys.path.append('..')
sys.path.append('../board')
from Board import Board

# first heuristics table for a 10x10 board
heuristic_table10x10 = [[100, -30,  8,  6,  2,  2,  6,  8, -30, 100],
                        [-30, -50,  6,  0,  0,  0,  0,  6, -50, -30],
                        [  8,   6,  0,  0,  0,  0,  0,  0,   6,   8],
                        [  6,   0,  0,  0,  0,  0,  0,  0,   0,   6],
                        [  2,   0,  0,  0,  3,  3,  0,  0,   0,   2],
                        [  2,   0,  0,  0,  3,  3,  0,  0,   0,   2],
                        [  6,   0,  0,  0,  0,  0,  0,  0,   0,   6],
                        [  8,   6,  0,  0,  0,  0,  0,  0,   6,   8],
                        [-30, -50,  0,  0,  0,  0,  0,  6, -50, -30],
                        [100, -30,  8,  6,  2,  2,  6,  8, -30, 100]]

# first heuristics table for a 8x8 board
heuristic_table8x8  = [[100, -30,  6,  2,  2,  6, -30, 100],
                       [-30, -50,  0,  0,  0,  0, -50, -30],
                       [  6,   0,  0,  0,  0,  0,   0,   6],
                       [  2,   0,  0,  3,  3,  0,   0,   2],
                       [  2,   0,  0,  3,  3,  0,   0,   2],
                       [  6,   0,  0,  0,  0,  0,   0,   6],
                       [-30, -50,  0,  0,  0,  0, -50, -30],
                       [100, -30,  6,  2,  2,  6, -30, 100]]

# first heuristics table for a 6x6 board
heuristic_table6x6  = [[100, -30,  6,  6, -30, 100],
                       [-30, -50,  0,  0, -50, -30],
                       [  6,   0,  3,  3,   0,   6],
                       [  6,   0,  3,  3,   0,   6],
                       [-30, -50,  0,  0, -50, -30],
                       [100, -30,  6,  6, -30, 100]]

class AI(Agent):
    def __init__(self, board, color):
        Agent.__init__(self, board, color)
        if len(board) == 6:
            self.h_table = heuristic_table6x6
        elif len(board) == 8:
            self.h_table = heuristic_table8x8
        elif len(board) == 10:
            self.h_table = heuristic_table10x10


    # return heuristic value for the given space
    def h(self, space):
        return self.h_table[space[0]][space[1]]
        
    # score function
    # calculates a score for a player based on a given board state
    def score(self, state, color, h):
        s = 0

        if color == 'W':
            for space in state.whiteBoard.getSpaces():
                if space[1] == 1: s += h(space[0])
        else:
            for space in state.blackBoard.getSpaces():
                if space[1] == 1: s += h(space[0])

        return s

    # customizes min max for othello
    def min_max(self, timeLeft):
        # using time left determine how far we should search
        max_depth = 2
        
        class SearchNode:
            def __init__(self, state, depth):
                self.state = state
                self.depth = depth

        # s = search node (state, depth)
        # player = MIN/MAX
        # minMax = used for alpha-beta pruning
        def mm(s, player, minMax=None):
            # calculate successors
            o_color = "W" if self.color == "B" else "B"
            color = self.color if player == "MAX" else o_color
            successors = s.state.successors(color)
            
            # TERMINAL TEST
            # we reached max depth limit
            # OR there are no child states
            if (not (s.depth < max_depth)) or len(successors) == 0:
                # CALCULATE TERMINAL VALUE
                terminal_value = self.score(s.state, self.color, self.h)
                
                return (None, terminal_value)
            # ELIF do MAX
            elif player == "MAX":
                # initalized to small threshold ("infinitely small")
                # change as needed
                maxValue = -999999
                # action used to get to the max value
                # only important if this is initial call of abmm()
                maxAction = None
                
                # determine MAX of the values at the next level
                # if they are not terminal values, use MIN to determine
                # values for next layer's nodes
                for action,state in successors:
                    # keep track of action used to get successor state
                    a = action
                    # pass current maxValue into minMax to use for
                    # alpha-beta pruning at the next layer
                    # returns value to check for current MAX layer
                    new_node = SearchNode(state=state, depth=s.depth+1)
                    
                    v = mm(new_node, "MIN", maxValue)[1]
            
                    # update current layer's MAX value
                    if v > maxValue:
                        maxValue = v
                        maxAction = a
                
                    # perform alpha-beta pruning
                    if minMax != None and v > minMax:
                        break
                
                return (maxAction, maxValue)
            # ELSE do MIN
            else:
                # initalized to large threshold ("infinitely large")
                # change as needed
                minValue = 999999
                # action used to get the min value
                # only important if this is initial call of abmm()
                minAction = None
                
                # determine MIN of the values at the next level in tree
                # if they are not terminal values, use MAX to determine
                # values for the nexxt layer's nodes
                for action,state in successors:
                    a = action
                    new_node = SearchNode(state=state, depth=s.depth+1)
                    v = mm(new_node, "MAX")[1]
                    
                    
                    # update current layer's MIN value
                    if v < minValue:
                        minValue = v
                        minAction = a
                
                    # perform alpha-beta pruning
                    if minMax != None and v < minMax:
                        break
                    
                return (minAction, minValue)
            
        # return value
        return mm(SearchNode(self.board, 0), "MAX")

    # get_move is the brain of the AI; largely based on minmax to make its decision
    # state = board
    # max_depth = how far to search
    # timeLeft = total time left for playing game
    def get_move(self, time_left):
        print("AI is thinking...")
        result = self.min_max(6)
        self.pieces_to_flip = self.board.validate_move(result[0], self.color)[1]
        return result[0]

    # Random Brain AI
    '''def get_move(self):
        choices = list(self.board.fringe.keys())
        move = random.choice(choices)

        while True:
            is_valid,pieces_to_flip = self.board.validate_move(move, self.color)

            if is_valid:
                self.pieces_to_flip = pieces_to_flip
                break
            else:
                choices.remove(move)
                move = random.choice(choices)

        return move'''

    def __str__(self):
        return "<AI %s>" % id(self)


if __name__ == "__main__":
    print("Testing AI.py...")
    board = Board(6)
    ai = AI(board, "W")

    print(ai.score(board, "W", ai.h))
