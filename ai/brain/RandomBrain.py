# File : RandomBrain.py
# Location: Othello/ai/brain

import random
from Brain import Brain

class RandomBrain(Brain):
    def __init__(self, actions=[]):
        Brain.__init__(self)
        self.actions = actions
    def run(self, percept):
        return random.choice(self.actions)
    def __str__(self):
        return "<RandomBrain %s %s>" % (id(self), self.actions)

if __name__ == '__main__':
    print("Testing RandomBrain.py...")
    b = RandomBrain([1,2,3])
    print(b)
