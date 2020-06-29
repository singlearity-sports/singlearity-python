##########################################
# Use a plate appearance predictor plus game simulator to find the best pitcher to bring in for extra inning based
# on 2020 extra inning rules.
##########################################

from common import sing
from pprint import pprint

from singlearity import State, Player, Team, Venue, Atmosphere, Matchup, Lineup, LineupPos, Game, ApiException, GameSimResults, ApiException

###############################################################
# First, validate that the API key is working
###############################################################
sing.hello_with_key()

###############################################################
# Find the best closer against the Yankees from a list of candidates
###############################################################
def find_best_reliever(pitchers, sims):
    print(f'\nFinding the best closer by simulating {sims} innings')
    home_lineup_positions = [
        LineupPos(player = sing.get_players(name = 'Mookie Betts')[0], position = 'CF'),
        LineupPos(player = sing.get_players(name = 'Gavin Lux')[0], position = '2B'),
        LineupPos(player = sing.get_players(name = 'Max Muncy')[0], position = '1B'),
        LineupPos(player = sing.get_players(name = 'Justin Turner')[0], position = '3B'),
        LineupPos(player = sing.get_players(name = 'Cody Bellinger')[0], position = 'RF'),
        LineupPos(player = sing.get_players(name = 'Corey Seager')[0], position = 'SS'),
        LineupPos(player = sing.get_players(name = 'A.J. Pollock')[0], position = 'DH'),
        LineupPos(player = sing.get_players(name = 'Joc Pederson')[0], position = 'LF'),
        LineupPos(player = sing.get_players(name = 'Will Smith', position = ['C'])[0], position = 'C'),  #for Will Smith add position to distinguish him from other Will Smith's
        LineupPos(player = sing.get_players(name = 'Clayton Kershaw')[0], position = 'P'),
    ]

    visit_lineup_positions = [
        LineupPos(player = sing.get_players(name = 'Mike Yastrzemski')[0], position = 'LF'),
        LineupPos(player = sing.get_players(name = 'Buster Posey')[0], position = 'C'),
        LineupPos(player = sing.get_players(name = 'Brandon Belt')[0], position = '1B'),
        LineupPos(player = sing.get_players(name = 'Evan Longoria')[0], position = '3B'),
        LineupPos(player = sing.get_players(name = 'Alex Dickerson')[0], position = 'RF'),
        LineupPos(player = sing.get_players(name = 'Brandon Crawford')[0], position = 'SS'),
        LineupPos(player = sing.get_players(name = 'Mauricio Dubon')[0], position = '2B'),
        LineupPos(player = sing.get_players(name = 'Wilmer Flores')[0], position = 'DH'),
        LineupPos(player = sing.get_players(name = 'Billy Hamilton')[0], position = 'CF'),
        LineupPos(player = sing.get_players(name = 'Johnny Cueto')[0], position = 'P'),
    ]

    location = sing.get_venues(stadium_name='Dodger Stadium')[0]
    home_team = sing.get_teams(name = "Dodgers")[0]
    #assume, visit team has one run lead in the bottom of the 10th inning.   Based on 2020 rules, home team starts with a runner on 2B and no one out
    bat_score_start = 2
    fld_score_start = 3 
    bat_lineup_start = 7  #assume home team is starting the inning at the #7 spot in their batting order
    st = State(inning = 10, top = False, on_1b=False, on_2b=True, on_3b=False, outs = 0, bat_score = bat_score_start, fld_score = fld_score_start, bat_lineup_order = bat_lineup_start)
    for pitcher in pitchers:
        visit_lineup_positions[9] = LineupPos(player = sing.get_players(name = pitcher)[0], position = 'P')
        visit_lineup = Lineup(lineup = visit_lineup_positions)
        home_lineup = Lineup(lineup = home_lineup_positions)
        game = Game(visit_lineup = visit_lineup, home_lineup = home_lineup, atmosphere = Atmosphere(venue = location, home_team = home_team))

        #run the simulation.  it will return an array of GameSimResults
        game_sim_results = sing.get_game_sim({'game' : game, 'start_state' :  st},  num_sims = sims)
        saves = len([1 for r in game_sim_results  if (r.away_score > r.home_score)])
        losses = len([1 for r in game_sim_results  if (r.away_score < r.home_score)]) 
        ties = len([1 for r in game_sim_results  if (r.away_score == r.home_score)]) 
        print('Pitcher: {:<20s}  Save Percentage: {:.1f}% Loss Percentage: {:.1f}%  Tie Percentage: {:.1f}%'.format(pitcher, 100*saves/sims
                ,100*losses/sims
                ,100*ties/sims))




if __name__ == '__main__':
    test_pitcher_list = ['Tony Watson', 'Shaun Anderson', 'Trevor Gott', 'Jarlin Garcia', 'Wandy Peralta']
    find_best_reliever(test_pitcher_list, sims = 1000)
    

