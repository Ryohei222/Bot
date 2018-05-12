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

import ranking

sys.path.append(Path.cwd())

def TweettoNoticeUsers():
    """
    今日ACしていない精進Botの登録したフォロワーにリプライを送ります
    """

    conn = sqlite3.connect(Path.cwd()/'db'/'info.db')
    c = conn.cursor()
    checksql = 'select * from userinfo where notice = 1'
    c.execute(checksql)
    res = c.fetchall()

    url = 'https://kenkoooo.com/atcoder/atcoder-api/results?user='

    api = ranking.GetTweepyAPI()

    for item in res:
        
        response = urllib.request.urlopen(url+item[1])
        data = json.loads(response.read().decode('utf8'))
        
        flag = True

        for i in data:
            if i['result'] == 'AC' and int(i['epoch_second']) >= Today:
                flag = False
                break
            
        if flag:
            # api.update_status(status='今日ACを確認していません', in_reply_to_status_id=i[0])
            print(i[0])


if __name__ == 'main':
    TweettoNoticeUsers()