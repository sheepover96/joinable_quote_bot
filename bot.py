# -*- coding: utf-8 -*-

import os, json
import datetime, random
from flask_sqlalchemy import SQLAlchemy

from requests_oauthlib import OAuth1Session
import twitter
import urllib.request, urllib.parse

from app import db
from app import User, Quote

class Bot():
    TWEET_URL = "https://api.twitter.com/1.1/statuses/update.json"

    def __init__(self, api):
        self.api = api

    def tweet(self):
        pass

def tweet(CK, CS, AT, ATS):
    quote = None
    nquotes = db.session.query(Quote).count()
    if nquotes != 0:
        rand_id = random.randint(1, nquotes)
        quote = db.session.query(Quote).get(id=rand)

        url = "https://api.twitter.com/1.1/statuses/update.json"
        api = OAuth1Session(CK,CS,AT,ATS)

        text = quote.text + '\n    ~' + quote.author + '\n quoted from ' + quote.book

        params = {
                "status": text
                }

        res = api.post(url, params)

def quote_register(CK, CS, AT, ATS):
    url = "https://api.twitter.com/1.1/direct_messages.json"
    api = OAuth1Session(CK, CS, AT, ATS)
    params = {}

    last_quote = db.session.query(Quote)\
                   .order_by(Quote.id.desc()).first()

    if last_quote is not None:
        since_id = last_quote.dm_id
        params["since_id"] = since_id

    res = api.get(url, params=params)

    if res.status_code == 200:
        dms = json.loads(res.text)
        for dm in dms:
            id = dm['id']
            text = dm['text']
            sender = dm['sender_screen_name']
            user = db.session.query(User).filter(User.username==sender)\
                    .first()

            if '@meibun' in text and user:
                print(text)
                parts = text.split(',')
                if len(parts) > 1:
                    main_text = parts[1]
                if len(parts) > 2:
                    author = parts[2]
                if len(parts) > 3:
                    book = parts[3]
                date = datetime.datetime.now()
                q = db.session.query(Quote).filter(Quote.text==main_text).first()
                if q is None:
                    q = Quote(main_text, author, book, user.id, date)
                    db.session.add(q)
                    db.session.commit()
    else:
        print('failed', res.status_code)


if __name__ == "__main__":
    #アクセス用
    CK = os.environ["CONSUMER_KEY"]
    CS = os.environ["CONSUMER_SECRET"]
    AT = os.environ["ACCESS_TOKEN_KEY"]
    ATS = os.environ["ACCESS_TOKEN_SECRET"]

    #名言を登録
    quote_register(CK, CS, AT, ATS)

    #ツイート
    tweet(CK, CS, AT, ATS)
