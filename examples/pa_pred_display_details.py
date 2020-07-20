##########################################
# Show the input features used to form the prediction
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
    batter_list = ['Mookie Betts']
    pitcher_list  = ['Chris Paddack']

    candidate_batters = [sing.get_players(name = player_name)[0] for player_name in batter_list]
    candidate_pitchers = [sing.get_players(name = player_name)[0] for player_name in pitcher_list]
    venue = sing.get_venues(stadium_name = "Dodger Stadium")[0]
    atmosph = Atmosphere(venue, temperature = 70, home_team = sing.get_teams(name = "Dodgers")[0])
    state = State(on_1b = False, on_2b = True, on_3b = False, pitch_number = 79, inning = 4, top = False, bat_score = 3, fld_score = 5)

    matchups = ([Matchup(batter = m, pitcher = p, 
        atmosphere = atmosph, state=state) for m in candidate_batters for p in candidate_pitchers])
    results = pd.DataFrame(sing.get_pa_sim(matchups, return_features = True))
    print(f'\nResults')
    print(results.sort_values(by=["woba_exp"], ascending = False))
    
if __name__ == '__main__':
    show_example()

