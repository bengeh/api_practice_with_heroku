from app import application, engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import *
from flask import request, jsonify, Response
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import Session
from flask_cors import CORS, cross_origin
import json

CORS(application, support_credentials=True)
Base = automap_base()
Base.prepare(engine, reflect=True)
print("inside routes....")
print(Base)
print(Base.classes)
Accounts = Base.classes.account
Posts = Base.classes.posts
print(Accounts)
print(Posts)
session = Session(engine)
metadata = MetaData(engine)


@application.route('/index')
@application.route('/')
def index():
    return 'Welcome to this page'


@application.route('/register', methods=["GET", "POST"])
def register():
    username = request.args.get('username')
    password = request.args.get('password')
    password_hash = generate_password_hash(password)
    account = Table('account', metadata, autoload=True)
    engine.execute(account.insert(), username=username, password=password_hash)
    return jsonify({'user_added': True})


@application.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    username_entered = request.args.get('username')
    password_entered = request.args.get('password')
    user = session.query(Accounts).filter(or_(Accounts.username == username_entered)
                                          ).first()
    if user is not None and check_password_hash(user.password, password_entered):
        return jsonify({'signed_in': True})
    return jsonify({'signed_in': False})

@application.route('/create_post', methods=["GET", "POST"])
def create_post():
    post_title = request.args.get("title")
    post_text = request.args.get("post_text")
    post = Table('posts', metadata, autoload=True)
    engine.execute(post.insert(), post_name=post_title, post_text=post_text)
    return jsonify({'post_added': True})

@application.route('/get_one_post', methods=["GET", "POST"])
def get_one_post():
    post_name = request.args.get('post_name')
    post = session.query(Posts).filter(or_(Posts.post_name == post_name)).first()
    print("got the post...")
    print(post)
    if post is not None:
        data = {'post': post}
        resp = Response(json.dumps(data), status=200, mimetype="application/json")
        return resp
    else:
        return jsonify({"error": True})

# @application.route('get_all_post', methods=["GET", "POST"])
# def get_all_post():
#     post_by = request.args.get('username')
#     posts = session.query(Posts).filter(or_(post_name))