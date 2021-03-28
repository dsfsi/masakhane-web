from enum import unique

from flask_sqlalchemy import SQLAlchemy 

from core.extensions import db

language_list = []

def get_last_id():
    if language_list:
        last_recipe = language_list[-1]
    else:
        # if there is any we initiate 
        # the first recipe having 
        # id of 1
        return 1
    
    # the id of the last recipe + 1(for the new recipe)
    return last_recipe.id + 1


class Language(db.Model):
    __tablename__ = 'language'
    # id = db.Column(db.Integer, primary_key=True)
    # src_tgt = db.Column(db.String(20), nullable=False)

    src_tgt = db.Column(db.String(20), primary_key=True)
    source_target = db.Column(db.String(30), nullable=False)
    domain = db.Column(db.String(30), nullable=True)
    
    created_at = db.Column(db.DateTime(), nullable=False,\
                                server_default=db.func.now())
    update_at = db.Column(db.DateTime(), nullable=False,\
                                server_default=db.func.now(), onupdate=db.func.now()) 

    # TODO We need to decide how we deal with duplicate on the review saving
    __table_args__ = (
        # this can be db.PrimaryKeyConstraint if you want it to be a primary key
        db.UniqueConstraint('src_tgt', 'source_target', 'domain'),) 

    def __init__(self, src_tgt, source_target="", domain="JW300") :
        super().__init__()
        self.src_tgt = src_tgt
        self.source_target = source_target
        self.domain = domain

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        source, target, domain = self.src_tgt, self.source_target, self.domain
        return {
            'source': source,
            'target': target,
            'domain': domain
        }