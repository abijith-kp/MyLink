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
import datetime as dtime
import time
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
#SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
#CLIENT_SECRET_FILE = 'client_secret.json'
#APPLICATION_NAME = 'Gmail API Python Quickstart'

def create_session():
    global session
    global config_session

    #engine = create_engine('sqlite:////home/abijith/Projects/links/proto.db', echo=False)
    engine = create_engine(SQLITE_DB, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    config_session = session.query(Config)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_title(url):
    title = url
    try:
        r = urllib2.urlopen(url)
        content = r.read()
        soup = BeautifulSoup(content, "html.parser")
        try:
            title = soup.html.find('title').text
        except:
            tmp = urllib2.urlparse.urlsplit(urllib2.urlparse.unquote(url))[2]
            title = tmp.split("/")[-1]
        print("%s %s" % (title, url))
    except Exception, e:
        print("ERROR: %s %s" % (url, e))
    return title

def db_add_url(url, msg_time=None):
    title = get_title(url)
    l = Links(link=url, title=title, updated=msg_time)
    session.add(l)
    try:
        session.commit()
    except Exception, e:
        session.rollback()
        print("ERROR: %s" % (e))

def check_page(url):
    try:
        if url.startswith("http"):
            urllib2.urlopen(url)
            return True
        else:
            return False
    except Exception, e:
        print(e)
        return False

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

def get_today():
    return time.mktime(time.gmtime())

def extract_date(msg):
    msg_time = None
    for h in msg['payload']['headers']:
        if h['name'] == "Date":
            msg_time = datetime.strptime(h['value'], "%a, %d %b %Y %X +%f")
    return msg_time

def get_message2(service, mt_before, mt_after, subject="Links"):
    results = None
    final_list = []
    if mt_before:
        mt_before_epoch = time.mktime(mt_before.timetuple())
        mt_after_epoch = time.mktime(mt_after.timetuple())
        #query = "subject:%s after:%d before:%d" % (subject, mt_after_epoch, mt_before_epoch)
        query = "subject:%s before:%d" % (subject, mt_before_epoch)
        results = service.users().messages().list(userId='me', q=query).execute()
        final_list.extend(results.get("messages", []))
        print(results)
        print(final_list)
        print(query)
        query = "subject:%s after:%d" % (subject, mt_after_epoch)
        results = service.users().messages().list(userId='me', q=query).execute()
        final_list.extend(results.get("messages", []))
        print(query)
        print("Query: subject:%s after:%s before:%s" % (subject, str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mt_after_epoch))), str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mt_before_epoch)))))
        print(final_list)
    else:
        query = "subject:%s" % (subject)
        final_list = service.users().messages().list(userId='me', q=query).execute()
        final_list = final_list.get("messages", [])
        print(final_list)
        print("Query: %s" % (query))
    return final_list

def update_time(mt_before, mt_after):
    conf_lu = config_session.first()
    if conf_lu:
        conf_lu.last_updated_after = mt_after
        conf_lu.last_updated_before = mt_before
    else:
        conf_lu = Config(last_updated_after=mt_after, last_updated_before=mt_before)
        session.add(conf_lu)
 
def main():
    service = create_service()
    if not service:
        print("ERROR in connection. Exiting")
        sys.exit(1)

    create_session()
    mt_before = get_config("mtb")
    mt_after = get_config("mta")
    msgs = get_message2(service, mt_before, mt_after)
    
    #msgs = results.get('messages', [])
    #if not msgs:
    #    print("No Messages")
    #    sys.exit(0)

    url_list = []
    c = 0
    for m in msgs:
        r = service.users().messages().get(userId='me', id=m['id']).execute()
        parts = r['payload']['parts']
        msg_time = extract_date(r)

        for p in parts:
            if p['mimeType'] == "text/plain":
                msg_str = base64.urlsafe_b64decode(p['body']['data'].encode('ASCII'))
                #print(msg_str)
                for u in msg_str.splitlines():
                    if check_page(u):
                        db_add_url(u, msg_time)
                        print("Url: " + u + " Time: " + str(msg_time) + " Status: True")
                    else:
                        print("Url: " + u + " Time: " + str(msg_time) + " Status: False")
                print("\n")

        print(mt_before, mt_after, msg_time)
        if not mt_before and not mt_after:
            mt_before = msg_time
            mt_after = msg_time

        else:
            if msg_time < mt_before:
                mt_before = msg_time
            elif msg_time > mt_after:
                mt_after = msg_time 

        update_time(mt_before, mt_after)
        try:
            session.commit()
        except:
            session.rollback()
            print("Error" + str(e))
        print("TEST...........")
        #break
    update_time(mt_before, datetime.today())
    try:
        session.commit()
    except:
        session.rollback()
        print("Error" + str(e))

if __name__ == '__main__':
    main()
