from flask import request
from flask_restful import Resource
from Model import db, Article, ArticleSchema

articles_schema = ArticleSchema(many=True)
article_schema = ArticleSchema()

class ArticleResource(Resource):
    def get(self):
        articles = Article.query.all()
        articles = articles_schema.dump(articles).data
        return {'status': 'success', 'data': articles}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = article_schema.load(json_data)
        if errors:
            return errors, 422
        article = Article.query.filter_by(title=data['title']).first()
        if article:
            return {'message': 'Article already exists'}, 400
        article = Article(
            title=json_data['title']
            )

        db.session.add(article)
        db.session.commit()

        result = article_schema.dump(article).data

        return { "status": 'success', 'data': result }, 201    

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No article data provided'}, 400
        # Validate and deserialize input
        data, errors = article_schema.load(json_data)
        if errors:
            return errors, 422
        article = Article.query.filter_by(id=data['id']).first()
        if not article:
            return {'message': 'Article does not exist'}, 400
        article.title = data['title']
        db.session.commit()

        result = article_schema.dump(article).data

        return { "status": 'success', 'data': result }, 204    

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No article data provided'}, 400
        # Validate and deserialize input
        data, errors = article_schema.load(json_data)
        if errors:
            return errors, 422
        article = Article.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = article_schema.dump(article).data

        return { "status": 'success', 'data': result}, 204    