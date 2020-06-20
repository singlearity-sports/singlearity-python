from common import sing
from pprint import pprint
##########################################
# Some examples of simulating portions of games using Singlearity-PA.
# An Enterprise API key is required.
##########################################


from singlearity import State, Player, Team, Venue, Atmosphere, Matchup, Lineup, LineupPos, Game, ApiException
from singlearity.rest import ApiException

import pandas as pd
pd.options.display.max_rows = 999
import numpy as np

###############################################################
# First, validate that the API key is working
###############################################################
sing.hello_with_key()


###############################################################
# Find the best closer against the Yankees from a list of candidates
###############################################################
def find_best_closer(pitchers, sims):
    print(f'\nFinding the best closer by simulating {sims} innings')
    yankees_lineup = Lineup(
        lineup = [
        LineupPos(player = sing.get_players(name = 'DJ LeMahieu')[0], position = '2B'),
        LineupPos(player = sing.get_players(name = 'Aaron Judge')[0], position = 'RF'),
        LineupPos(player = sing.get_players(name = 'Gleyber Torres')[0], position = 'SS'),
        LineupPos(player = sing.get_players(name = 'Giancarlo Stanton')[0], position = 'LF'),
        LineupPos(player = sing.get_players(name = 'Gary Sanchez')[0], position = 'C'),
        LineupPos(player = sing.get_players(name = 'Gio Urshela')[0], position = '3B'),
        LineupPos(player = sing.get_players(name = 'Luke Voit')[0], position = '1B'),
        LineupPos(player = sing.get_players(name = 'Miguel Andujar')[0], position = 'DH'),
        LineupPos(player = sing.get_players(name = 'Brett Gardner')[0], position = 'CF'),
        LineupPos(player = sing.get_players(name = 'Gerrit Cole')[0], position = 'P'),
        ]
    )

    location = sing.get_venues(stadium_name='Tropicana')[0]
    home_team = sing.get_teams(name = "Rays")[0]
    for pitcher in pitchers:
        #for half inning simulation, only the pitcher is required
        visit_lineup = Lineup(
            lineup = [
                 LineupPos(player = sing.get_players(name = pitcher)[0], position = 'P'),
            ]
        )
        game = Game(visit_lineup = yankees_lineup, home_lineup = visit_lineup, atmosphere = Atmosphere(venue = location, home_team = home_team))
        game_sim = sing.get_inning_sim(game = game, num_sims = sims)
        print(('Pitcher: {:<20s}  Average Runs/Inning: {:.4f}   Save Percentage: {:.2f}%').format(pitcher, np.mean(game_sim), 100 * len([g for g in game_sim if g == 0])/len(game_sim)))



if __name__ == '__main__':
    test_pitcher_list = ['Nick Anderson', 'Liam Hendriks', 'Brad Hand', 'Colin Poche', 'Scott Barlow', 'Oliver Drake', 'Ryan Pressly', 'Seth Lugo', 'Drew Pomeranz', 'Emilio Pagan', 'Diego Castillo', 'Ty Buttrey']
    find_best_closer(test_pitcher_list, sims = 1000)
    

