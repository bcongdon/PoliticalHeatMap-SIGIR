from datetime import datetime
import sys, os
from TwitterAPI import TwitterAPI
from alchemyapi import AlchemyAPI
import APIKeyManager

import json, time

def doTwitterSearch(searchTerm, coordinates, radius, stateName):

    print "-Doing Twitter search for \"" + searchTerm + "\" in " + stateName
    alchemyAPI = APIKeyManager.GetAlchemyAPIObject()
    try:
        api = APIKeyManager.GetTwitterAPIObject()
        queryTerms = {"q":searchTerm,"geocode":coordinates + "," + radius + "km", "count":100}

        query = api.request('search/tweets',queryTerms).json()

        prunedOutput = dict()
        prunedOutput["tweets"] = list()
        for tweet in query["statuses"]:
            resultDict = dict()
            resultDict["text"] = tweet["text"]
            resultDict["id"] = tweet["id"]
            resultDict["text"] = tweet["text"]
            resultDict["created_at"] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            resultDict["geotag"] = tweet["geo"]
            resultDict["userid"] = tweet["user"]["id"]
            prunedOutput["tweets"].append(resultDict)

            ### SENTIMENT ANALYSIS
            sentiment = "0"
            if tweet["text"] != None:
                alchemyResponse = alchemyAPI.sentiment('text', tweet["text"])
                count = 0
                if alchemyResponse["status"] == "OK":
                    if 'score' in alchemyResponse["docSentiment"]:
                        sentiment = alchemyResponse["docSentiment"]["score"]
                        count += 1

                else:
                    print alchemyResponse["status"]
                    print "Problem with AlchemyAPI response: " + alchemyResponse["statusInfo"]
                    alchemyAPI = APIKeyManager.GetAlchemyAPIObject()
            resultDict["sentiment"] = sentiment

        #Sorts the results from oldest -> newest
        prunedOutput["tweets"] = sorted(prunedOutput["tweets"], key=lambda result: result["created_at"])

        #Number of recieved tweets
        queryTerms["tweets_returned"] = len(query["statuses"])

        #Returns data
        return prunedOutput


    except Exception as e:
        print(e)

def OutputJSONResults(resultsDict, candidate):
    #Import old results if they exists
    outputResults = dict()
    DIR = "output/"
    if not os.path.exists(os.path.dirname(DIR)):
        os.makedirs(os.path.dirname(DIR))
    try:
        with open(DIR + candidate.replace(" ","") + ".json", "r") as oFile:
            outputResults = json.load(oFile);
    except Exception as e:
        print "No old JSON file found, creating new one."

    if not 'candidate' in outputResults:
        outputResults['candidate'] = candidate

    #See if state exists
    if not 'states' in outputResults:
        outputResults['states'] = dict()

    #Iterate through the current dataset
    for state in resultsDict['states'].keys():
        #Appending new data to the old set
        if outputResults['states'].has_key(state):
            for newTweet in resultsDict['states'][state]['tweets']:
                if not newTweet in outputResults['states'][state]['tweets']:
                    outputResults['states'][state]['tweets'].append(newTweet)
        #Create new dictionary if doesn't exist
        else:
            outputResults['states'][state] = resultsDict['states'][state]

        outputResults['states'][state]['sentiment'] = ProcessSentimentStatistics(outputResults['states'][state]['tweets'])

    with open(DIR + candidate.replace(" ","") + ".json", "w+") as oFile:
        json.dump(outputResults, oFile);

def ProcessSentimentStatistics(tweets):
    posSentiment, negSentiment = 0,0
    cumSentiment = 0.0
    for tweet in tweets:
        cumSentiment += float(tweet['sentiment'])
        if float(tweet['sentiment']) > 0:
            posSentiment += 1
        elif float(tweet['sentiment']) < 0:
            negSentiment += 1
    if len(tweets) <= 0:
        return None
    return {"overall_sentiment": cumSentiment, "percent_positive_sentiment": float(100.0*posSentiment/len(tweets)),
        "percent_negitive_sentiment": float(100.0*negSentiment/len(tweets))}


def DoSearchOnCandidate(candidate):
    outputResults = dict()
    outputResults["candidate"] = candidate
    outputResults["states"] = dict()

    api = APIKeyManager.GetTwitterAPIObject()
    with open("state-coords.txt","r") as sFile:
        for line in sFile:
            if len(line.split()) == 0:
                continue
            stateName = line.split()[0]
            coordinates = line.split()[1]
            radius = line.split()[2]
            outputResults["states"][stateName] = doTwitterSearch(candidate, coordinates, radius, stateName)
    print "***Searches left: " + str(api.request('application/rate_limit_status',{"resources":"search"}).json()["resources"]["search"]["/search/tweets"]["remaining"])
    OutputJSONResults(outputResults, candidate)

def SearchAllCandidates():
    with open("candidates.txt","r") as cFile:
        for line in cFile.read().split("\n"):
            if line != "":
                print "-----------"+line+"--------------"
                DoSearchOnCandidate(line)

SearchAllCandidates()
