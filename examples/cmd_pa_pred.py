##########################################
# cmd line batter vs. pitcher predictor
# To run: env SINGLEARITY_API_KEY=<api_key> cmd_pa_pred.py 
# cmd_pa_pred.py --help will print out help message and options
##########################################
from common import sing
from pprint import pprint
import seaborn as sns
import matplotlib.pyplot as plt

from singlearity import State, Player, Team, Venue, Atmosphere, Matchup, ApiException

import pandas as pd
import argparse
from datetime import datetime 

pd.options.display.max_rows = 999
pd.options.display.max_columns = 999

#fill in the singlearity parameters with the arguments from the command line
def get_predictions(args):
    batter_list = [sing.get_players(name=b.strip())[0] for b in args.batters.split(',')]
    pitcher_list = [sing.get_players(name=p.strip())[0] for p in args.pitchers.split(',')]

    state = State(inning = args.inning, 
                  on_1b = args.on1b,
                  on_2b = args.on2b,
                  on_3b = args.on3b,
                  outs = args.outs,
                  top = not(args.bottom),
                  bat_score = args.batscore,
                  fld_score = args.fieldscore,
                  pitch_number = args.pitchnumber)
    venue = sing.get_venues(stadium_name=args.venue)[0]
    atmosphere = Atmosphere(venue=venue, home_team=sing.get_teams(name=args.hometeam)[0], temperature = args.temperature)
    matchups = [Matchup(batter = m, pitcher = p,
                         atmosphere = atmosphere, 
                         state=state,
                         date = args.date)
                         for m in batter_list for p in pitcher_list]
    results = pd.DataFrame(sing.get_pa_sim(matchups, return_features=args.showinputs, model_name=args.predictiontype))
    return results


def plot_results(df, key):
    if key is None: 
        return
    df_pivot = df.pivot(index='batter_name', columns='pitcher_name', values=key)
    plt.figure(figsize=(20, 20))
    plt.rcParams.update({'font.size': 15})
    sns.heatmap(df_pivot, annot=True, fmt='g')
    plt.title(f'Predictions for {key}', wrap=True)
    plt.xlabel('Pitcher')
    plt.ylabel('Batter')
    plt.yticks(rotation=0)
    plt.savefig(f'{key}.png')

default_batters = 'Mookie Betts, Cody Bellinger'
default_pitchers = 'Mike Clevinger, Chris Paddack'
default_venue = 'Dodger Stadium'
default_hometeam = 'Dodgers'
default_temperature = 70
default_date = datetime.today().strftime('%Y-%m-%d')

parser = argparse.ArgumentParser(description='Singleairty Batter vs. Pitcher command line.')

parser.add_argument('--batters', default=default_batters, help = f'batters. Quoted and comma separated list of batters. Default "{default_batters}"')
parser.add_argument('--pitchers', default=default_pitchers, help = f'batters. Quoted and comma separated list of batters. Default "{default_pitchers}"')
parser.add_argument('--venue', default=f'{default_venue}', help = f'venue name. Default "{default_venue}"')
parser.add_argument('--hometeam', default=f'{default_hometeam}', help = f'home team. Default "{default_hometeam}"')
parser.add_argument('--date', default=default_date, help=f"date of the game (use format like 2018-08-25). Default is today's date")
parser.add_argument('--inning', type=int, default=1, help='inning.  Default 1')
parser.add_argument('--outs', type=int, default=0, help='outs.  Default 0')
parser.add_argument('--bottom', action='store_true', help='true if bottom half of the inning.  Default False')
parser.add_argument('--on1b', action='store_true', help='true if runner on first base.  Default False')
parser.add_argument('--on2b', action='store_true', help='true if runner on second base. Default False')
parser.add_argument('--on3b', action='store_true', help='true if runner on third base. Default False')
parser.add_argument('--temperature', type=int, default=default_temperature, help=f'temperature.  Default {default_temperature}')
parser.add_argument('--batscore', type=int,help="batting team's score.  Default 0")
parser.add_argument('--fieldscore', type=int,help="fielding team's score.  Default 0")
parser.add_argument('--pitchnumber', type=int,help="pitcher's pitch count at start of the at bat.  Default 0")
model_choices = ['ab_outcome', 'ab_woba', 'ab_woba_no_state']
parser.add_argument('--predictiontype', choices=model_choices, default='ab_outcome', help=f'type of prediction.  Valid options are {model_choices[0]}. Default "ab_outcome"')
parser.add_argument('--showinputs', action='store_true', help='show the values of the input features that were used to make the prediction.  Default False')
parser.add_argument('--plotresult', default=None, help=f'create a plot of a prediction (e.g. "woba_exp"). Default None')


args = parser.parse_args()
results = get_predictions(args)
print(f"Results:\n{results}") #print the dataframe
plot_results(results, args.plotresult)
