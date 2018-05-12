# coding: UTF-8
import requests
import tweepy
import sqlite3
import re
import sys
import urllib
import json
import datetime
import time
import yaml
from operator import itemgetter
from bs4 import BeautifulSoup

class TweepyAPI():
    f = open('conf.yaml', 'r+')
    tokens = yaml.load(f)
    auth = tweepy.OAuthHandler(tokens['CK'], tokens['CS'])
    auth.set_access_token(tokens['AT'], tokens['AS'])
    api = tweepy.API(auth)

   