##########################################
# Demonstrate making plate appearance predictions based on a game state
##########################################
from common import sing
from pprint import pprint


from singlearity import State, Player, Team, Venue, Atmosphere, Matchup, ApiException
from singlearity.rest import ApiException

import pandas as pd
pd.options.display.max_rows = 999

###############################################################
# First, validate that the API key is working
###############################################################
sing.hello_with_key()

def show_example():
    batter_list = ['Mookie Betts', 'Cody Bellinger', 'Corey Seager', 'Manny Machado']
    pitcher_list  = ['Chris Paddack', 'Clayton Kershaw']

    candidate_batters = [sing.get_players(name = player_name)[0] for player_name in batter_list]
    candidate_pitchers = [sing.get_players(name = player_name)[0] for player_name in pitcher_list]
    venue = sing.get_venues(stadium_name = "Dodger Stadium")[0]
    game_state = State(on_1b = False, on_2b = True, on_3b = False, inning = 4, outs = 0, top = True, 
            bat_score = 3, fld_score = 5, pitch_number = 50)
    atmosph = Atmosphere(venue, temperature = 70, home_team = sing.get_teams(name = "Dodgers")[0])

    matchups = ([Matchup(batter = m, pitcher = p, state = game_state,
        atmosphere = atmosph ) for m in candidate_batters for p in candidate_pitchers])
    results = pd.DataFrame(sing.get_pa_sim(matchups))
    print(f'\nResults')
    print(results.sort_values(by=["woba_exp"], ascending = False))
    
if __name__ == '__main__':
    show_example()

