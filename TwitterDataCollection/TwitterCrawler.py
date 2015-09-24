from datetime import datetime
import sys
from TwitterAPI import TwitterAPI
import json, time

#Reads Twitter credientials from file and creates an authenticated TwitterAPI Object
def getAPIObject():
    credentials = []
    with open("credentials.txt", "r") as credFile:
         credentials = credFile.read().split("\n")

    #Auth the API object
    try:
        auth = TwitterAPI(credentials[0],credentials[1],credentials[2],credentials[3])
        return auth
    except Exception as e:
        print "Error authenticating with Tweepy: " + str(e)

def doTwitterSearch(searchTerm, coordinates, excludeRTs, stateName):

    print "**Doing Twitter search for \"" + searchTerm + "\""
    try:
        api = getAPIObject()
        queryTerms = {"q":searchTerm}
        print "Searches left: " + str(api.request('application/rate_limit_status',{"resources":"search"}).json()["resources"]["search"]["/search/tweets"]["remaining"])

        query = api.request('search/tweets',queryTerms).json()

        prunedOutput = dict()
        prunedOutput["results"] = list()
        for tweet in query["statuses"]:
            if excludeRTs and not tweet["text"].startswith("RT"):
                resultDict = dict()
                resultDict["text"] = tweet["text"]
                resultDict["id"] = tweet["id"]
                resultDict["text"] = tweet["text"]
                resultDict["created_at"] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                resultDict["geotag"] = tweet["geo"]
                resultDict["userid"] = tweet["user"]["id"]
                prunedOutput["results"].append(resultDict)

        #Sorts the results from oldest -> newest
        prunedOutput["results"] = sorted(prunedOutput["results"], key=lambda result: result["created_at"])

        #Number of recieved tweets
        queryTerms["tweets_returned"] = len(query["statuses"])
        prunedOutput["query"] = queryTerms

        """
        TODO: Put output JSON files in a separate directory
        """

        #Dumps JSON data to file in format "query".txt
        with open(queryTerms["q"] + '.json', 'w+') as outputFile:
            json.dump(prunedOutput, outputFile)

        #Prints rate limit quoata

    except Exception as e:
        print(e)

def DoSearchOnCandidate(candidate):
    with open("state-coords.txt","r") as sFile:
        for line in sFile:
            doTwitterSearch(candidate, line.split()[1], True, line.split()[0])
DoSearchOnCandidate("bernie sanders")
