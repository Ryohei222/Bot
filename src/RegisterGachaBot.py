# coding: UTF-8
import time
import sys
import urllib
import requests
import json
import re
import tweepy
import sqlite3
import yaml

from operator import itemgetter
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime, date

import ranking

auth = ranking.GetTweepyAuth()
api = tweepy.API(auth)

#gacha 100~2400
#abc 100~2400 / A/B/C/D
#arc 100~2400 / A/B/C/D
#agc 100~2400 / A/B/C/D/E/F
#review 100~2400
#virtual n 100 200 300 400

class MyStreamListener(tweepy.StreamListener):
    
    def on_status(self, status):
        
        tweet = status.text.split()
        user = str(status.user.screen_name)
        tag = tweet[0]

        if tag[0] != '#':
            return True
        else:
            print(tag)

        status = ""

        if tag == '#register':
            conn = sqlite3.connect(str(Path.cwd()/'db'/'info.db'))
            c = conn.cursor()
            checksql = 'select * from userinfo where twitterid = ?'
            c.execute(checksql, (user,))
            res = c.fetchone()
            
            if res:
                sql = 'update userinfo set acid = ? where twitterid = ?'
                c.execute(sql, (tweet[1], user))
                status = "@" + user + " AtCoderID:" + tweet[1] + 'で上書き登録しました！'
            else:
                sql = 'insert into userinfo values(?, ?, 0)'
                c.execute(sql, (user, tweet[1]))
                status = "@" + user + " AtCoderID:" + tweet[1] + 'で新規登録しました！'
            
            conn.commit()
            conn.close()
            
        elif tag == '#confirm':
            conn = sqlite3.connect(str(Path.cwd()/'db'/'info.db'))
            c = conn.cursor()
            checksql = 'select * from userinfo where twitterid = ?'
            c.execute(checksql, (user,))
            res = c.fetchone()
            if res:
                status = "@" + user + " AtCoderID:" + res[1] + 'で登録されています！'
            else:
                url = 'http://twitcoder.azurewebsites.net/api/users?TwitterID='
                response = urllib.request.urlopen(url+user)
                data = json.loads(response.read().decode('utf8'))
                if len(data) != 0:
                    sql = 'insert into userinfo values(?, ?, 0)'
                    c.execute(sql, (user, data[0]['userName']))
                    status = "@" + user + " AtCoderID:" + data[0]['userName'] + 'で新規登録しました！'
                else:
                    status = "@" + user + ' #register {AtCoderID}を使用して登録してください'

                conn.commit()
                conn.close()         
        
        elif tag == '#notice':
            conn = sqlite3.connect(str(Path.cwd()/'db'/'info.db'))
            c = conn.cursor()
            checksql = 'select * from userinfo where twitterid = ?'
            c.execute(checksql, (user,))
            res = c.fetchone()
            
            if res and tweet[1] == 'on':
                sql = 'update userinfo set notice = 1 where twitterid = ?'
                c.execute(sql, (user,))
                status = "@" + user + " streek切れ通知をオンにしました！"
            elif res and tweet[1] == 'off':
                sql = 'update userinfo set notice = 0 where twitterid = ?'
                c.execute(sql, (user,))
                status = "@" + user + " streek切れ通知をオフにしました！"
            
            conn.commit()
            conn.close() 

        '''  
        elif tag == 'gacha':
            
        elif tag == 'abc':
            
        elif tag == 'arc':
            
        elif tag == '#agc':
            
        elif tag == '#review':
            
        elif tag == '#virtual':
        '''

        if status != "":
            status += str(datetime.now())
            api.update_status(status=status)
            print(status)

        return True


listener = MyStreamListener()
stream = tweepy.Stream(auth, listener)
stream.userstream()
