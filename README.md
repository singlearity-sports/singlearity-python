![enter image description here](http://beta3.singlearity.com/static/assets/Logo-PNG.png)
# Welcome to Singlearity!

Singlearity is a web-based service for baseball analytics.  It uses machine learning to make predictions based on a wide range of player and historical data.    These predictions can be used to make more effective pre-game and in-game strategy decisions and to provide for more accurate game simulations.

This work was presented at the 2021 SABR Conference and the 2021 Sloan Sports Analytics Conference.   You can view the [technical paper](https://www.singlearity.com/static/assets/sloan-singlearity.pdf) or the [Powerpoint presentation](https://www.singlearity.com/static/assets/Singlearity-sabr.pptx).

You can also view an earlier article about Singlearity that appeared on [Baseball Prospectus](https://www.baseballprospectus.com/news/article/59993/singlearity-using-a-neural-network-to-predict-the-outcome-of-plate-appearances/).



# Description

This repository contains sample Python code for making programmatic calls to the Singlearity web service hosted at api.singlearity.com.  If you prefer to use a [Jupyter Notebook](https://www.dataquest.io/blog/jupyter-notebook-tutorial/) to view and experiment with capabilities of the Singlearity service, you can access a Singlearity Notebook [here](https://github.com/singlearity-sports/singlearity-python/blob/master/singlearity.ipynb).

There are two closely related types of predictions that can be obtained:

* **Batter vs. Pitcher predictions (Singlearity-PA)**.   To generate batter vs. pitcher predictions, you must programmatically generate a **Matchup**.  A Matchup consists of a **Batter**, a **Pitcher**, the **Atmosphere** (containing things such as game location and weather), and a **State** (containing things such as score, inning, and baserunners).  A list of matchups can be submitted to the Singlearity server and it will return predicted outcomes for each matchup.  Visit the [singlearity.com](https://www.singlearity.com) website to see a GUI version of Singlearity-PA.

* **Game simulation predictions (Singlearity-Game)**.   Game simulations work by running hundreds or thousands of Monte Carlo simulations using the plate appearance outcomes provided by Singlearity-PA.   To generate game simulations, you must programmatically create home and away **Lineup**s.   The simulation may optionally include a starting **State** at some intermediate point in the game.  This would allow you to simulate, for instance, a tie game in the bottom of the 9th inning game with multiple runners on base, the #5 hitter coming to bat with a tired pitcher on the mound.   Currently, Singlearity-Game only supports simulating to the end of the half-inning.  With a very short piece of code, you could, for instance, simulate how successful each of ten different relievers would be in holding a lead in the bottom of the 10th inning when facing a given portion of the lineup.    It is possible to accurately simulate hundreds or thousands of games in just a few seconds. 

# Requirements

Python 3.6+

## Installation

We recommend you create a virtual environment using **venv** or similar as described in the [python.org guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

Obtain a Trial API key through the [Singlearity Contact Form](https://docs.google.com/forms/d/e/1FAIpQLSdO_K9_6cGBG_iStuSMKbqUBRX3Z8RAYzNVFRBVIXuumVSjAg/viewform?usp=sf_link)

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
from pprint import pprint
import pandas as pd

from common import sing
from singlearity import State, Player, Team, Venue, Atmosphere, Matchup, ApiException
from singlearity.rest import ApiException

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
env SINGLEARITY_API_KEY=YOUR_API_KEY python pa_pred_very_simple.py 
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

## Example Visualizations
It is easy to combine the Singlearity prediction outputs with libraries such as [matplotlib](https://matplotlib.org/) and [seaborn](https://seaborn.pydata.org/) to create visualizations which communicate the important information efficiently. 

 [Here is an example in python](https://github.com/singlearity-sports/singlearity-python/blob/master/examples/inning_pred_extra_innings.py "Here is an example in Python") which combines Singlearity-PA with Singlarity-Game to help select a relief pitcher during a game.  This example assumes that the Yankees are trying to hold on to a one run lead against the Orioles to start the bottom of the tenth inning.     Note that according to the 2020 MLB rules on extra innings, a runner starts on second base with no outs, and there are additional restrictions  on pitcher substitutions.  Singlearity-Game allows the programmer to create this particular game state, and to then run thousands of game simulations to evaluate the probabilities that each pitcher will be able to hold the lead. 

The visualization below shows the probability of each Yankees pitcher holding the one run lead depending on where in the batting order the Orioles begin their half of the inning.

![enter image description here](https://github.com/singlearity-sports/singlearity-python/blob/master/resources/yankees_os_extra_save_python.png)


<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE1NjYzNzc2NzksLTE1MjM3NzY0NTZdfQ
==
-->
