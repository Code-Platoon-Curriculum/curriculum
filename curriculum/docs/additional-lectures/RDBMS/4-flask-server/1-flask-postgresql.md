# Flask and PostgreSQL

## Introduction

Welcome to today's lecture on integrating Flask with PostgreSQL. In this session, we will explore the process of connecting a Flask server to a PostgreSQL database, enabling you to build powerful web applications with robust data storage capabilities.

## Review of SQL Schema and Relationships

![schema](./resources/schema.png)

Before delving into Flask and PostgreSQL integration, let's briefly review SQL schema and relationships. SQL, or Structured Query Language, is a standard language for interacting with relational databases. A schema represents the structure of the database, including tables, fields, and relationships between them. In our example, we have tables such as `game`, `genre`, and `employee`, each with its own set of fields and relationships defined through foreign keys.

## Review Creating a Flask Server

Flask is a micro web framework for Python, designed for building web applications quickly and with minimal boilerplate code. Let's take a quick look at how to create a basic Flask server:

```python
from flask import Flask

app = Flask('app')

@app.route('/')
def index():
    return 'Hello, World!'

app.run(debug=True, port=8000)
```

## What are Views?

In Flask, views are the functions that respond to requests from clients. These views are mapped to specific URLs and HTTP methods using decorators. For example, the `@app.route('/')` decorator in the previous code snippet binds the `index()` function to the root URL.

## Review Creating an API View

API views in Flask are similar to regular views but are specifically designed to return data in a format suitable for consumption by other applications. This often means returning data in JSON format. Here's an example of creating an API view in Flask:

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    data = {'key': 'value'}
    return jsonify(data)

app.run(debug=True, port=8000)
```

## Connecting Flask to PostgreSQL Using a URI

Now, let's connect our Flask application to a PostgreSQL database using a URI. We will utilize SQLAlchemy, a popular SQL toolkit and Object-Relational Mapping (ORM) library for Python, to interact with the database. Here's an example of connecting Flask to PostgreSQL:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://username:password@localhost:port/database_name'
db = SQLAlchemy(app)
```

## Conclusion


In conclusion, integrating Flask with PostgreSQL opens up a world of possibilities for building dynamic web applications with robust data storage capabilities. By leveraging the power of Flask's simplicity and flexibility along with PostgreSQL's reliability and scalability, you can create applications that meet the needs of modern web development.

Thank you for joining today's lecture on Flask and PostgreSQL. If you have any questions, feel free to ask.
