import sys
from alchemyapi import AlchemyAPI
from TwitterAPI import TwitterAPI

def GetAlchemyAPIObject():
    with open("api_key.txt","r") as aFile:
        for line in aFile.read().split("\n"):
            if line != "":
                api = AlchemyAPI(line)
                result = api.sentiment("text","test")
                if result["status"] != "ERROR":
                    return api
    print "Could not initialize valid, usable AlchemyAPI object. Consider requesting another API key."
    exit()
    return None

#Reads Twitter credientials from file and creates an authenticated TwitterAPI Object
def GetTwitterAPIObject():
    credentials = []
    with open("credentials.txt", "r") as credFile:
         credentials = credFile.read().split("\n")
    for line in credentials:
        line = line.split(',')
        #Auth the API object
        try:
            auth = TwitterAPI(line[0],line[1],line[2],line[3])
            if auth.request('application/rate_limit_status',{"resources":"search"}).json()["resources"]["search"]["/search/tweets"]["remaining"] > 0:
                return auth
        except Exception as e:
            print "Error authenticating with TwitterAPI: " + str(e)
    print "Could not find valid, non-expired TwitterAPI object"
    exit()
