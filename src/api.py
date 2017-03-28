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
            self.person = c.person
        else:
            print("Going to {} for {} players.".format(c.region,c.rank))
            self.rank = c.rank
            self.region = c.region
    print(self)

  def run(self):
        tweets = get_tweets(self.person,2)
        if self.person == "realDonaldTrump":
            ts = tweets.timestamp[tweets.text.str.contains("Mex")]
            print(ts)
        players = getIDS(self.rank,self.region)
        dfAP = pd.DataFrame(columns = ['playerID','matchID','timestamp','kills','deaths','assists','minionsKilled','matchDuration','totalKills'])
        dfAV = pd.DataFrame(columns = ['playerID','matchID','timestamp','kills','deaths','assists','minionsKilled','matchDuration','totalKills'])
        dfAV,dfAP = getMatches(players[0],self.region)

api = Api()
api.interpret(example_api_model)
api.run()
