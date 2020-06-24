###############################################################
# Let's try to sign a veteran RH 1B or DH to platoon against the Yankees lefty pitchers 
###############################################################
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

    candidate_batters = (sing.get_players(position= ["1B", "DH"], 
                      bat_side = ["R"], age_min = 32, active = True))
    candidate_pitchers  = [sing.get_players(name = p)[0] for p in ['J.A. Happ', 'James Paxton', 'Jordan Montgomery']]

    venue = sing.get_venues(stadium_name = "Yankee Stadium")[0]
    atmosph = Atmosphere(venue, temperature = 70, home_team = sing.get_teams(name = "Yankee")[0])

    matchups = ([Matchup(batter = m, pitcher = p,
        atmosphere = atmosph, state=State()) for m in candidate_batters for p in candidate_pitchers])
    results = pd.DataFrame(sing.get_pa_sim(matchups))
    print(results.sort_values(by=["woba_exp"], ascending = False))

if __name__ == '__main__':
    show_example()

