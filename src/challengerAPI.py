import requests
from pprint import pprint
import pandas as pd
import time
from datetime import datetime
from find_dir import cmd_folder
import yaml

with open(cmd_folder+"config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

APIKey = cfg['key']

def getIDS(rank,region):
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

# challengers = getIDS("challenger","LAN")

# masters = getIDS("master",region,APIKey)

def checkPartId(req,ids):
    i = 0
    acc = False
    while (i < 10)&(not acc):
        acc = req['participantIdentities'][0]['player']['summonerId'] == ids
        i+=1
    return i-1

def getMatches(players,region,dfAV,dfAP,tst):
    #Here is how I make my URL.  There are many ways to create these.
    compteur = 0
    t = time.time()
    for player in players:
        if compteur%9 == 0:
            time.sleep(max(0,round(15-time.time()+t)))
            t = time.time()
        URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/matchlist/by-summoner/"+player+"?rankedQueues=TEAM_BUILDER_RANKED_SOLO&beginTime=1481108400000&api_key=" + APIKey
    #requests.get is a function given to us my our import "requests". It basically goes to the URL we made and gives us back a JSON.
        response = requests.get(URL)
        compteur +=1
    #Here I return the JSON we just got.
    # #Once again, what requestData returns is a JSON.
        responseJSON  = response.json()
        # for i in range(len(responseJSON['matches'])):
        # for i in range(10):

        i = 0
        ts = responseJSON['matches'][i]['timestamp']/1000
        while ts > tst:
            i+=1
            ts = responseJSON['matches'][i]['timestamp']/1000

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
        dfAV.loc[len(dfAV)] = [player,ids,ts,kills,deaths,assists,minionsKilled,matchDuration,totalKills]

        i = i-1
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
        dfAP.loc[len(dfAP)] = [player,ids,ts,kills,deaths,assists,minionsKilled,matchDuration,totalKills]

    return dfAV,dfAP

# region = "LAN"
# player = challengers[0]

# df1 = getMatches([challengers[0]],region,APIKey)
# int(ts)/1000
# ts_epoch = float(df1.timestamp[0])/1000
# datetime.fromtimestamp(int(ts)/1000-3600).strftime('%Y-%m-%d %H:%M:%S')
# ts


# df1.to_csv(cmd_folder+'csv/riot.csv')
