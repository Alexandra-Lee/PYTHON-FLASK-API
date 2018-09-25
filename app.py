from flask import Flask
from flask import Blueprint
from flask_restful import Api
from resources.Article import ArticleResource
from resources.Comment import CommentResource
from resources.User import UserResource


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(ArticleResource, '/Article')
api.add_resource(CommentResource, '/Comment')
api.add_resource(UserResource, '/User')


