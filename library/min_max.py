# File : min_max.py

import Board as Board


# TODO:
# Generate terminal_values dictionary from terminal search nodes in search tree
# the terminal_test(s) method should be defined in AI.py file
# the min-max algorithm should be moved over as well, defined after terminal_test(s) has been initialized


#################### START: TEST DATA ####################
def successors(s):
    d = {
        's1' : [('a1', 's2'), ('a2', 's3'), ('a3', 's4')],
        's2' : [('a4', 's5'), ('a5', 's6'), ('a6', 's7')],
        's3' : [('a7', 's8'), ('a8', 's9'), ('a9', 's10')],
        's4' : [('a10', 's11'), ('a11', 's12'), ('a12', 's13')],
        's5' : [('a13', 's14'), ('a14', 's15'), ('a15', 's16')]
    }
    d1 = dict([("s%s" % _, []) for _ in range(5, 14)])
    d.update(d1)
    # if value not found return None (bad data)
    return d.get(s, None)

def terminal_value(s):
    d = {
        5:5,
        6:4,
        7:7,
        8:2,
        9:4,
        10:6,
        11:14,
        12:5,
        13:8,
        #14:7,
        #15:42,
        #16:-1
    }

    i = int(s[1:])
    return d.get(i, None)

def terminal_test(s):
    return terminal_value(s) is not None
  
#################### END: TEST DATA ####################

########## MIN MAX ALGORITHM
# board  = Board
# player = MAX/MIN
# minMax = used for alpha-beta pruning; initialized to None for left-most nodes in each row
def abmm(s, player, minMax=None): 
    # check if current node has terminal value
    if terminal_test(s):
        return (None, terminal_value(s))
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
        for action,state in successors(s):
            # keep track of action used to get successor state
            a = action
            # pass current maxValue into minMax to use for
            # alpha-beta pruning at the next layer
            # returns value to check for current MAX layer
            v = abmm(state, "MIN", maxValue)[1]
            
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
        for action,state in successors(s):
            a = action
            v = abmm(state, "MAX")[1]
            
            
            # update current layer's MIN value
            if v < minValue:
                minValue = v
                minAction = a
                
            # perform alpha-beta pruning
            if minMax != None and v < minMax:
                break
                
        return (minAction, minValue)
                    
# maximum threshold (large negative #, etc) instead of initalizing to None
# merge alpha and beta into minMax
# 

def minMax(board, depth, alpha = -9999999, beta = 99999999, player = True):
  if depth == 0 or (board.whiteboard & board.blackboard) == 2: # or whiteBoard & blackBoard = 2^size*size
    return board.eval()
  if player:
    maxEval = -999999999
    for move in board.getmoves("W"):
      eval = minMax(move, depth-1, alpha, beta, False)
      maxEval = max(maxEval, eval)
      alpha = max(alpha, eval)
      if beta <= alpha:
        break
    return maxEval
  
  else:
    minEval = 999999999
    for move in board.getmoves("B"):
      eval = minMax(move, depth-1, alpha, beta, True)
      minEval = min(minEval, eval)
      beta = min(beta, eval)
      if beta <= alpha:
        break
    return minEval

if __name__ == '__main__':
    # test min-max with alpha-beta pruning algorithm
    ret = abmm('s1', "MAX")
    print(ret)




'''def abmm(s, player, alpha = [None, -999999], beta = [None, 999999]):
  if termial_test(s):
    return(None, termial_value(s))
  
  # block for when the player is max returning the best a
  elif player in ['MAX', 'Max', 'max']:
    maximum = -99999999
    maximum_action = None
    for action, state in successors(s):
      action_value = abmm(state, "Min", alpha, beta)
      a, v = action_value
      if v > maximum:
          maximum = v
          maximum_action = [action, a]
      if maximum > alpha[1]:
          alpha[1] = maximum
          alpha[0] = maximum_action

      if beta[1] <= alpha[1]:
        # print('skipping past', state)
        break
    return (maximum_action, maximum)
  
  else:
    minimum = 99999999
    minimum_action = None
    for action , state in successors(s):
      action_value = abmm(state, "Max", alpha, beta)
      a, v = action_value
      if minimum == None or v < minimum:
        minimum = v
        minimum_action = [action, a]
      if minimum > beta[1]:
        beta[1] = minimum
        beta[0] = minimum_action
      if beta[1] <= alpha[1]:
        # print('skipping past', state)
        break
    return (minimum_action, minimum)'''
