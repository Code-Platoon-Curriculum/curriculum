from flask import Flask, jsonify
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
from models import *
import json

app = Flask('server')
# -h localhost -p 5432 -U franciscoavila -d store_db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://franciscoavila@localhost:5432/store_db'

db.init_app(app)


# routes we need a route that will display at index == '/'
@app.route('/', methods=['GET'])
def home():
    return "Hello Whiskey"

@app.route('/api/v1/genres/', methods=['GET'])
def all_genres():
    # SELECT * FROM genre;
    genres = Genre.query.all()
    #SELECT * FROM genre LIMIT 1;
    # print(Genre.query.first())
    json_genres = [{'genre_id': x.genre_id, 'genre_name':x.genre_name} for x in genres]
    #  json_genres = [] 
    #  for x in genres:
    #      genre_dict = {'genre_id': x.genre_id, 'genre_name':x.genre_name}
    #      json_genrese.append(genre_dict)
    return jsonify(json_genres)


# useParams /:id
@app.route('/api/v1/genres/<id>/', methods=['GET'])
def get_genre_by_id(id):
    #SELECT * FROM genre WHERE genre_id = 3;
    genre = Genre.query.get(id)
    json_genre = {'genre_id': genre.genre_id, 'genre_name':genre.genre_name}
    return jsonify(json_genre)

@app.route('/api/v1/employees/<name>/', methods=['GET'])
def get_employee_by_partial_name(name):
# SELECT * FROM employee WHERE employee_name ILIKE '%m%';
    employees = Employee.query.filter(Employee.employee_name.ilike(f'%{name}%')).all()
    json_employees = [
        {
            'id': x.id,
            'employee_name': x.employee_name,
            'position': x.position,
            'salary':x.salary
        }
        for x in employees
    ]
    return jsonify(json_employees)

# route, function, accept a parameter, querydb, return a jsonified response

@app.route('/api/v1/salaries/<salary_in>/', methods = ['GET'])
def get_employees_by_salary(salary_in):
# SELECT * FROM employee WHERE salary > 40000;
    # print(type(salary))
    employees = Employee.query.filter(Employee.salary >int(salary_in)).all()
    json_employees = [
        {
            'id': x.id,
            'employee_name': x.employee_name,
            'position': x.position,
            'salary':x.salary
        }
        for x in employees
    ]
    return jsonify(json_employees)


app.run(debug=True, port=8000)