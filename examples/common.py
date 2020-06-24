import os
import singlearity as singlearity
from singlearity import State, Player, Team, Venue, Atmosphere, Matchup, ApiException
from singlearity.rest import ApiException
from pprint import pprint

configuration = singlearity.Configuration()

#set the api key in an environment variable
if os.getenv("SINGLEARITY_API_KEY") is None:
    print('You are not using an API key.  You will not be able to use some Singlearity APIs')
configuration.api_key['SINGLEARITY_API_KEY'] = os.environ.get("SINGLEARITY_API_KEY", "") 

#use environment variable or default to beta3.singlearity.com
configuration.host = os.environ.get("SINGLEARITY_API_SERVER", "http://beta3-api.singlearity.com")

# Enter a context with an instance of the API client
with singlearity.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    sing = singlearity.APIsApi(api_client)
    
    #validate that we can connect to the singelarity server
    print(sing.hello())


