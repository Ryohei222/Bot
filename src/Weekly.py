# coding: UTF-8
from datetime import datetime, date, timedelta
import json
import re
import sqlite3
import sys
import time
import urllib
import random
import os
import subprocess
from pathlib import Path
from operator import itemgetter

import requests
import tweepy
from PIL import Image, ImageDraw, ImageFont

import yaml

import ranking

def datetime_to_epoch(d):
    return int(time.mktime(d.timetuple()))

def epoch_to_date(epoch):
    return datetime(*time.localtime(epoch)[:6]).date()

api = ranking.GetTweepyAPI()

# ここでやりたいのはツイート本文の生成
# 形式
# DailyACRanking 2018-3-14
# 1. {name}({@screen_name}) {diffAC}AC {diffSum}pts
# 2. {name}({@screen_name}) {diffAC}AC {diffSum}pts
# 3. {name}({@screen_name}) {diffAC}AC {diffSum}pts
# 4. {name}({@screen_name}) {diffAC}AC {diffSum}pts
# 5. {name}({@screen_name}) {diffAC}AC {diffSum}pts
# 形式
# DailyPointRanking 2018-3-14
# 1. {name}({@screen_name}) {diffAC}AC {diffSum}pts
# 2. {name}({@screen_name}) {diffAC}AC {diffSum}pts
# 3. {name}({@screen_name}) {diffAC}AC {diffSum}pts
# 4. {name}({@screen_name}) {diffAC}AC {diffSum}pts
# 5. {name}({@screen_name}) {diffAC}AC {diffSum}pts

week = timedelta(days=7)
mon = datetime_to_epoch(epoch_to_date(time.time() - week.total_seconds()))
sun = datetime_to_epoch(epoch_to_date(time.time()))
message = 'WeeklyACRanking {0}\n'.format(epoch_to_date(mon))

# '{0}. {1}({2}) {3}AC {4}pts\n'
    
temprate_message = '{0}. {1}({2}) {3}AC {4}pts\n' # {0}-順位 {1}-user {2}-screen_name {3}AC {4}-sum

url = 'https://kenkoooo.com/atcoder/atcoder-api/results?user='

conn = sqlite3.connect(str(Path.cwd()/'db'/'info.db'))
c = conn.cursor()
sql = 'select * from userinfo'
c.execute(sql)
res = c.fetchall()

acdata = list()


for row in res:

    screen_name = row[0]
    user_id = row[1]
    response = urllib.request.urlopen(url+user_id)
    data = json.loads(response.read().decode('utf8'))

    count = 0
    point_sum = 0
    pow_sum = 0

    for item in data:
        if item['result'] == 'AC' and mon <= int(item['epoch_second']) and int(item['epoch_second']) <= sun:
            count += 1
            if 'point' in item:
                p = int(item['point'])
                if p >= 5000:
                    continue
                point_sum += p
                pow_sum += pow(p, 2.0)
    
    if count != 0:
        print(screen_name + ' ' + str(count))
        acdata.append((screen_name, count, point_sum, pow_sum))


sumdata = acdata
acdata = sorted(acdata, key=itemgetter(1), reverse=True)

print(acdata)

PATH = str(Path.cwd()/'data') + '/'

large_font_size = 72
font_size = 50
large_font = ImageFont.truetype(PATH + 'ipagp00303.ttf', large_font_size)
font = ImageFont.truetype(PATH + 'ipagp00303.ttf', font_size)
offset = large_font_size + font_size
text_canvas = Image.new('RGB', (1800, font_size * (len(acdata) + 1) + large_font_size + 100), (255, 255, 255))
draw = ImageDraw.Draw(text_canvas)

rank = 0
before = -1

draw.text((10, 10), 'WeeklyACRanking {0}~{1}'.format(epoch_to_date(mon), epoch_to_date(mon + timedelta(days=6).total_seconds())), font=large_font, fill='#000')

margin = 2
font_size += margin

for j in range(len(acdata)):

    rank = j + 1
    draw.text((10, offset + font_size * j), str(rank) + '. ', font=font, fill='#000')
    res = font.getsize(str(rank) + '. ')
    wres = res[0] + 10

    screen_name = acdata[j][0]
    username = ''
    try:
        username = str(api.get_user(screen_name=screen_name).name)
    except:
        username = 'notfound'

    ac = acdata[j][1]
    point_sum = acdata[j][2]

    imageMessage = '{0}({1}) {2}AC {3}pts'.format(screen_name, username, ac, point_sum)

    draw.text((10 + wres, offset + font_size * j), imageMessage, font=font, fill='#000')

text_canvas.save(PATH + 'text_img.jpg', 'JPEG', quality=90, optimize=True)


api.update_with_media(filename=PATH + 'text_img.jpg', status=message[0:min(140, len(message))])


acdata = sorted(sumdata, key=itemgetter(3), reverse=True)

message = 'WeeklyPointRanking\n'
large_font_size = 72
font_size = 50
large_font = ImageFont.truetype(PATH + 'ipagp00303.ttf', large_font_size)
font = ImageFont.truetype(PATH + 'ipagp00303.ttf', font_size)
offset = large_font_size + font_size
text_canvas = Image.new('RGB', (1800, font_size * (len(acdata) + 1) + large_font_size + 100), (255, 255, 255))
draw = ImageDraw.Draw(text_canvas)

rank = 0
before = -1

draw.text((10, 10), 'WeeklySquareSumRanking {0}~{1}'.format(epoch_to_date(mon), epoch_to_date(mon + timedelta(days=6).total_seconds())), font=large_font, fill='#000')

margin = 2
font_size += margin

for j in range(len(acdata)):

    rank = j + 1
    draw.text((10, offset + font_size * j), str(rank) + '. ', font=font, fill='#000')
    res = font.getsize(str(rank) + '. ')
    wres = res[0] + 10

    screen_name = acdata[j][0]
    username = ''
    try:
        username = str(api.get_user(screen_name=screen_name).name)
    except:
        username = 'notfound'
        
    ac = acdata[j][1]
    point_sum = acdata[j][2]
    pow_sum = acdata[j][3]

    imageMessage = '{0}({1}) {2}AC {3}pts({4})'.format(screen_name, username, ac, point_sum, pow_sum)

    draw.text((10 + wres, offset + font_size * j), imageMessage, font=font, fill='#000')

text_canvas.save(PATH + 'ptext_img.jpg', 'JPEG', quality=90, optimize=True)


api.update_with_media(filename=PATH + 'ptext_img.jpg', status=message[0:min(140, len(message))])
