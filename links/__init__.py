from apps import mylink

from flask_sqlalchemy import SQLAlchemy

mylink.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proto.db'
mylink.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(mylink)
with mylink.app_context():
    db.create_all()
