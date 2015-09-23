import codecs
from datetime import datetime
import sys
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager
import json, time

#Reads Twitter credientials from file and creates an authenticated TwitterAPI Object
def getAPIObject():
    credentials = []
    with open("credentials.txt", "r") as credFile:
         credentials = credFile.read().split("\n")

    #Auth the API object
    try:
        api = TwitterAPI(credentials[0],
                         credentials[1],
                         credentials[2],
                         credentials[3])
        return api
    except Exception as e:
        print "Error authenticating with TwitterAPI: " + str(e)
def doTwitterSearch(searchTerm, coordinates, radius, excludeRTs):
    try:
        api = getAPIObject()
        queryTerms = {"q":searchTerm,"count":100,"lang":"en","include_entities":"false","geocode":coordinates + "," + str(radius) + "mi"}
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

        #Dumps JSON data to file in format "query".txt
        with open(queryTerms["q"] + '.json', 'w+') as outputFile:
            json.dump(prunedOutput, outputFile)

        #Prints rate limit quoata
        print "Searches left: " + str(api.request('application/rate_limit_status',{"resources":"search"}).json()["resources"]["search"]["/search/tweets"]["remaining"])

    except Exception as e:
        print(e)

doTwitterSearch("bernie sanders", "38.898748,-77.037684", 20, True)
# with open("CandidateList.txt","r") as searchFile:
#     for term in searchFile.read().split("\n"):
#         if term != "" and term != " ":
#             doTwitterSearch(term, "38.898748,-77.037684", 20)
