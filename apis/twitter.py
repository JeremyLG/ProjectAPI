# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urllib.parse import parse_qs
from pprint import pprint
import pandas as pd
from datetime import datetime
from find_dir import cmd_folder

pd.options.mode.chained_assignment = None

with open(cmd_folder+"config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = cfg['CONSUMER_KEY']
CONSUMER_SECRET = cfg['CONSUMER_SECRET']

OAUTH_TOKEN = cfg['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = cfg['OAUTH_TOKEN_SECRET']

def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

def get_tweets(name,nbr):
        oauth = get_oauth()
        data = pd.DataFrame(columns= ['timestamp','favorite_count','retweet_count','text'])
        for j in range(int(nbr)):
            if j == 0:
                url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+name+"&count="+str(200)
            else:
                url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+name+"&count="+str(200)+"&max_id="+str(max_id)
            response = requests.get(url = url, auth=oauth)
            responseJSON  = response.json()
            for i in range(len(responseJSON)):
                txt = responseJSON[i]['text']
                ts = responseJSON[i]['created_at']
                fav = responseJSON[i]['favorite_count']
                rt = responseJSON[i]['retweet_count']
                data.loc[len(data)] = [ts,fav,rt,txt]
            max_id = responseJSON[199]['id']
        for i in range(len(data)):
            data.timestamp[i] = datetime.strptime(data.timestamp[i], '%a %b %d %H:%M:%S %z %Y')
            data.timestamp[i] = int(data.timestamp[i].timestamp())
        # data['created_at'] =  pd.to_datetime(data['created_at'], format='%a %b %d %H:%M:%S %z %Y')
        return data

if __name__ =="__main__":
    data = get_tweets("realDonaldTrump",3)
    data
    data[data['text'].str.contains("Mex")]
    data.to_csv(cmd_folder+'csv/tweets.csv')
