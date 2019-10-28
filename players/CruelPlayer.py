from players.Owner import Owner
from players.Player import Player

from collections import defaultdict
import numpy as np


### Implement player's strategy. You can compare it with random player
### (or some strategy implemented by one of you colleagues)
### Time limit per decision 0.01s !!!


class CruelPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.overview = None
        self.pile = []
        self.opponent_draw = True

    def _init_overview(self):
        overview = {(value, color): Owner.IDK for value in range(9, 15) for color in range(4)}
        for card in self.cards:
            overview[card] = Owner.ME
        return overview

    def _bigger_than_n(self, x):
        n = 0
        for card, owner in self.overview:
            if x > card and owner == Owner.BOOT:
                n += 1
        return n


    ### player's simple strategy
    def putCard(self, declared_card):

        ### check if must draw
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            if len(self.pile) > 1:
                self.pile.pop()
            return "draw"

        card = min(self.cards, key=lambda x: x[0])
        self.pile.append(card)

        declaration = (card[0], card[1])
        if declared_card is not None:
            min_val = declared_card[0]
            if card[0] < min_val: declaration = (min(min_val + 1, 14), declaration[1])
        return card, declaration

    def checkCard(self, opponent_declaration):
        #print("------")
        #print([c for c, o in self.overview.items() if o == Owner.ME])
        #print(len([c for c, o in self.overview.items() if o == Owner.BOOT]))
        #print([c for c, o in self.overview.items() if o == Owner.IDK])
        #print("------")
        self.opponent_draw = False
        if opponent_declaration in self.cards:
            return True
        elif opponent_declaration in [c for c, o in self.overview.items() if o == Owner.BOOT]:
            return False
        else:
            return np.random.choice([True, False], p=[0.3, 0.7])

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        print(self.pile)
        print(noTakenCards)
        if checked:
            if iChecked:
                if not iDrewCards:
                    if noTakenCards > 0:
                        self.overview[revealedCard] = Owner.BOOT
                    if noTakenCards > 1:
                        self.overview[self.pile.pop()] = Owner.BOOT
            else:
                if not iDrewCards:
                    if noTakenCards > 0:
                        self.overview[self.pile.pop()] = Owner.BOOT
                    if noTakenCards > 2:
                        self.overview[self.pile.pop()] = Owner.BOOT
        elif self.opponent_draw:
            print("Draw")
            if len(self.pile) > 0:
                self.overview[self.pile.pop()] = Owner.BOOT
            if len(self.pile) > 2:
                self.overview[self.pile.pop()] = Owner.BOOT

        self.opponent_draw = True

    def pop_n(self, n):
        for i in range(n):
            if self.pile[-1]:
                self.pile.pop()

    def startGame(self, cards):
        super().startGame(cards)
        self.overview = self._init_overview()

    def takeCards(self, cards_to_take):
        self.cards = self.cards + cards_to_take
        #print(cards_to_take)
        for card in cards_to_take:
            self.overview[card] = Owner.ME




