#!/usr/bin/env python
# coding: utf-8

import numpy as np
import random

from Game import Game
from players.SimplePlayer import SimplePlayer
from players.CruelPlayer import CruelPlayer
from players.RandomPlayer import RandomPlayer

    




def print_n_moves(n):
    player1 = SimplePlayer("Player A")
    player2 = CruelPlayer("Player B")
    game = Game([player1, player2])

    for i in range(n):
        game.takeTurn()

    
def simulate_n_games(n, p1, p2):
### Perform a full game n times
    stats_wins = [0, 0]
    stats_moves = [0, 0]
    stats_cheats = [0, 0]
    stats_errors = [0, 0]
    stats_cards = [0, 0]
    stats_checks = [0, 0]
    stats_draw_decisions = [0, 0]
    stats_pile_size = 0

    errors = 0

    for t in range(n):
        player1 = p1
        player2 = p2
        game = Game([player1, player2], log = False)
        
        error = False
        while True:
            valid, player = game.takeTurn(log = False)
            if not valid:
                error = True
                stats_errors[player] += 1
                errors += 1
                break
            if game.isFinished(log = False):
                stats_wins[player] += 1
                break
                
        stats_pile_size += len(game.pile)
        if not error:
            for j in range(2):
                stats_moves[j] += game.moves[j]
                stats_cheats[j] += game.cheats[j]
                stats_checks[j] += game.checks[j]
                stats_draw_decisions[j] += game.draw_decisions[j]
                stats_cards[j] += len(game.player_cards[j])

    stats_pile_size /= (n - errors)          
    for j in range(2):
        stats_moves[j] /= (n - errors)
        stats_cheats[j] /= (n - errors)
        stats_checks[j] /= (n - errors)
        stats_draw_decisions[j] /= (n - errors)
        stats_cards[j] /= (n - errors)

        
    print("Wins:")
    print(stats_wins)
    print("Moves:")
    print(stats_moves)
    print("Cards:")
    print(stats_cards)
    print("Pile size:")
    print(stats_pile_size)
    print("Checks:")
    print(stats_checks)
    print("Draw decisions:")
    print(stats_draw_decisions)
    print("Cheats:")
    print(stats_cheats)
    print("Errors:")
    print(stats_errors)
    print("Total errors:")
    print(errors)


def main():
    pass

if __name__ == '__main__':
    main()


simulate_n_games(100, SimplePlayer("Simple"), CruelPlayer("Cruel"))
#print_n_moves(15)