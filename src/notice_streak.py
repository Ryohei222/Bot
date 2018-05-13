# coding: UTF-8
from datetime import datetime, date
import json
import re
import sqlite3
import sys
import time
import urllib
import random
from pathlib import Path
from operator import itemgetter

import requests
import tweepy
from bs4 import BeautifulSoup

import yaml

import ranking

sys.path.append(str(Path.cwd()))

def epoch_to_date(epoch):
    return datetime(*time.localtime(epoch)[:6]).date()

message = ['Streakが切れるよ！やばいよ！やばたにえんだよ！', 'へ\nStreakがきれそうですが\nしょうじんbotより', '今日は忙しいんですね']

def TweettoNoticeUsers():
    """
    今日ACしていない精進Botの登録したフォロワーにリプライを送ります
    """

    conn = sqlite3.connect(str(Path.cwd()/'db'/'info.db'))
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
        today = date.today()

        for i in data:
            if i['result'] == 'AC' and epoch_to_date(int(i['epoch_second'])) == today:
                flag = False
                break
            
        if flag:
            f = random.randrange(3)
            status = ""

            if f == 1:
                status = '@' + item[0] + '\n' 
                username = str(api.get_user(screen_name=item[0]).name)
                status += username + message[f]
            else:
                status = '@' + item[0] + '\n' + message[f]

            api.update_status(status=status)
            print(status)

        else:
            print('@' + item[0] + '(' + item[1] + ')は今日ACをしています！')


TweettoNoticeUsers()
