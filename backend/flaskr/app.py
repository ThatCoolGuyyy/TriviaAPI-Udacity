import os
from unicodedata import category
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
        
        if category is None:
            abort(404)
        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in category}
        })
    

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        category = Category.query.all()

        if len(current_questions) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {category.id: category.type for category in category},
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
            abort(404)

    @app.route('/questions', methods=['POST'])
    def create_new_question():
        body = request.get_json()

        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')

        if new_question is None or new_answer is None or new_category is None or new_difficulty is None:
            abort(422)
        try:
            category = Category.query.all()
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert()
            return jsonify({
                'success': True,
                'created': question.id,
    
            })
        except:
            abort(422)
            

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm')
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': {category.id: category.type for category in Category.query.all()}
            }), 200
    
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_by_category(id):
        get_categories = Category.query.get(id)
        questions = Question.query.join(Category, Category.id == Question.category).filter(Category.id == id).all()
        current_questions = paginate_questions(request, questions)
        
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': get_categories.type,
            }), 200

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        body = request.get_json()
        previousQuestion = body.get('previous_questions')
        category = body.get('quiz_category')
        if previousQuestion is None or category is None:
            abort(422)
        if (category['id'] == 0):
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category['id']).all()

        def random_question():
            next_question = questions[random.randrange(0, len(questions), 1)]
            return next_question

        def check_if_question_used(question):
            used = False
            for q in previousQuestion:
                if (q == question.id):
                    used = True

            return used

        question = random_question()

    
        while (check_if_question_used(question)):
            question = random_question()

            if (len(previousQuestion) == len(questions)):
                return jsonify({
                    'success': True
                })

    
        return jsonify({
            'success': True,
            'question': question.format()
        })

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
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500
   
    return app

