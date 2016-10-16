from flask import jsonify, render_template, request, flash, redirect, url_for, jsonify
from datetime import datetime

from apps import links_app
from models import *
from . import db

#session = create_session()
session = create_session("sqlite:///proto.db")
PAGE_SIZE = 10

@links_app.route("/", methods=["GET"])
def index():
    return render_template("urls.html")

@links_app.route("/analytics", methods=["POST", "GET"])
def analytics():
    return render_template("index.html")

@links_app.route("/del/<string:uuid>", methods=["GET"])
def delete_link(uuid):
    l = session.query(Links).filter_by(uuid=uuid).delete()
    session.commit()
    print l
    return str(l)

@links_app.route("/update/<string:uuid>", methods=["GET"])
def update_link(uuid):
    args = request.args
    print args
    result = session.query(Links).all()
    l = session.query(Links).filter_by(uuid=uuid).first()
    l.title = args.get('title', l.title)
    session.commit()
    print l, l.link, l.title
    return ""

@links_app.route("/url", methods=["POST", "GET"])
def url():
    #args = request.args
    #print args
    #page = int(args.get('page', 1))
    # result = session.query(Links).all()
    #result = session.query(Links).limit(PAGE_SIZE).offset((page - 1) * PAGE_SIZE)
    result = session.query(Links.uuid, Links.link, Links.title).all()
    # print jsonify([{"link":r.link, "updated":datetime.strftime(r.updated, "%a, %d %b %Y %X +%f")}    for r in result])
    #print [{"link":r.link, "title":r.title}    for r in result]
    print "selected all the table"
    return jsonify({r.uuid:[r.link, r.title]    for r in result})
    #return jsonify({r.link:datetime.strftime(r.updated, "%a, %d %b %Y %X +%f")    for r in result})
