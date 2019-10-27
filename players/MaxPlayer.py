from players.Player import Player
import numpy as np


### Implement player's strategy. You can compare it with random player
### (or some strategy implemented by one of you colleagues)
### Time limit per decision 0.01s !!!


class MaxPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.cards_history = self.init_cards_history()
        self.pile = []

    def init_cards_history(self):
        history = {(i, j): False for i in range(9, 15) for j in range(4)}
        for c, v in history:
            if c in self.cards:
                history[c] = True
        return history

    ### player's simple strategy
    def putCard(self, declared_card):

        ### check if must draw
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            return "draw"

        card = min(self.cards, key=lambda x: x[0])
        self.pile.append(card)
        self.pile.append(None)

        declaration = (card[0], card[1])
        if declared_card is not None:
            min_val = declared_card[0]
            if card[0] < min_val: declaration = (min(min_val + 1, 14), declaration[1])
        return card, declaration

    def checkCard(self, opponent_declaration):
        if opponent_declaration in self.cards: return True

        return np.random.choice([True, False], p=[0, 1])

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if checked:
            if iChecked:
                if not iDrewCards:
                    self.pile.pop()
                    self.cards_history[self.pile.pop()] = False
                    self.pile.pop()
                else:
                    for x in self.cards:
                        self.cards_history[x] = True
            else:
                if not iDrewCards:
                    print("")


