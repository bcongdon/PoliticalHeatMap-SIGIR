from datetime import datetime
import sys
from TwitterAPI import TwitterAPI
from alchemyapi import AlchemyAPI

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

def getAlchemyObject():
    return AlchemyAPI()

def doTwitterSearch(searchTerm, coordinates, excludeRTs, stateName):

    print "**Doing Twitter search for \"" + searchTerm + "\" in " + stateName
    try:
        api = getAPIObject()
        queryTerms = {"q":searchTerm}

        query = api.request('search/tweets',queryTerms).json()

        sentimentScore = 0.0
        posNegSentiment = [0,0]
        count = 0

        prunedOutput = dict()
        prunedOutput["tweets"] = list()
        for tweet in query["statuses"]:
            if excludeRTs and not tweet["text"].startswith("RT"):
                resultDict = dict()
                resultDict["text"] = tweet["text"]
                resultDict["id"] = tweet["id"]
                resultDict["text"] = tweet["text"]
                resultDict["created_at"] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                resultDict["geotag"] = tweet["geo"]
                resultDict["userid"] = tweet["user"]["id"]
                prunedOutput["tweets"].append(resultDict)

                ### SENTIMENT ANALYSIS
                count += 1
                alchemyResponse = AlchemyAPI().sentiment('text', tweet["text"])
                sentiment = 0.0
                if alchemyResponse["status"] == "OK":
                    sentiment = getAlchemyObject().sentiment('text', tweet["text"])["docSentiment"]["score"]

                with open("alchemy.json","w+") as test:
                    try:
                        json.dump(AlchemyAPI().sentiment('text', tweet["text"]), test)

                    except Exception as e:
                        print e
                if sentiment > 0:
                    posNegSentiment[0] += 1
                elif sentiment < 0:
                    posNegSentiment[1] += 1
                sentimentScore += float(sentiment)
                resultDict["sentiment"] = sentiment

        #Sorts the results from oldest -> newest
        prunedOutput["tweets"] = sorted(prunedOutput["tweets"], key=lambda result: result["created_at"])

        #Number of recieved tweets
        queryTerms["tweets_returned"] = len(query["statuses"])

        prunedOutput["sentiment"] = {"sentimentScore":sentimentScore, "percentPositiveSentiment":float(100.0 * posNegSentiment[0]/count),
            "percentNegitiveSentiment":float(100.0 * posNegSentiment[1]/count)}

        #Returns data
        return prunedOutput


    except Exception as e:
        print(e)

def DoSearchOnCandidate(candidate):
    outputResults = dict()
    outputResults["candidate"] = candidate
    outputResults["states"] = dict()

    api = getAPIObject()
    with open("state-coords.txt","r") as sFile:
        for line in sFile:
            stateName = line.split()[0]
            coordinates = line.split()[1]
            radius = line.split()[2]
            outputResults["states"][stateName] = doTwitterSearch(candidate, coordinates, True, stateName)
    print "***Searches left: " + str(api.request('application/rate_limit_status',{"resources":"search"}).json()["resources"]["search"]["/search/tweets"]["remaining"])
    with open(candidate.replace(" ","") + ".json", "w+") as oFile:
        json.dump(outputResults, oFile);

DoSearchOnCandidate("bernie sanders")
