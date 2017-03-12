from textx.metamodel import metamodel_from_file

api_meta = metamodel_from_file('./textX/api.tx')

example_api_model = api_meta.model_from_file('./textX/example.api')

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
    for c in model.commands:

        if c.__class__.__name__ == "TwitterCommand":
            print("Check des tweets de : {}".format(c.person))
            self.person = c.person
        else:
            print("Going to {} for {} players.".format(c.region,c.rank))
            self.rank = c.rank
            self.region = c.region


    print(self)

api = Api()
api.interpret(example_api_model)
