##########################################
# Use a Singlearity-PA (plate appearance predictor)  plus game simulator (Singlearity-Game) to find the best pitcher to bring in for extra inning based
# on 2020 extra inning rules.
##########################################

from common import sing
from pprint import pprint
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from singlearity import State, Player, Team, Venue, Atmosphere, Matchup, Lineup, LineupPos, Game, ApiException, GameSimResults, ApiException

###############################################################
# First, validate that the API key is working
###############################################################
sing.hello_with_key()

###############################################################
# Find the best closer against the Orioles from a list of candidates
###############################################################
def find_best_reliever(pitchers, sims):
    print(f'\nFinding the best closer by simulating {sims} innings')
    home_lineup_positions = [
        LineupPos(player = sing.get_players(name = 'Austin Hays')[0], position = 'CF'),
        LineupPos(player = sing.get_players(name = 'Anthony Santander')[0], position = 'RF'),
        LineupPos(player = sing.get_players(name = 'Jose Iglesias')[0], position = 'SS'),
        LineupPos(player = sing.get_players(name = 'Rio Ruiz')[0], position = '3B'),
        LineupPos(player = sing.get_players(name = 'Hanser Alberto')[0], position = '2B'),
        LineupPos(player = sing.get_players(name = 'Renato Nunez')[0], position = '1B'),
        LineupPos(player = sing.get_players(name = 'Dwight Smith')[0], position = 'DH'),
        LineupPos(player = sing.get_players(name = 'Pedro Severino')[0], position = 'C'),
        LineupPos(player = sing.get_players(name = 'DJ Stewart')[0], position = 'CF'),
        LineupPos(player = sing.get_players(name = 'Tommy Milone')[0], position = 'P'),
    ]

    visit_lineup_positions = [
        LineupPos(player = sing.get_players(name = 'Yandy Diaz')[0], position = '3B'),
        LineupPos(player = sing.get_players(name = 'Jose Martinez')[0], position = '1B'),
        LineupPos(player = sing.get_players(name = 'Yoshi Tsutsugo')[0], position = 'DH'),
        LineupPos(player = sing.get_players(name = 'Hunter Renfroe')[0], position = 'RF'),
        LineupPos(player = sing.get_players(name = 'Manuel Margot')[0], position = 'LF'),
        LineupPos(player = sing.get_players(name = 'Mike Brosseau')[0], position = '3B'),
        LineupPos(player = sing.get_players(name = 'Willy Adames')[0], position = 'SS'),
        LineupPos(player = sing.get_players(name = 'Kevin Kiermaier')[0], position = 'CF'),
        LineupPos(player = sing.get_players(name = 'Mike Zunino')[0], position = 'C'),
        LineupPos(player = sing.get_players(name = 'Tyler Glasnow')[0], position = 'P'),
    ]

    B = pd.Index([f'{batter.player.full_name} ({batter.player.bat_side})' for batter in home_lineup_positions], name="rows")[0:9]
    P = pd.Index([f'{pitcher.full_name} ({pitcher.pitch_hand})' for pitcher in test_pitcher_list] , name="columns")
    home_lineup = Lineup(lineup = home_lineup_positions)
    df = pd.DataFrame('', index=B, columns=P)
    location = sing.get_venues(stadium_name='Oriole Park')[0]
    home_team = sing.get_teams(name = "Orioles")[0]
    #assume, visit team has one run lead in the bottom of the 10th inning.   Based on 2020 rules, home team starts with a runner on 2B and no one out
    bat_score_start = 2
    fld_score_start = 3 
    for bat_lineup_start in range(1, 10):  #loop through batters.    Skip last batter (pitcher) because of DH
        st = State(inning=10, top=False, on_1b=False, on_2b=True, on_3b=False, outs=0, bat_score=bat_score_start,
                   fld_score=fld_score_start, bat_lineup_order=bat_lineup_start)
        pitcher_count = 0
        for pitcher in pitchers:  #loop through pitchers
            pitcher_count = pitcher_count + 1   #track which pitcher we are using
            visit_lineup_positions[9] = LineupPos(player = sing.get_players(id = pitcher.mlb_id)[0], position = 'P')
            visit_lineup = Lineup(lineup = visit_lineup_positions)
            game = Game(visit_lineup = visit_lineup, home_lineup = home_lineup, atmosphere = Atmosphere(venue = location, home_team = home_team))

            #run the simulation.  it will return an array of GameSimResults
            game_sim_results = sing.get_game_sim({'game' : game, 'start_state' :  st},  num_sims = sims)

            saves = len([1 for r in game_sim_results  if (r.away_score > r.home_score)])
            losses = len([1 for r in game_sim_results  if (r.away_score < r.home_score)])
            ties = len([1 for r in game_sim_results  if (r.away_score == r.home_score)])
            print('Pitcher: {:<20s} Lineup Start: {} Save Percentage: {:.1f}% Loss Percentage: {:.1f}%  Tie Percentage: {:.1f}%'.format(pitcher.full_name, bat_lineup_start, 100*saves/sims
                ,100*losses/sims
                ,100*ties/sims))
            df.loc[B[bat_lineup_start - 1]][P[pitcher_count - 1]] = round(saves/sims, 3)
    for col in df.columns:
        df[col] = df[col].astype(float)
    return df


def plot_results(df):
    plt.figure(figsize=(40, 50))
    sns.heatmap(df, annot=True, fmt='g')
    plt.title('Pitcher Save Probability\n(Assumes an extra inning game with one run lead in the bottom of the 10th,\nno outs, man on 2nd, pitcher pitch_count of 0 )', wrap=True)
    plt.xlabel('Pitcher')
    plt.ylabel('Inning Leadoff Batter')
    plt.yticks(rotation=0)
    plt.show()


if __name__ == '__main__':
    test_pitcher_list = sing.get_players(team_name = 'Yankees', position = 'P', on_40 = True)
    print(f'Evaluating {len(test_pitcher_list)} pitchers')

    df = find_best_reliever(test_pitcher_list, sims = 100)
    df.to_pickle("results.df")   #save it because it may take a long time to run

    #optionally plot the results
    #plot_results(df)
    

