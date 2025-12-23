# Flask Models and Responsive URL's

## What is a Model?

In the context of web development, a model represents the structure of the data in the application. It defines how data is stored, accessed, and manipulated within the application. In Flask, models are typically defined using SQLAlchemy, which provides an ORM (Object-Relational Mapping) to interact with databases.

## Creating Models

Models in Flask are created using SQLAlchemy's declarative syntax. Each model class corresponds to a table in the database, with class attributes representing columns. Let's take a look at an example:

```python
class Genre(db.Model):
    genre_id = db.Column(db.Integer(), primary_key=True)
    genre_name = db.Column(db.String(20))
```

## Interacting with Models through API Views

API views in Flask allow us to interact with models and retrieve data from the database. We can define routes that correspond to specific endpoints and perform CRUD (Create, Read, Update, Delete) operations on the database. For example, the `all_genres()` function retrieves all genres from the `Genre` table.

## Passing Arguments through Views? `api/v1/<name>`

Flask allows us to define routes that accept parameters in the URL. We can pass arguments through views to filter data based on specific criteria. For instance, the `get_employee_by_partial_name()` function retrieves employees whose names contain a certain substring specified in the URL.

## Methods for Querying Models

In SQLAlchemy, we have several methods for querying models to retrieve data from the database:

- `.all()`: Retrieves all records from the table.
- `.first()`: Retrieves the first record from the table.
- `.get()`: Retrieves a record by its primary key.
- `.filter_by(field=arg).all()`: Filters records based on a specific field value.
- `.filter(model.field.like()).all()`: Filters records using pattern matching.

## What are we Missing and Why Django?

Despite the power and flexibility of Flask, there are certain features that may be missing or require additional implementation compared to other frameworks like Django. In Django, several concepts are more seamlessly integrated:

- Tables = Models
- Constraints = Validators
- Many-to-one = ForeignKey
- One-to-one = OneToOne
- Many-to-many = ManyToMany
- Serializers utilized to interpret querysets into JSON data
- URL parameter reinforcement

Django provides built-in support for these features, simplifying the development process for complex applications.

In conclusion, Flask offers a lightweight and flexible approach to building web applications, allowing developers to tailor solutions to their specific needs. However, for projects requiring extensive database modeling and complex relationships, Django may offer a more comprehensive solution out of the box.

Thank you for attending today's lecture on Flask Models and Responsive URL's. If you have any questions, feel free to ask.