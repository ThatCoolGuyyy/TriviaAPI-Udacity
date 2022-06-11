## Full Stack Trivia API Project



This trivia project allows a user to play a trivia game to test their knowledge on general knowledge concepts. By Using this application, the user is able to:
1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started
### Install Dependencies
Dependencies for this project include Pip, Python, Npm and Node.js.
### Frontend Dependencies
Find and download Node and Npm using this [link](./https://nodejs.com/en/download).

This project uses Npm to manage software dependencies. Npm Relies on the package.json file located in the frontend directory of this repository.

`npm install`
### Backend Dependencies
First thing to do is to startup your virtual environment and once that is up and running, navigate to the backend directory and run the following command:

`pip install -r requirements.txt`

# API Reference

## Error Handling
Errors are returned in the folowing JSON format:
```
{
    "error": 404,
    "message": "resource not found",
    "success": false
}
```
The API returns 5 types of errors:

- 400: bad request
- 404: resource not found
- 405: method not allowed
- 422: unprocessable
- 500: internal server error
## Endpoints
#### GET '/categories'
- This endpoint fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Example `curl http://127.0.0.1:5000/categories`
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```
#### GET '/questions'
- This endpoint fetches all the questions in the database with a pagination of 10 questions per page.
- Example `curl http://127.0.0.1:5000/questions`
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 18
}
```
#### GET '/categories/<int:id>/questions'
- This endpoint gets questions by category id using url parameters and returns a JSON object. It also returns the total number of questions in the category.
- Example `curl http://127.0.0.1:5000/categories/2/questions`
```
{
    "current_category": "Art",
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true,
    "total_questions": 4
}
```
#### DELETE '/questions/<int:id>'
- This endpoint deletes a question with the matching id, it also returns the ID of the question that was deleted upon successful deletion.
- Example `curl -X DELETE http://127.0.0.1:5000/questions/2`
```
{
    "deleted": 2,
    "success": true
}
```
#### POST '/questions'
- This endpoint creates a new question and returns the ID of the question that was created upon successful creation.
- Example `curl -X POST -H "Content-Type: application/json" -d '{"question": "Who invented the electricity?", "answer": "Benjamin Franklin", "category": "4", "difficulty": "3"}' http://127.0.0.1:5000/questions`
```
{
    "created": 26,
    "success": true
}
```
#### POST '/questions/search'
- This endpoint searches for questions based on the search term and returns a JSON object.
- Example `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Butter"}' http://http://127.0.0.1:5000/questions/search`

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```
#### POST '/quizzes'
- This endpoint creates a new quiz and returns the ID of the quiz that was created upon successful creation.
- Example `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [6, 4], "quiz_category": {"type": "History", "id": "2"}}' http://127.0.0.1:5000/quizzes`
```

## Author and Acknowledgements
- Oshungboye Oluwadamilola authored the API (app.py), test suite (test_flaskr.py), and this README.
All other project files, including the models and frontend, were created by Udacity as a project template for the Full Stack Web Developer Nanodegree.
