from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id',db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True)
    img_path = db.Column(db.String)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email  = email

    def __reper__(self):
        return '<User %s>' %self.username
    
        
    def get_id(self):
        return str(self.id)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    
class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())

    owner = db.relationship('User', foreign_keys = user_id)

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    def __repr__(self) -> str:
        return '<Post %s>' % self.id

class Follow(db.Model):
    __tablename__ = 'follow'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    owner = db.relationship('User', foreign_keys = user_id)
    follower = db.relationship('User',foreign_keys = follower_id)


    