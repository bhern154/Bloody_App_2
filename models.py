from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP 

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Post Model"""
    __tablename__ = 'user_tb'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(30),
                     nullable=False)
    
    last_name = db.Column(db.String(30),
                     nullable=False)

    image_url = db.Column(db.String(30), default='https://cdn-icons-png.flaticon.com/512/9131/9131529.png')
           
class Post(db.Model):
    """Post Model"""
    __tablename__ = "post_tb"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(TIMESTAMP)
    user_id = db.Column(db.Text, db.ForeignKey('user_tb.id'))

    user = db.relationship('User', backref='post_tb')
