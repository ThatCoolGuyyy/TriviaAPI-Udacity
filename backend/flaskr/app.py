import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-control-allow-header', 'Content-Type, Authorization')
        response.headers.add('Access-control-allow-methods', 'GET, POST, DELETE, PUT, PATCH, OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        category = Category.query.all()

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in category}
        })
    

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {category.id: category.type for category in Category.query.all()},
        }), 200


    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            }), 200
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_new_question():
        body = request.get_json()

        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')

        try:
            category = Category.query.all()
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            db.session.add(question)
            db.session.commit()
            return jsonify({
                'success': True,
                'created': question.id,
    
            }), 200
        except Exception as error:
            db.session.rollback()
            abort(422)
            

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm')
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        current_questions = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': {category.id: category.type for category in Category.query.all()}
            }), 200
    
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_by_category(id):
        questions = Question.query.filter(Category.id ==  id).all()
        current_questions = paginate_questions(request, questions)
        get_categories = Category.query.get(id)
        category = Category.query.all()
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': get_categories.type,
            # 'categories': {category.id: category.type for category in category}
            }), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405
    
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    

    return app

