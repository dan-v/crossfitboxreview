from app import db
from sqlalchemy import *
from sqlalchemy.exc import IntegrityError

class Affiliate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.String(50), nullable=False)
    reviews = db.relationship('Review', backref = 'review', lazy = 'dynamic')
    
    def __repr__(self):
        return '<Affiliate %r>' % (self.name)    

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    affiliate_id = db.Column(db.Integer, db.ForeignKey('affiliate.id'))
    ipaddress = db.Column(db.String(20), nullable=False)
    rating_overall = db.Column(db.Integer, nullable=False)
    rating_equipment = db.Column(db.Integer, nullable=False)
    rating_instructor = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    review_date = db.Column(db.DateTime, nullable=False)
    __table_args__ = (
            UniqueConstraint("affiliate_id", "ipaddress"),
        )

    def __repr__(self):
        return '<Review %r>' % (self.comment)

