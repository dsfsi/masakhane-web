from enum import unique

from flask_sqlalchemy import SQLAlchemy 

from core.extensions import db

class Language(db.Model):
    __tablename__ = 'language'
    # id = db.Column(db.Integer, primary_key=True)
    src_tgt_dmn = db.Column(db.String(50), primary_key=True)
    source_target_domain = db.Column(db.String(50), nullable=True)
    
    created_at = db.Column(db.DateTime(), nullable=False,\
                                server_default=db.func.now())
    update_at = db.Column(db.DateTime(), nullable=False,\
                                server_default=db.func.now(), onupdate=db.func.now()) 

    def __init__(self, src_tgt_dmn, source_target_domain="") :
        super().__init__()
        self.src_tgt_dmn = src_tgt_dmn
        self.source_target_domain = source_target_domain

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        source, target, domain = self.src_tgt_dmn.split('-')
        return {
            'source': source,
            'target': target,
            'src-tgt_domn' : self.source_target_domain,
            'domain': domain
        }