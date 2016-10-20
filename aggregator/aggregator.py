from __future__ import print_function
import httplib2
import os
import sys
import base64
import urllib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from config import *

from models import Links, Base, Config
from sqlalchemy import create_engine

from datetime import datetime
import time
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def create_session():
    global session
    global config_session

    engine = create_engine(SQLITE_DB, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    config_session = session.query(Config)

def commit_rollback():
    try:
        session.commit()
    except:
        session.rollback()

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'mylink.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
    return credentials

def get_title(url):
    title = url
    try:
        url_fd = urllib2.urlopen(url)
        content = url_fd.read()
        soup = BeautifulSoup(content, "html.parser")
        try:
            title = soup.html.find('title').text
        except:
            tmp = urllib2.urlparse.urlsplit(urllib2.urlparse.unquote(url))[2]
            title = tmp.split("/")[-1]
    except:
        title = False
    return title

def db_add_url(url, msg_time=None):
    title = get_title(url)
    if not title:
        print("Url: " + url + " Time: " + str(msg_time) + " Status: False")
        return False

    l = Links(link=url, title=title, updated=msg_time)
    session.add(l)
    commit_rollback()
    print("Url: " + url + " Time: " + str(msg_time) + " Status: True")
    return True

def create_service():
    service = None
    try:
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
    except:
        pass
    return service

def get_config(arg):
    conf_lu = config_session.first()
    if not conf_lu:
        return None
    elif arg == "mta":
            return conf_lu.last_updated_after
    elif arg == "mtb":
            return conf_lu.last_updated_before

def extract_date(msg):
    timestamp = None
    for header in msg['payload']['headers']:
        if header['name'] == "Date":
            timestamp = datetime.strptime(header['value'], "%a, %d %b %Y %X +%f")
    return timestamp

def get_message(service, time_before, time_after, subject="Links"):
    final_list = []
    if time_before:
        time_before_epoch = time.mktime(time_before.timetuple())
        time_after_epoch = time.mktime(time_after.timetuple())
        query = "subject:%s before:%d" % (subject, time_before_epoch)
        results = service.users().messages().list(userId='me', q=query).execute()
        final_list.extend(results.get("messages", []))
        query = "subject:%s after:%d" % (subject, time_after_epoch)
        results = service.users().messages().list(userId='me', q=query).execute()
        final_list.extend(results.get("messages", []))
    else:
        query = "subject:%s" % (subject)
        final_list = service.users().messages().list(userId='me', q=query).execute()
        final_list = final_list.get("messages", [])
    return final_list

def update_time(time_before, time_after):
    conf_lu = config_session.first()
    if conf_lu:
        conf_lu.last_updated_after = time_after
        conf_lu.last_updated_before = time_before
    else:
        conf_lu = Config(last_updated_after=time_after, last_updated_before=time_before)
        session.add(conf_lu)
    commit_rollback()

def decode(string):
    return base64.urlsafe_b64decode(string.encode('ASCII'))

def main():
    service = create_service()
    if not service:
        print("ERROR in connection. Exiting")
        sys.exit(1)

    create_session()
    time_before = get_config("mtb")
    time_after = get_config("mta")
    msgs = get_message(service, time_before, time_after)
    
    for m in msgs:
        message = service.users().messages().get(userId='me', id=m['id']).execute()
        parts = message['payload']['parts']
        msg_time = extract_date(message)

        for p in parts:
            if p['mimeType'] == "text/plain":
                msg_str = decode(p['body']['data'])
                url_list = msg_str.splitlines()
                for u in url_list:
                    db_add_url(u, msg_time)

        if not time_before and not time_after:
            time_before = time_after = msg_time
        else:
            if msg_time < time_before:
                time_before = msg_time
            else:
                time_after = msg_time 

        update_time(time_before, time_after)
    update_time(time_before, datetime.today())

if __name__ == '__main__':
    main()
