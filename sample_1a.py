from common import sing
from pprint import pprint
##########################################
# Some examples of get prediction results using Singlearity-PA.
# An API key is required.
##########################################


from singlearity import State, Player, Team, Venue, Atmosphere, Matchup, ApiException
from singlearity.rest import ApiException

import pandas as pd
pd.options.display.max_rows = 999

###############################################################
# First, validate that the API key is working
###############################################################
sing.hello_with_key()


###############################################################
# Let's try to sign a veteran RH 1B or DH to platoon against the Yankees lefty pitchers 
###############################################################
def get_best_veteran():
    print(f'Running get_best_veteran()')
    candidate_batters = (sing.get_players(position= ["1B", "DH"], 
                      bat_side = ["R"], age_min = 32, active = True))

    #Note that get_players returns a list (even if it returns only one player).
    #So we need to grab the first player.
    candidate_pitchers = [sing.get_players(name = p)[0] for p in ['J.A. Happ', 'James Paxton', 'Jordan Montgomery']]

    #Note that get_venues always returns a list so grab the first venue
    venue = sing.get_venues(stadium_name = "Tropicana")[0]

    atmosph = Atmosphere(venue, temperature = 70, home_team = sing.get_teams(name = "Yankees")[0])

    #form the list of possible matchup by looking at every candidate_batter x candidate_pitcher
    matchups = ([Matchup(batter = m, pitcher = p, 
      atmosphere = atmosph, state=State()) for m in candidate_batters for p in candidate_pitchers])
    results = pd.DataFrame(sing.get_pa_sim(matchups))
    print(f'\nBest Veterans to platoon against Yankee LHP')
    print(results.sort_values(by=["woba_exp"], ascending = False))
    


###############################################################
# Find the pitcher least likely to let in the winning run in a tie game against Aaron Judge in the 9th with two outs and the bases loaded
###############################################################
def choose_reliever():
    print(f'Running choose_reliever()')
    batter = sing.get_players(name="Aaron Judge")[0]
    candidate_pitchers = sing.get_players(team_name="Rays", position=["P"], active = True)
    atmosph = Atmosphere(sing.get_venues(stadium_name = "Yankee Stadium")[0], temperature = 70,
        home_team = sing.get_teams(name = "Yankees")[0])
    state = State(inning=9, top=False, bat_score=3, fld_score=3, on_1b=True, on_2b=True, on_3b=True, outs=2)
    matchups = [Matchup(batter = batter, pitcher = p, 
        atmosphere = atmosph, state=state) for p in candidate_pitchers]
    results = pd.DataFrame(sing.get_pa_sim(matchups))
    print(f'\nBest pitcher to face Aaron Judge with the game on the line')
    pprint(results.sort_values(by=["obp_exp"])) 


if __name__ == '__main__':
    get_best_veteran()  #change to average him against a random sample of lefty pitchers
    choose_reliever()   

