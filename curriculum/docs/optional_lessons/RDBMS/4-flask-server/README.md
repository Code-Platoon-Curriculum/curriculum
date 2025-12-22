# Flask + PostgreSQL (Models and Views)

## What are we trying to accomplish?

By learning the topics encompassing SQL schema and relationships, creating a Flask server, understanding views and API views, connecting Flask to PostgreSQL, comprehending models, creating them, and interacting with them through API views while passing arguments via URLs, one aims to gain a comprehensive understanding of building robust web applications with Flask and PostgreSQL integration. This journey encompasses understanding the fundamental structure of databases, creating a backend server with Flask, defining routes and views to handle client requests, integrating Flask with PostgreSQL for data storage, modeling data with SQLAlchemy, and leveraging advanced querying techniques to retrieve and manipulate data. Furthermore, exploring the limitations and complexities of this approach compared to Django sheds light on the necessity of considering alternative frameworks for more extensive database modeling and complex relationship management, emphasizing Django's integrated solutions for handling tables as models, enforcing constraints, managing relationships, and simplifying data serialization and URL parameter handling. Overall, mastering these concepts empowers developers to architect scalable, efficient, and maintainable web applications tailored to diverse requirements and challenges.

## Lectures and Assignments

- [Lecture - Flask + PostgreSQL](./1-flask-postgresql.md)
- [Lecture - Models and URL Params](./2-models-urlparams.md)

## TLO's (Terminal Learning Objectives)

- N/a these topics will not be tested within Code Platoon

## ELO's (Enabling Learning Objectives)

- Connect Flask to PostgreSQL using a URI
- Creating Models with SQL Alchemy
- Interact with Models through API views
- Passing arguments through urls `api/v1/<name>`
- Using SQL Alquemy to query Databasis
  - .all()
  - .first()
  - .get()
  - .filter_by(field=arg).all()
  - .filter(model.field.like()).all()
- What are we missing and why Django?
