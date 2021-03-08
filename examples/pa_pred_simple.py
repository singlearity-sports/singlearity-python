##########################################
# Simple batter vs. pitcher plate appearance prediction using defaults
##########################################
from common import sing
from pprint import pprint


from singlearity import State, Player, Team, Venue, Atmosphere, Matchup, ApiException
from singlearity.rest import ApiException

import pandas as pd

batter_list = ['Mookie Betts', 'Cody Bellinger', 'Gavin Lux']
pitcher_list  = ['Chris Paddack']
candidate_batters = [sing.get_players(name = player_name)[0] for player_name in batter_list]
candidate_pitchers = [sing.get_players(name = player_name)[0] for player_name in pitcher_list]
venue = sing.get_venues(stadium_name = "Dodger Stadium")[0]
atmosph = Atmosphere(venue, temperature = 70, home_team = sing.get_teams(name = "Dodgers")[0])
matchups = ([Matchup(batter = m, pitcher = p, 
        atmosphere = atmosph, state=State()) for m in candidate_batters for p in candidate_pitchers])

results = pd.DataFrame(sing.get_pa_sim(matchups))
#just get some interesting stats.  comment below line out to see all predictions
results = results[['batter_name', 'pitcher_name', 'hr_exp', 'so_exp', 'ba_exp', 'ops_exp',  'woba_exp']]
print(f'Results:\n{results}')
    

