from models import Feedback, db, User
from app import app



db.drop_all()
db.create_all()

User.query.delete()
Feedback.query.delete()