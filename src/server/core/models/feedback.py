from enum import unique

from flask_sqlalchemy import SQLAlchemy 

from core.extensions import db

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    
    src_lang = db.Column(db.String(20), nullable=False)
    tgt_lang = db.Column(db.String(20), nullable=False)
    input = db.Column(db.String(800), nullable=False, unique=False)
    review = db.Column(db.String(800), nullable=False, unique=False)
    stars = db.Column(db.Integer, nullable=True, unique=False)    
    token = db.Column(db.String(20), nullable=False)

    created_at = db.Column(db.DateTime(), nullable=False,\
                                server_default=db.func.now())
    update_at = db.Column(db.DateTime(), nullable=False,\
                                server_default=db.func.now(), onupdate=db.func.now())

    # TODO We need to decide how we deal with duplicate on the review saving
    # __table_args__ = (
    #     # this can be db.PrimaryKeyConstraint if you want it to be a primary key
    #     db.UniqueConstraint('input', 'review', 'stars'),)
      

    def save(self):
        db.session.add(self)
        db.session.commit()