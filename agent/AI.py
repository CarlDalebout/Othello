# File : AI.py
# Location: Othello/agent

############# TODO LIST #############
# [DONE] Built SearchNode.py (Othello/library)
# [DONE] Merged minMax algorithms + added comments
# [TODO - Nathan] Board Methods (Generate Valid Moves & Successors)
# [TODO - Carl] Generate Search Tree (AI.py in AI.get_move())
# [TODO] Create State Class; used for convenience for storing board
# [TODO] Create heuristic_table (dictionary)
# [TODO] Finish AI.score() and AI.h()
# [TODO] Ginish AI.get_t() to generate terminal values for terminal nodes in search tree
# [TODO] Update MinMax to work with the generated searchtree and terminal values
# [TODO] Finish and test AI.get_move()


from Agent import Agent
import random

# TODO : create heuristic table
heuristic_table = {}

class AI(Agent):
    def __init__(self, closed_list, fringe):
        Agent.__init__(self, closed_list, fringe)

    # TODO: return heuristic value for space
    def h(self, h_table, space):
        pass
        
    # score function
    # calculates a score for a player based on a given state
    def score(self, state, player):
        sum_score = 0
        # FOR EACH player's piece
        #  add h(space) to sum_score
        return sum_score

    # get_t : generates terminal value
    # state = board
    # player = whose turn is it
    def get_t(self, state, player):
        opponent = 'O' if player == 'X' else 'X'
        
        # TODO: try out different heuristics...
        
        # example heuristic: return difference of scores
        playerScore = self.score(state,player)
        opponentScore = self.score(state, opponent)
        return (playerScore - opponentScore)

    # calculate minmax value using heuristic function and minmax algorithm
    # state = board
    def get_move_(self, state, player, max_depth):
        # step 1: generate search tree
        # requires that we create a SearchNode
        # each SearchNode should have:
        # (state, parent, parent_action, value=None, possible_actions)

        # 1.1 TODO : board.get_successors()
        initial_node = SearchNode(state=state,
                                  parent=None,
                                  parent_action=None,
                                  value=None,
                                  children=board.get_successors())

        # 1.2 use for loop to generate rest of tree

        # 1.3 generate terminal values for bottom search nodes (using heuristic)

        # 1.4 call min_max on search tree


        # 1.5 return action/move
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
