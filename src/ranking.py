# coding: UTF-8
import datetime
import json
import re
import sqlite3
import sys
import time
import urllib
from pathlib import Path
from operator import itemgetter

import requests
import tweepy
from bs4 import BeautifulSoup

import yaml

def GetTweepyAPI():
    """
    conf.yamlからトークンを読み込んでAPIインスタンスを返します
    """
    f = open(str(Path.cwd()/'conf.yaml'), 'r+')
    tokens = yaml.load(f)
    auth = tweepy.OAuthHandler(tokens['CK'], tokens['CS'])
    auth.set_access_token(tokens['AT'], tokens['AS'])
    return tweepy.API(auth)

def GetTweepyAuth():
    """
    conf.yamlからトークンを読み込んでTwitterオブジェクトを返します
    """
    f = open(str(Path.cwd()/'conf.yaml'), 'r+')
    tokens = yaml.load(f)
    auth = tweepy.OAuthHandler(tokens['CK'], tokens['CS'])
    auth.set_access_token(tokens['AT'], tokens['AS'])
    return auth

'''
def GetFollowerInfo():
    """
    TwitCoderを叩いてBotのfollowerと対応するAtCoderのIDをタプルと辞書で返します
    """
    api = GetTweepyAPI()
    FollowerInfo = []
    ScreenNames = []

    url = 'http://twitcoder.azurewebsites.net/api/users?TwitterID='

    for followers_id in tweepy.Cursor(api.followers_ids, user_id='ACRankerbot').items():
        ScreenNames.append(followers_id)

    for i in range(0, len(ScreenNames), 100):
        for user in api.lookup_users(user_ids=ScreenNames[i:i+100]):
            FollowerInfo.append([user.screen_name, user.name]) 
    

def GetRankingData(isDaily):
    """
    return ranking data
    """
    userids, IDdict = UpdateUsers()
    url = 'https://kenkoooo.com/atcoder/atcoder-api/results?user='

    scores = [] # powsum sum count user_id 13:33
    now = datetime.datetime.now()
    Yesterday = int((now - datetime.timedelta(days=+6)).timestamp())
    sall = len(userids)
    tmp = 1

    for AtCoderid in userids:
        
        response = urllib.request.urlopen(url+AtCoderid)
        data = json.loads(response.read().decode('utf8'))
        powsum = nsum = count = 0
        
        for item in data:
            if item['result'] == 'AC' and int(item['epoch_second']) >= Yesterday:
                count = count + 1

                if 'point' in item:
                    point = int(item['point'])
                    powsum = powsum + pow(point, 1.8)
                    nsum = nsum + point

        scores.append((powsum, nsum, count, IDdict[AtCoderid]))

        print(str(float(tmp/sall)*100)[0:5] + '%')

        tmp = tmp + 1
    
    sortedscore = sorted(scores, key=itemgetter(0), reverse=True)

    rank = 1

    for item in sortedscore:
        print(str(rank) + ':' + item[3] + ' point_sum:' + str(item[1]) + ' powsum:' + str(int(item[0])))
        rank = rank + 1
'''
