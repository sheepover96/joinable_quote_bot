# -*- coding: utf-8 -*-

import os, json
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request

from requests_oauthlib import OAuth1Session
import twitter

import datetime
import random

# DB接続に関する部分
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# モデル作成
#ユーザモデル
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    date = db.Column(db.DateTime())

    def __init__(self, username, date):
        self.username = username
        self.date = date

    def __repr__(self):
        return '<User %r>' % self.username

#名言モデル
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(200), unique=True)
    author = db.Column(db.String(80), unique=False)
    book = db.Column(db.String(80), unique=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    date = db.Column(db.DateTime())

    def __init__(self, text, author, book, user_id, date):
        self.text = text
        self.author = author
        self.book = book
        self.user_id = user_id
        self.date = date

    def __repr__(self):
        return '<Quote %r>' % self.text


@app.route("/", methods=['POST'])
def register():
    return render_template('base.html')  return render_template('base.html')


@app.route("/user_register", methods=['POST'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        #ユーザが存在するかつ名言がまだないなら追加
        if not db.session.query(User).filter(User.username == username).count():
            date = datetime.datetime.now()
            user = User(username, date)
            db.session.add(user)
            db.session.commit()



@app.route("/quote_register", methods=['POST'])
def quote_register():
    if request.method == 'POST':
        text = request.form['text']
        author = request.form['author']
        book = request.form['book']
        username = request.form['username']
        #ユーザが存在するかつ名言がまだないなら追加
        if not db.session.query(User).filter(User.username == username).count():
            if not db.session.query(Quote).filter(Quote.text == text).count():
                user_id = User.query.filter_by(User.email == email).first().id
                date = datetime.datetime.now()
                quote = Quote(text, author, book, user_id, date)
                db.session.add(quote)
                db.session.commit()



#つぶやき用API
@api.route("/tweet", methods=['POST'])
def tweet():
    quote = None
    nquotes = Quote.query(Quote).all().count()
    if not nquotes:
        rand_id = random.randint(1, nquotes)
        quote = Quote.query(Quote).get(id=rand)

        url = "https://api.twitter.com/1.1/statuses/update.json"
        api = OAuth1Session(consumer_key=os.environ["CONSUMER_KEY"],
                          consumer_secret=os.environ["CONSUMER_SECRET"],
                          access_token_key=os.environ["ACCESS_TOKEN_KEY"],
                          access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
                          )

        text = quote.text + '\n    ~' + quote.author + '\n quoted from ' + quote.book

        params = {
                "status": text
                }

        res = api.post(url, params)


if __name__ == '__main__':
    app.debug = True
    app.run()
