# -*- coding: utf-8 -*-

import os, json
from datetime import datetime

from requests_oauthlib import OAuth1Session
import twitter

class Bot():
    TWEET_URL = "https://api.twitter.com/1.1/statuses/update.json"

    def __init__(self, api):
        self.api = api

    def tweet(self):
        pass

if __name__ == "__main__":
    url = "https://api.twitter.com/1.1/statuses/update.json"

    params = {
            "status": "僕の心の中には黒いネクタイが並べられている．見つけてすぐに捨てても，いつだってまだ少し残っているんだ"
            }

    api = twitter.Api(consumer_key=os.environ["CONSUMER_KEY"],
                      consumer_secret=os.environ["CONSUMER_SECRET"],
                      access_token_key=os.environ["ACCESS_TOKEN_KEY"],
                      access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
                      )

    res = api.post(url, params)
