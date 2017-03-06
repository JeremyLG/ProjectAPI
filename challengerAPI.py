import requests
from pprint import pprint
import pandas as pd
import time

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

challengers = getIDS("challenger",region,APIKey)

masters = getIDS("master",region,APIKey)

def checkPartId(req,ids):
    i = 0
    acc = False
    while (i < 10)&(not acc):
        acc = req['participantIdentities'][0]['player']['summonerId'] == ids
        i+=1
    return i-1

def getMatches(players,region, APIKey):
    #Here is how I make my URL.  There are many ways to create these.
    df = pd.DataFrame(columns = ['playerID','matchID','timestamp','kills','deaths','assists','minionsKilled','matchDuration','totalKills'])
    startTime = time.time()
    for player in players:
        t = time.time()
        URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/matchlist/by-summoner/"+player+"?rankedQueues=TEAM_BUILDER_RANKED_SOLO&beginTime=1481108400000&api_key=" + APIKey
    #requests.get is a function given to us my our import "requests". It basically goes to the URL we made and gives us back a JSON.
        response = requests.get(URL)
    #Here I return the JSON we just got.
    # #Once again, what requestData returns is a JSON.
        responseJSON  = response.json()
    # pprint(responseJSON)
        for i in range(len(responseJSON['matches'])):
            if i%9 == 0:
                print(max(0,round(10-time.time()+t)))
                time.sleep(max(0,round(10-time.time()+t)))
                t = time.time()
            ids = str(responseJSON['matches'][i]['matchId'])
            ts = str(responseJSON['matches'][i]['timestamp'])
            URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/match/"+ids+"?api_key=" + APIKey
            response = requests.get(URL)
            responseJSON2  = response.json()
            partID = checkPartId(responseJSON2,player)
            assists = responseJSON2['participants'][partID]['stats']['assists']
            kills = responseJSON2['participants'][partID]['stats']['kills']
            deaths = responseJSON2['participants'][partID]['stats']['deaths']
            minionsKilled = responseJSON2['participants'][partID]['stats']['minionsKilled']
            assists = responseJSON2['participants'][partID]['stats']['assists']
            matchDuration = responseJSON2['matchDuration']
            totalKills = 0
            for j in range(10):
                totalKills += responseJSON2['participants'][j]['stats']['kills']
            df.loc[len(df)] = [player,ids,ts,kills,deaths,assists,minionsKilled,matchDuration,totalKills]
    return df

# player = challengers[1]

df1 = getMatches([challengers[0]],region,APIKey)

pprint(df1)
