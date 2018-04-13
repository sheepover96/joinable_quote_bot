# -*- coding: utf-8 -*-

import os, json
import datetime, random
from flask_sqlalchemy import SQLAlchemy

from requests_oauthlib import OAuth1Session
import twitter
import urllib.request, urllib.parse

from app import db
from app import User, Quote

SPLITTER = '::'
QUOTE_REGISTER = '@meibun'
USER_REGISTER = '@sanga'


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
        quote = None
        while quote is None:
            rand_id = random.randint(1, nquotes) + 1
            quote = db.session.query(Quote).get(rand_id)

        url = "https://api.twitter.com/1.1/statuses/update.json"
        api = OAuth1Session(CK,CS,AT,ATS)

        author = "不明"
        if quote.author is not None:
            author = quote.author

        book = "不明"
        if quote.book is not None:
            book = quote.book

        text = quote.text + '\n' +  '作者: ' + author + '\n' + '作品:「' + book + '」'

        params = {
                "status": text
                }


        res = api.post(url, params)

def register(CK, CS, AT, ATS):
    url = "https://api.twitter.com/1.1/direct_messages.json"
    api = OAuth1Session(CK, CS, AT, ATS)
    params = {'full_text': True}

    last_quote = db.session.query(Quote).order_by(Quote.id.desc()).first()
    last_user = db.session.query(User).order_by(User.dm_id.desc()).first()

    if last_quote is not None and last_user is not None:
        since_quote_id = last_quote.dm_id
        since_user_id = last_user.dm_id
        since_id = min([since_quote_id, since_user_id])
        params["since_id"] = since_id


    res = api.get(url, params=params)

    if res.status_code == 200:
        dms = json.loads(res.text)
        for dm in dms:
            id = int(dm['id'])
            text = dm['text']
            sender = dm['sender_screen_name']
            user = db.session.query(User).filter(User.username==sender)\
                    .first()

            if USER_REGISTER in text and user is None:
                date = datetime.datetime.now()
                user = User(sender, date, id)
                db.session.add(user)
                db.session.commit()

            if QUOTE_REGISTER in text and user:
                print(text)
                parts = text.split(SPLITTER)
                main_text = None
                author = None
                book = None
                if len(parts) > 1:
                    main_text = parts[1]
                if len(parts) > 2:
                    author = parts[2]
                if len(parts) > 3:
                    book = parts[3]
                date = datetime.datetime.now()
                if main_text is not None:
                    q = db.session.query(Quote).filter(Quote.text==main_text).first()
                    if q is None:
                        q = Quote(main_text, author, book, user.id, id, date)
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
    register(CK, CS, AT, ATS)

    #ツイート
    tweet(CK, CS, AT, ATS)
