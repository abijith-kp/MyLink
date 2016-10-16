from flask import jsonify, render_template, request, flash, redirect, url_for, jsonify
from datetime import datetime
import random

from apps import links_app
from models import Links
from . import db

#session = create_session()
# session = create_session("sqlite:///proto.db")
PAGE_SIZE = 10

@links_app.route("/", methods=["GET"])
def index():
    return render_template("urls.html")

@links_app.route("/analytics", methods=["POST", "GET"])
def analytics():
    return render_template("index.html")

@links_app.route("/del/<string:uuid>", methods=["GET"])
def delete_link(uuid):
    l = Links.query.filter_by(uuid=uuid).delete()
    db.session.commit()
    print l
    return str(l)

@links_app.route("/update/<string:uuid>", methods=["GET"])
def update_link(uuid):
    args = request.args
    print args
    result = Links.query.all()
    l = Links.query.filter_by(uuid=uuid).first()
    l.title = args.get('title', l.title)
    db.session.commit()
    print l, l.link, l.title
    return ""

@links_app.route("/url", methods=["POST", "GET"])
def url():
    args = request.args
    print args
    page = int(args.get('page', 1))
    result = Links.query.limit(PAGE_SIZE).offset((page - 1) * PAGE_SIZE)
    #result = Links.query.all()
    print "selected all the table"
    return jsonify({r.uuid:[r.link, r.title]    for r in result})

@links_app.route("/random", methods=["GET"])
def random_url():
    count = Links.query.count()
    rand = random.randrange(1, count)
    l = Links.query.filter_by(id=rand).first()
    try:
        print l.link
        return jsonify({"link": l.link})
    except:
        return random_url()
        
