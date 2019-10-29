from players.Owner import Owner
from players.Player import Player

from collections import defaultdict
import numpy as np
import random


### Implement player's strategy. You can compare it with random player
### (or some strategy implemented by one of you colleagues)
### Time limit per decision 0.01s !!!


class CruelPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.overview = None
        self.pile = []
        self.opponent_draw = True

    ### player's simple strategy
    def putCard(self, declared_card):

        ### check if must draw
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            self._pop_n(3)
            return "draw"

        card = min(self.cards, key=lambda x: x[0])
        self.pile.append(card)

        declaration = (card[0], card[1])
        if declared_card is not None:
            min_val = declared_card[0]
            if card[0] < min_val:
                possible_picks = [c for c, o in self.overview.items()
                                    if c[0] >= min_val and o == Owner.ME]
                if possible_picks:
                    declaration = random.choice(possible_picks)
                else:
                    declaration = (min(min_val + 1, 14), declaration[1])
        return card, declaration

    def checkCard(self, opponent_declaration):
        self.opponent_draw = False
        self.pile.append(None)
        if self.overview[opponent_declaration] == Owner.IDK:
            idk = list(self.overview.values()).count(Owner.IDK)
            if idk <= 12:
                return np.random.choice([True, False], p=[1-(idk-8)/16, (idk-8)/16])
            else:
                return np.random.choice([True, False], p=[0.3, 0.7])
        elif self.overview[opponent_declaration] == Owner.ME:
            return True
        else:
            return False

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if checked:
            if iChecked:
                if not iDrewCards:
                    self._pop_and_assign(3, Owner.BOOT)
                    self.overview[revealedCard] = Owner.BOOT
                else:
                    self._pop_n(3)
            else:
                if not iDrewCards:
                    self._pop_and_assign(3, Owner.BOOT)
                else:
                    self._pop_n(3)
        elif self.opponent_draw:
            self._pop_and_assign(3, Owner.BOOT)

        self.opponent_draw = True

    def startGame(self, cards):
        super().startGame(cards)
        self.overview = self._init_overview()

    def takeCards(self, cards_to_take):
        self.cards = self.cards + cards_to_take
        for card in cards_to_take:
            self.overview[card] = Owner.ME

    def _pop_n(self, n):
        for i in range(n):
            if self.pile:
                self.pile.pop()

    def _pop_and_assign(self, n, owner):
        for i in range(n):
            if len(self.pile) > 0:
                top_card = self.pile.pop()
                if top_card is not None:
                    self.overview[top_card] = owner

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

        # print("------")
        # print([c for c, o in self.overview.items() if o == Owner.ME])
        # print([c for c, o in self.overview.items() if o == Owner.BOOT])
        # print([c for c, o in self.overview.items() if o == Owner.IDK])
        # print("------")

    # boot_cards = [c for c, o in self.overview.items() if o == Owner.BOOT]
    # if len(boot_cards) > 0:
    #     boot_max = max([c for c, o in self.overview.items() if o == Owner.BOOT])
    #     better_then_boot_cards = [c for c in self.cards if c[0] >= boot_max[0]]
    #     if len(better_then_boot_cards) > 0:
    #         card = min(better_then_boot_cards)

