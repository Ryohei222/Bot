# coding: UTF-8
from datetime import datetime, date
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

sys.path.append(str(Path.cwd()))

def epoch_to_date(epoch):
    return datetime(*time.localtime(epoch)[:6]).date()

def TweettoNoticeUsers():
    """
    今日ACしていない精進Botの登録したフォロワーにリプライを送ります
    """

    conn = sqlite3.connect(str(Path.cwd()/'db'/'info.db'))
    c = conn.cursor()
    checksql = 'select * from userinfo'
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
            # api.update_status(status='今日ACを確認していません', in_reply_to_status_id=item[0])
            print('@' + item[0] + '(' + item[1] +')は今日ACをしていません')
        else:
            print('@' + item[0] + '(' + item[1] + ')は今日ACをしています！')


TweettoNoticeUsers()