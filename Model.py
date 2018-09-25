from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True nullable=False)
    author = db.Column(db.String(30), nullable=False)
    written_date = db.Column(db.DateTime, nullable=True)
    content = db.Column(db.Text, nullable=False)    
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name):
        self.title = title
        self.author = author
        self.written_date = written_date
        self.content = content
        self.date_posted = date_posted

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)
    article = db.relationship('Article', backref=db.backref('comments', lazy='dynamic' ))

    def __init__(self, comment, article_id, creation_date):
        self.comment = comment
        self.article_id = article_id
        self.creation_date = creation_date

class ArticleSchema(ma.Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    author = fields.String(required=True)
    written_date = fields.DateTime()
    content = fields.String(required=True, minimum=100)
    date_posted = fields.DateTime()
    
class CommentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    article_id = fields.Integer(required=True)
    comment = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()
        