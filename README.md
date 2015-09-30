# PoliticalHeatMap-SIGIR
## TwitterCrawler
Uses the "TwitterAPI" python module to collect tweets based on search query and geocode. Outputs to *.json.

### Setup
TwitterCrawler.py makes use of TwitterAPI and AlchemyAPI. In order to use TwitterCrawler, you must have valid API keys for each service.

1. Create a file called "credentials.txt" in the same directory as TwitterCrawler.py. This file contains your <b>TwitterAPI</b> keys.
2. Create a new Twitter App [here](https://apps.twitter.com/app/new).
  1. Once you've created your app, go to the "Keys and Access Tokens" tab.
  2. Click "Generate my access token"
  3. Record your Consumer Key, Consumer Secret Key, Access Token, and Access Token Secret.
3. In credentials.txt, place your keys in a single line in the following format. Separate with commas, no spaces.

  ```
  CONSUMER_KEY,COMSUMER_SECRET_KEY,ACCESS_TOKEN,ACCESS_TOKEN_SECRET
  ```
  * If you have more than one Twitter account, you may place additional API keys on subsequent lines to circumvent the limit on API calls per account.
4. Create a file called "api_key.txt" in the same directory as TwitterCrawler.py. This file contains your <b>AlchemyAPI</b> keys.
5. Register for an Alchemy API key [here](http://www.alchemyapi.com/api/register.html).
6. In "api_key.txt" place your Alchemy API key on the first line.
  * If you have more than one AlchemyAPI key, you may place additional API keys on subsequent lines to circumvent the limit on API calls per account.
7. Run the following command to install the necessary Python packages. 

  ```pip install TwitterAPI```

8. Run the following command: 

  ```python TwitterCrawler.py```

### Optional Settings
* The "candidates.txt" file may be edited to add or remove candidates to search for. Each candidate must be written on separate lines. By default, this file contains current 2016 US Presidential candidates as of ~September, 2015.
* The "state-coords.txt" file may be edited to add or remove locations to search for. The format per line for each location is as follows:

  ```
  LOCATION_NAME LATITUDE,LONGITUDE RADIUS
  ```
  Where Latitude and Longitude are in Decimal Degree formate and Radius is in Kilometers.
