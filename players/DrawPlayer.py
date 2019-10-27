from Player import Player
import numpy as np

class DrawPlayer(Player):
    
    ### player's random strategy
    def putCard(self, declared_card):
        return "draw"
    
    ### randomly decides whether to check or not
    def checkCard(self, opponent_declaration):
        return np.random.choice([False, False])
