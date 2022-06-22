
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    username = db.Column(db.String(20),primary_key=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback', backref='user', cascade='all, delete-orphan')

    

    @classmethod
    def register(cls, username, pwd, email, first, last):
        """Register user w/hashed password & return user"""
        
        hashed = bcrypt.generate_password_hash(pwd)
        
        hashed_utf8 = hashed.decode('utf8')
        
        return cls(username=username, password=hashed_utf8, email=email, first_name=first, last_name=last)


    @classmethod
    def authenticate(cls, username, password):
          """Validate that user exists & password is correct. Return user if valid; else return False."""
          
          u = User.query.filter_by(username=username).first()
          if u and bcrypt.check_password_hash(u.password, password):
              return u
          else:
              return False    
              
    
    def __repr__(self):
        u = self
        return f"<username={u.username} password={u.password} email={u.password} first_name={u.first_name} last_name={u.last_name}>"


class Feedback(db.Model):
    """Feedback model for users"""

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False) 

    """ feedback = db.relationship('User', backref='feedback', cascade='all, delete-orphan') """ 
    
