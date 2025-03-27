from datetime import datetime
from database import db

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    keyword = db.Column(db.JSON)
