from apps import links_app

from flask_sqlalchemy import SQLAlchemy

links_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proto.db'
links_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(links_app)
with links_app.app_context():
    db.create_all()
