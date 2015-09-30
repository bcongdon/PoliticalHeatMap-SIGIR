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
4. Create a file called "api_key.txt" in the same directory as TwitterCralwer.py. This file contains your <b>AlchemyAPI</b> keys.
