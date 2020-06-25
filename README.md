![enter image description here](http://beta3.singlearity.com/static/assets/Logo-PNG.png)
# Welcome to Singlearity!


Singlearity is a web-based service for baseball analytics.  It uses machine learning to make predictions based on a wide range of historical data.    These predictions can be used to make more effective pre-game and in-game strategy decisions and to provide for more accurate game simulations.


# Requirements

Python 3.6+

## Installation

We recommend you create a virtual environment using **venv** or similar as described in the [python.org guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

Obtain an API key by sending an email request to keys@singlearity.com

``` pip install singlearity```


## Example Usage

**Create it**

Copy ```examples/common.py``` to a local directory.

```pip install pandas```

Create a file ```pa_pred_very_simple.py``` with:

```
##########################################
# Simple batter vs. pitcher plate appearance prediction using defaults
##########################################
from common import sing
from pprint import pprint


from singlearity import State, Player, Team, Venue, Atmosphere, Matchup, ApiException
from singlearity.rest import ApiException

import pandas as pd

def show_example():
    batter_list = ['Mookie Betts', 'Justin Turner', 'Joc Pederson', 'Corey Seager', 'Gavin Lux']
    pitcher_list  = ['Chris Paddack']

    candidate_batters = [sing.get_players(name = player_name)[0] for player_name in batter_list]
    candidate_pitchers = [sing.get_players(name = player_name)[0] for player_name in pitcher_list]
    venue = sing.get_venues(stadium_name = "Dodger Stadium")[0]
    atmosph = Atmosphere(venue, temperature = 70, home_team = sing.get_teams(name = "Dodgers")[0])

    matchups = ([Matchup(batter = m, pitcher = p,
        atmosphere = atmosph, state=State()) for m in candidate_batters for p in candidate_pitchers])
    results = pd.DataFrame(sing.get_pa_sim(matchups))
    print(f'\nResults')
    results = results[['batter_name', 'pitcher_name', 'hr_exp', 'so_exp', 'ba_exp', 'ops_exp',  'woba_exp']]
    print(results.sort_values(by=["woba_exp"], ascending = False))

if __name__ == '__main__':
    show_example()

```

**Run it**
```
env SINGLEARITY_API_SERVER=https://beta3.singlearity.com SINGLEARITY_API_KEY=<API_KEY> python pa_pred_very_simple.py 
```
**Results**
```
     batter_name   pitcher_name    hr_exp    so_exp    ba_exp   ops_exp  woba_exp
2   Mookie Betts  Chris Paddack  0.040692  0.246808  0.252624  0.772680  0.334633
0  Justin Turner  Chris Paddack  0.040539  0.270383  0.242369  0.721671  0.312508
3   Corey Seager  Chris Paddack  0.043649  0.272041  0.242698  0.726551  0.312113
1   Joc Pederson  Chris Paddack  0.043248  0.340692  0.220657  0.695325  0.301649
4      Gavin Lux  Chris Paddack  0.032899  0.356026  0.206187  0.617087  0.269010
```

