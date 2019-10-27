from players.Player import Player
import numpy as np
import random

class RandomPlayer(Player):
    
    def putCard(self, declared_card):
        
        ### check if must draw
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            return "draw"
        
        ### player randomly decides which card put on the table
        card = random.choice(self.cards)
        declaration = card
        
        ### player randomly decides whether to cheat or not
        cheat = np.random.choice([True, False])
       
        ### if (s)he decides to cheat, (s)he randomly declares the card.
        if cheat:
            declaration = random.choice(self.cards)             
            
        ### Yet, declared card should be no worse than a card on the top of the pile . 
        if declared_card is not None and declaration[0] < declared_card[0]:
            declaration = (min(declared_card[0]+1,14), declaration[1])

        ### return the decision (true card) and declaration (player's declaration)
        return card, declaration
    
    ### randomly decides whether to check or not
    def checkCard(self, opponent_declaration):
        return np.random.choice([True, False])
