import requests
from pprint import pprint
import pandas as pd

APIKey = "3c96ea44-ba1a-41df-b7ee-66d3c72a2952"
region = 'LAN'

def getIDS(rank,region, APIKey):
    #Here is how I make my URL.  There are many ways to create these.
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.5/league/"+rank+"?type=RANKED_SOLO_5x5&api_key=" + APIKey
    #requests.get is a function given to us my our import "requests". It basically goes to the URL we made and gives us back a JSON.
    response = requests.get(URL)
    #Here I return the JSON we just got.
    # #Once again, what requestData returns is a JSON.
    responseJSON  = response.json()
    # pprint(responseJSON)
    ids = []
    for i in range(len(responseJSON['entries'])):
        ID = responseJSON['entries'][i]['playerOrTeamId']
        ID = str(ID)
        ids.append(ID)
    return ids

print(getIDS("challenger",region,APIKey))

print(getIDS("master",region,APIKey))

https://lan.api.pvp.net/api/lol/lan/v2.2/matchlist/by-summoner/394585?api_key=3c96ea44-ba1a-41df-b7ee-66d3c72a2952

def getMatches(player,region, APIKey):
    #Here is how I make my URL.  There are many ways to create these.
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/matchlist/by-summoner/"+player+"?rankedQueues=TEAM_BUILDER_RANKED_SOLO&beginTime=1481108400000&api_key=" + APIKey
    #requests.get is a function given to us my our import "requests". It basically goes to the URL we made and gives us back a JSON.
    response = requests.get(URL)
    #Here I return the JSON we just got.
    # #Once again, what requestData returns is a JSON.
    responseJSON  = response.json()
    # pprint(responseJSON)
    df = pd.DataFrame(columns = ['matchID','timestamp'])
    for i in range(len(responseJSON['matches'])):
        ids = responseJSON['matches'][i]['matchId']
        ts = responseJSON['matches'][i]['timestamp']
        ids = str(ids)
        ts = str(ts)
        df.loc[len(df)] = [ids,ts]
    return df

pprint(getMatches('394585',region,APIKey))



a = pd.DataFrame()



a['rr']= ids
a['tt']=timestamps
a.append([1,'trt'])
