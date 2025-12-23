from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Genre(db.Model):
    genre_id = db.Column(db.Integer(), primary_key=True)
    genre_name = db.Column(db.String(20))

    def __repr__(self):
        return self.genre_name

class Gaming_engine(db.Model):
    engine_id = db.Column(db.Integer(), primary_key=True)
    engine_name = db.Column(db.String(20))

class Game(db.Model):
    game_id = db.Column(db.Integer(), primary_key=True)
    engine_id = db.Column(db.Integer())
    game_title = db.Column(db.String(255))
    quantity = db.Column(db.Integer())
    price = db.Column(db.types.DECIMAL(5,2))

class Genre_game(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    game_id = db.Column(db.Integer())
    genre_id = db.Column(db.Integer())

class Action_figure(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    action_figure_title = db.Column(db.String(255))
    quantity = db.Column(db.Integer())
    price = db.Column(db.types.DECIMAL(5,2))

class Poster(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    poster_title = db.Column(db.String())
    quantity = db.Column(db.Integer())
    price = db.Column(db.types.DECIMAL(4,2))

class Employee(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    employee_name = db.Column(db.String())
    position = db.Column(db.String())
    salary = db.Column(db.DECIMAL(7,2))

class Social_security(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    employee_id = db.Column(db.Integer())
    ssn = db.Column(db.String(11))

class Shifts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    start_time = db.Column(db.TIMESTAMP())
    end_time = db.Column(db.TIMESTAMP())
    employee_id = db.Column(db.Integer())
