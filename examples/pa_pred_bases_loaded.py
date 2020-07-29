###############################################################
# Find the pitcher least likely to let in the winning run in a tie game against Aaron Judge in the 9th with two outs and the bases loaded
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
    batter = sing.get_players(name="Aaron Judge")[0]
    pitching_team = "Rays"
    candidate_pitchers = sing.get_players(team_name = pitching_team, position=["P"], active = True, on_40=True)
    atmosph = Atmosphere(sing.get_venues(stadium_name = "Yankee Stadium")[0], temperature = 70,
        home_team = sing.get_teams(name = "Yankees")[0])
    state = State(inning=9, top=False, bat_score=3, fld_score=3, on_1b=True, on_2b=True, on_3b=True, outs=2)
    matchups = [Matchup(batter = batter, pitcher = p, 
        atmosphere = atmosph, state=state) for p in candidate_pitchers]
    results = pd.DataFrame(sing.get_pa_sim(matchups))
    print(f'\nBest pitcher to face Aaron Judge with the game on the line')
    pprint(results.sort_values(by=["obp_exp"])) 


if __name__ == '__main__':
    show_example()
