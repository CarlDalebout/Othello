

def abmm(s, player, alpha = [None, -999999], beta = [None, 999999]):
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
    return (minimum_action, minimum)