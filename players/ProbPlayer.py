from players.Player import Player
import numpy as np


### Time limit per decision 0.01s !!!
class ProbPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        # vector of probabilities, that opponent has given card
        self.prob_vector = self.init_prob_vector()
        # current pile of put down cards, (i,j) if known card, None if unkown card
        self.pile = []
        self.cards_no = 8      # number of cards in player's hand
        self.op_cards_no = 8   # number of oponnent's cards
        self.revealed_cards = 8  # number of cards which location player is certain abput

        self.opponent_didnt_draw = False

    def init_prob_vector(self):
        probs = {(i, j): 0.5 for i in range(9, 15) for j in range(4)}
        for c, _ in probs:
            if c in self.cards:
                probs[c] = 0
        return probs

    def putCard(self, declared_card):
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            if self.pile: self.pile.pop()
            if self.pile: self.pile.pop()
            if self.pile: self.pile.pop()
            return "draw"

        card = min(self.cards, key=lambda x: x[0])
        self.pile.append(card)

        declaration = (card[0], card[1])
        if declared_card is not None:
            min_val = declared_card[0]
            if card[0] < min_val: declaration = (min(min_val + 1, 14), declaration[1])

        self.pile.append(card)
        return card, declaration

    def checkCard(self, opponent_declaration):
        self.opponent_didnt_draw = True
        self.pile.append(None)
        # 0.5 is magic constant
        cheat_p = self.prob_vector[opponent_declaration] * 0.5
        return np.random.choice([True, False], p=[cheat_p, 1-cheat_p])

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if checked:
            if iChecked:
                if not iDrewCards:
                    if self.pile: self.pile.pop()
                    if self.pile: self.prob_vector[self.pile.pop()] = 1
                    if.self.pile: self.pile.pop()
                    self.prob_vector[revealedCard] = 1
                else:
                    if self.pile: self.pile.pop()
                    if self.pile: self.pile.pop()
                    if self.pile: self.pile.pop()
            else:
                if not iDrewCards:
                    if self.pile: self.prob_vector[self.pile.pop()] = 1
                    if self.pile: self.pile.pop()
                    if self.pile: self.prob_vector[self.pile.pop()] = 1
                else:
                    if self.pile: self.pile.pop()
                    if self.pile: self.pile.pop()
                    if self.pile: self.pile.pop()
        elif not self.opponent_didnt_draw:
            # we dont know whether top card is outs or opponent's, so we have to check each one
            if self.pile and self.pile[-1] is not None: self.prob_vector[self.pile.pop()] = 1
            if self.pile and self.pile[-1] is not None: self.prob_vector[self.pile.pop()] = 1
            if self.pile and self.pile[-1] is not None: self.prob_vector[self.pile.pop()] = 1
            
        self.opponent_didnt_draw = False # reset flag

    # Add some cards to player's hand (if (s)he checked opponent's move, but (s)he was wrong)
    def takeCards(self, cards_to_take):
        self.cards = self.cards + cards_to_take
        for x in self.cards:
            self.prob_vector[x] = 0



