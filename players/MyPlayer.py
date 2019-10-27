from Player import Player
import numpy as np

### Implement player's strategy. You can compare it with random player 
### (or some strategy implemented by one of you colleagues)
### Time limit per decision 0.01s !!!

class YourPlayer(Player):
    
    ### player's random strategy
    def putCard(self, declared_card):
        return None, None
    
    ### randomly decides whether to check or not
    def checkCard(self, opponent_declaration):
        return False


