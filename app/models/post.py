from datetime import datetime
from ..extensions import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)           
    organizer = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))    
    subject = db.Column(db.String(250))
    participants = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)


