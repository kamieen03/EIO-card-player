import players
from Cheater import simulate_n_games
import sys, inspect

def main():

    # construct list of (class, class_name) pairs
    all_players = []
    for name, obj in inspect.getmembers(sys.modules['players']):
        if inspect.isclass(obj):
            all_players.append((obj, name))

    # for all pairs simulate 100 games
    for i, (obj1, name1) in enumerate(all_players):
        for j, (obj2, name2) in enumerate(all_players[i+1:]):
            print(f'\n\n-------------{name1} VS {name2}--------------')
            simulate_n_games(100, obj1(name1), obj2(name2))

if __name__ == '__main__':
    main()
