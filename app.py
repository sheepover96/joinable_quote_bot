# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

from requests_oauthlib import OAuth1Session
import twitter

import os, json
import datetime

# DB接続に関する部分
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/quote_bot'
db = SQLAlchemy(app)

# モデル作成
#ユーザモデル
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    date = db.Column(db.DateTime())
    dm_id = db.Column(db.BigInteger)

    def __init__(self, username, date, dm_id=1):
        self.username = username
        self.date = date
        self.dm_id = dm_id

    def __repr__(self):
        return '<User %r>' % self.username

#名言モデル
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, unique=True)
    author = db.Column(db.String(80), unique=False)
    book = db.Column(db.String(80), unique=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    dm_id = db.Column(db.BigInteger)
    date = db.Column(db.DateTime)

    def __init__(self, text, author, book, user_id, dm_id, date):
        self.text = text
        self.author = author
        self.book = book
        self.user_id = user_id
        self.dm_id = dm_id
        self.date = date

    def __repr__(self):
        return '<Quote %r>' % self.text


@app.route("/")
def register():
    return render_template('base.html')


@app.route("/user_register", methods=['POST'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        #ユーザが存在しないなら追加
        if not db.session.query(User).filter(User.username == username).count():
            date = datetime.datetime.now()
            user = User(username, date)
            db.session.add(user)
            db.session.commit()
            print(user)
    return render_template('base.html')


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
    return render_template('base.html')


if __name__ == '__main__':
    port = os.environ.get("PORT","5000")
    app.run(host='0.0.0.0', port=int(port))
