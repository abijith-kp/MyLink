from flask import jsonify, render_template, request, flash, redirect, url_for, jsonify
from datetime import datetime
import random

from apps import mylink
from models import Links
from . import db

PAGE_SIZE = 10

@mylink.route("/", methods=["GET"])
def index():
    return render_template("urls.html")

@mylink.route("/analytics", methods=["POST", "GET"])
def analytics():
    return render_template("index.html")

@mylink.route("/del/<string:uuid>", methods=["GET"])
def delete_link(uuid):
    l = Links.query.filter_by(uuid=uuid).delete()
    db.session.commit()
    return str(l)

@mylink.route("/update/<string:uuid>", methods=["GET"])
def update_link(uuid):
    args = request.args
    result = Links.query.all()
    l = Links.query.filter_by(uuid=uuid).first()
    if l:
        l.title = args.get('title', l.title)
        db.session.commit()
    return ""

@mylink.route("/url", methods=["POST", "GET"])
def url():
    args = request.args
    page = int(args.get('page', 1))
    result = Links.query.limit(PAGE_SIZE).offset((page - 1) * PAGE_SIZE)
    return jsonify({r.uuid:[r.link, r.title]    for r in result})

@mylink.route("/random", methods=["GET"])
def random_url():
    count = Links.query.count()
    rand = random.randrange(1, count)
    l = Links.query.filter_by(id=rand).first()
    try:
        return jsonify({"link": l.link})
    except:
        return random_url()
