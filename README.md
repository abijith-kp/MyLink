MyLink
======

For sometime now, I was planing to create an application which could help with aggregating all the
links that I send to my mail id. I have this habit of sending links/urls of any
interesting things that I find on the internet, something like archiving them
for future reading or reference purposes.

With this idea in mind, here I present [MyLink](https://github.com/abijith-kp/MyLink).
Initially I planned on  doing it as a Single Page Application(as of now this is
the state), so that I have an oppertunity to look into some
[AngularJS](https://angularjs.org/). Along with Angular in the front end I
have used [Flask](http://flask.pocoo.org/) for some REST support in server side.
For database [SQLite](https://sqlite.org/) is used along with
[Flask SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/) for DB management from python
code.



How does it work??
------------------

Initially you just have to email to yourself with all the links in each
separate lines. And also make sure that the subject fo the mail should always be
smae and this subject string is to be configured in the application.

The whole server side work divided among two applications.

One is a regular python script(aggregator) which uses the [Gmail
API](https://developers.google.com/gmail/api/) to collect mails from the
specified gmail account and parse the mails for any urls. Aggregator collects
the mails, verifies if the urls is working and then stores it to the DB.

The second part is a flask web app, which displays all the collected information
and lets you organize them. You could continue reading your filtered articles
or jokes from here now.

> The application also has a funcationality that I have named as
> **SURPRISE ME**, which will redirect you to a link randomly selected from the
> database. This function will help you to read a random article that we had
> ourself hand picked before.



How to install/start the application??
--------------------------------------

##### Step 1: Install the dependencies mentioned in the requirements.txt

```python
pip install -r requirements.txt
```

> Both the aggregator script and web app works independently. So whenever, you
> want to update the DB run the aggregator script. And when you want to see the
> visualization, start the web app.

##### Step 2: Aggregator script

```python
python aggregator.py
```

##### Step 3: MyLink Web application

```python
python wsgi.py
```


Configuration
--------------

* Turn on Gmail API:

In the begining we will have to create a gmail application in google developer site.
You can see the steps [here](https://developers.google.com/gmail/api/quickstart/python).
Create a client_secret.json file and mention the path inside
aggregator/config.py or by default the file from inside aggregator/ directory is
considered.

Please make a point to change the APP_NAME variable also in the config.py to
what you have provided in the Google developer site.

* SQLite databse file path:

There are two places where we need to mention this file name.
One inside aggregator/config.py and another is in links/\_\_init__.py. Provide
same path in both these files. Refer [here](http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlite)
for details on how to provide DB file path.

* IP and port of the server in wsgi.py script inside links/ directory. Change the
values as per what you wanted


How to contribute:
------------------

Just create a pull request. Fell free to provide any kind suggestions. All kinds of inputs
regarding any improvements or new features are highly appreciated.
