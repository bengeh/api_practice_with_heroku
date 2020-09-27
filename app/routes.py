from app import application, engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import *
from flask import request, jsonify, Response
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import Session
from flask_cors import CORS, cross_origin
import json
from flask import make_response


CORS(application, support_credentials=True)
Base = automap_base()
Base.prepare(engine, reflect=True)
print("inside routes....")
print(Base)
print(Base.classes)
Accounts = Base.classes.accounts
Posts = Base.classes.posts
Comments = Base.classes.comments
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
    account = Table('accounts', metadata, autoload=True)
    engine.execute(account.insert(), user_name=username, password=password_hash)
    return jsonify({'user_added': True})


@application.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    print("signing in....")
    username_entered = request.args.get('username')
    password_entered = request.args.get('password')
    user = session.query(Accounts).filter(or_(Accounts.user_name == username_entered)
                                          ).first()
    if user is not None and check_password_hash(user.password, password_entered):
        print("user is not none...")
        return jsonify({'signed_in': True})
    print("signed in false...")
    return make_response(jsonify({'signed_in': False}), 403)

@application.route('/create_post', methods=["GET", "POST"])
def create_post():
    if sign_in().status_code == 200:
        post_created_by = request.args.get("post_created_by")
        post_title = request.args.get("post_title")
        post_text = request.args.get("post_text")
        post = Table('posts', metadata, autoload=True)
        engine.execute(post.insert(), user_name=post_created_by, post_title=post_title, post_text=post_text)
        return jsonify({'post_added': True})
    else:
        return jsonify({'error': "No credentials given. Try logging in"})

@application.route('/get_post', methods=["GET", "POST"])
def get_one_post():
    if sign_in().status_code == 200:
        post_name = request.args.get('post_name')
        posts = session.query(Posts).filter(or_(Posts.post_title == post_name)).all()
        if posts is not None:
            for u in posts:
                print(u.__dict__.get("post_title"))
                return jsonify({
                    "user_name": u.__dict__.get("user_name"),
                    "post_title": u.__dict__.get("post_title"),
                    "post_text": u.__dict__.get("post_text"),
                    "post_created_time": u.__dict__.get("post_created")
                })
    else:
        return jsonify({"error": "No credentials given. Try logging in"})

@application.route('/add_comments', methods=["GET", "POST"])
def add_comments():
    if sign_in().status_code == 200:
        user_name = request.args.get('user_name')
        post_title = request.args.get('post_title')
        comment_text = request.args.get('comment_text')
        comment = Table('comments', metadata, autoload=True)
        engine.execute(comment.insert(), user_name=user_name, post_title=post_title, comment_text=comment_text)
        return jsonify({'comment_added': True})
    else:
        return jsonify({"error": "No credentials given. Try logging in"})

# {

#     "post_title": "hello test",
#     "comments": [
#             {
#                 "user_name": "jack", 
#                 "comment_text": "this is a test comment 1234"
#             },
#             {
#                 "user_name": "ben", 
#                 "comment_text": "this is a test comment 1234",
#             },
            
#     ]
    
# }


@application.route('/get_comments', methods=["GET", "POST"])
def get_comments():
    if sign_in().status_code == 200:
        post_title = request.args.get('post_title')
        posts = session.query(Comments).filter(or_(Comments.post_title == post_title)).distinct().all()
        if posts is not None:
            comments = []
            for u in posts:
                commentsMap = {}
                print(u.__dict__.get("post_title"))
                print(u.__dict__.get("comment_text"))
                print(u.__dict__.get("user_name"))
                commentsMap["user_name"] = u.__dict__.get("user_name")
                commentsMap["comment_text"] = u.__dict__.get("comment_text")
                comments.append(commentsMap)
            return jsonify({
                "post_title": u.__dict__.get("post_title"),
                "comments": comments
            })

    else:
        return jsonify({"error": True})