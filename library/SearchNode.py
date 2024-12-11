# File : SearchNode.py

class SearchNode:
    '''
    SearchNode class, used for generating search tree for MinMax algorithm
    state = board statex
    value = value generated from heuristic (f cost); only used for terminal nodes
    children = sucessors from current node
    isTerminal = identifes if node is terminal
    '''

    def __init__(self,
                 state,
                 value=0,
                 children=[],
                 isTerminal=False):
        self.state = state
        self.value = value
        self.children = children
        self.isTerminal=isTerminal

    def priority(self):
        return self.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value
     
        
    def __str__(self):
        return '<SearchNode %s %s %s>' % (id(self),
                                          self.state,
                                          self.value,
                                          len(self.children))

if __name__ == '__main__':
    print("Testing SearchNode.py...")
