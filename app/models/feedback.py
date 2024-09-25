from datetime import datetime
from ..extensions import db

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)        
    author = db.Column(db.Integer)
    post_author_id = db.Column(db.Integer)        
    post_id = db.Column(db.Integer)
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)