from textx.metamodel import metamodel_from_file
from find_dir import cmd_folder
from twitter import get_tweets
from challengerAPI import getIDS,getMatches
import pandas as pd

api_meta = metamodel_from_file(cmd_folder+'textX/api.tx', autokwd=True)

example_api_model = api_meta.model_from_file(cmd_folder+'textX/example.api')


class Api(object):

  def __init__(self):
    # Initial position is (0,0)
    self.region = ""
    self.rank = ""
    self.person = ""
    self.fun = ""

  def __str__(self):
    return "\nActuellement l'api riot va être lancée sur la région {} et sur les joueurs de rang {}  \nEt {} utilisée sur les tweets de {} !".format(self.region, self.rank,self.fun,self.person)

  def interpret(self, model):

    # model is an instance of Program
    # for d in model.:
        # print("La fonction choisie est : {}".format(d.function))
    for c in model.commands:
        if c.__class__.__name__ == "TwitterCommand":
            print("Check des tweets de : {}".format(c.person))
            if c.person== 'putin':
                self.person = 'PutinRF_Eng'
            else:
                self.person = c.person
        else:
            print("Going to {} for {} players.".format(c.region,c.rank))
            self.rank = c.rank
            self.region = c.region
    self.fun = model.function
    print(self)


  def run(self):
        tweets = get_tweets(self.person,2)
        if self.person == "realDonaldTrump":
            ts = tweets.timestamp[tweets.text.str.contains("Mex")]
            ts.reset_index(drop = True,inplace= True)
            print(ts)
        if self.person == "PutinRF_Eng":
            ts = tweets.timestamp
            ts = ts[28:31]
            ts.reset_index(drop = True,inplace= True)
            print(ts)
        # players = getIDS('challenger','LAN')
        players = getIDS(self.rank,self.region)
        dfAP = pd.DataFrame(columns = ['playerID','matchID','timestamp','kills','deaths','assists','minionsKilled','matchDuration','totalKills'])
        dfAV = pd.DataFrame(columns = ['playerID','matchID','timestamp','kills','deaths','assists','minionsKilled','matchDuration','totalKills'])
        dfAV,dfAP = getMatches(players[0:5],self.region,dfAV,dfAP,ts[0:len(ts)])
        kdaIND = dfAV.kills + dfAV.assists
        print(dfAV.shape)
        print(dfAP.shape)
        dfAV.deaths[dfAV.deaths ==0] =1
        kdaAV = ((dfAV.kills+dfAV.assists)/dfAV.deaths).mean()
        dfAP.deaths[dfAP.deaths ==0] =1
        kdaAP = ((dfAP.kills+dfAP.assists)/dfAP.deaths).mean()
        totalKAV = dfAV.totalKills.mean()
        totalKAP = dfAP.totalKills.mean()
        minionsKilledAV = (dfAV.minionsKilled/dfAV.matchDuration).mean()
        minionsKilledAP = (dfAP.minionsKilled/dfAP.matchDuration).mean()
        durationAV = dfAV.matchDuration.mean()
        durationAP = dfAP.matchDuration.mean()
        score = 0
        if kdaAP > kdaAV:
            score +=1
        else:
            if kdaAP < kdaAV:
                score -=1
        if minionsKilledAP > minionsKilledAV:
            score+=1
        else:
            if minionsKilledAP < minionsKilledAV:
                score -=1
        if totalKAP < totalKAV:
            score +=2
        else:
            if totalKAP > totalKAV:
                score -=2
        if durationAP < durationAV:
            score +=2
        else:
            if durationAP > durationAV:
                score -=2
        print(score/6)










































api = Api()

api.interpret(example_api_model)

api.run()
