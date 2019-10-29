from players.Player import Player
import numpy as np


### Time limit per decision 0.01s !!!
class ProbPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        # vector of probabilities, that opponent has given card
        self.prob_vector = None
        # current pile of put down cards, (i,j) if known card, None if unkown card
        self.pile = []
        self.opponent_didnt_draw = False

    def _init_prob_vector(self):
        probs = {(i, j): 0.5 for i in range(9, 15) for j in range(4)}
        for c, _ in probs:
            if c in self.cards:
                probs[c] = 0
        return probs
    
    def _recount_probs(self):
        #print(self.prob_vector)
        for c in self.cards:
            self.prob_vector[c] = 0

        non_sure = sum([v for k, v in self.prob_vector if v not in (0,1)])
        if non_sure > 8:
            for k, v in self.prob_vector:
                if 0 < v < 1:
                    self.prob_vector[k] = 1/(non_sure+8)
        elif non_sure == 8:
            # player obtains perfect information about cards' locations
            for k, v in self.prob_vector:
                if 0 < v < 1:
                    self.prob_vector[k] = 0
        else:
            raise Exception('Non-sure cards number can\'t be less than 8!')
            


    def putCard(self, declared_card):
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]:
            if self.pile: self.pile.pop()
            if self.pile: self.pile.pop()
            if self.pile: self.pile.pop()
            return "draw"

        card = min(self.cards, key=lambda x: x[0])

        declaration = (card[0], card[1])
        if declared_card is not None:
            min_val = declared_card[0]
            if card[0] < min_val: declaration = (min(min_val + 1, 14), declaration[1])

        self.pile.append(card)
        return card, declaration

    def checkCard(self, opponent_declaration):
        self.opponent_didnt_draw = True
        self.pile.append(None)
        # 1 is magic constant
        ttp = self.prob_vector[opponent_declaration] * 1 # telling truth probability
        return np.random.choice([True, False], p=[1-ttp, ttp])

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if checked:
            if iChecked:
                if not iDrewCards:
                    if self.pile:
                        top = self.pile.pop()
                        if top is not None:
                            self.prob_vector[top] = 1
                    if self.pile:
                        top = self.pile.pop()
                        if top is not None:
                            self.prob_vector[top] = 1
                    if self.pile:
                        top = self.pile.pop()
                        if top is not None:
                            self.prob_vector[top] = 1

                    self.prob_vector[revealedCard] = 1
                else:
                    if self.pile: self.pile.pop()
                    if self.pile: self.pile.pop()
                    if self.pile: self.pile.pop()
            else:
                if not iDrewCards:
                    if self.pile:
                        top = self.pile.pop()
                        if top is not None:
                            self.prob_vector[top] = 1
                    if self.pile:
                        top = self.pile.pop()
                        if top is not None:
                            self.prob_vector[top] = 1
                    if self.pile:
                        top = self.pile.pop()
                        if top is not None:
                            self.prob_vector[top] = 1
                else:
                    if self.pile: self.pile.pop()
                    if self.pile: self.pile.pop()
                    if self.pile: self.pile.pop()
        elif not self.opponent_didnt_draw:
            if self.pile:
                top = self.pile.pop()
                if top is not None:
                    self.prob_vector[top] = 1
            if self.pile:
                top = self.pile.pop()
                if top is not None:
                    self.prob_vector[top] = 1
            if self.pile:
                top = self.pile.pop()
                if top is not None:
                    self.prob_vector[top] = 1
            
        self.opponent_didnt_draw = False # reset flag
        self._recount_probs()



    #======================================================

    def startGame(self, cards):
        self.cards = cards
        self.prob_vector = self._init_prob_vector()


    # Add some cards to player's hand (if (s)he checked opponent's move, but (s)he was wrong)
    def takeCards(self, cards_to_take):
        self.cards = self.cards + cards_to_take
        for x in self.cards:
            self.prob_vector[x] = 0



