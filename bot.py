# -*- coding: utf-8 -*-

import os, json
from datetime import datetime

from requests_oauthlib import OAuth1Session
import twitter
import urllib.request, urllib.parse

class Bot():
    TWEET_URL = "https://api.twitter.com/1.1/statuses/update.json"

    def __init__(self, api):
        self.api = api

    def tweet(self):
        pass

if __name__ == "__main__":
    #Twitterつぶやき用apiにアクセス

    data = {
            'CK': os.environ["CONSUMER_KEY"],
            'CS': os.environ["CONSUMER_SECRET"],
            'AT': os.environ["ACCESS_TOKEN_KEY"],
            'ATS': os.environ["ACCESS_TOKEN_SECRET"]
            }

    data = urllib.parse.urlencode(data).encode("utf-8")
    with urllib.request.urlopen("http://www.yoheim.net/", data=data) as res:
       html = res.read().decode("utf-8")
