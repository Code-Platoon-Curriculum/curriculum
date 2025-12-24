# Unit Testing in a Github Actions Workspace

Being familiar with unittesting, you'll recall that its advantages revolve around the ease and simplicity at which it can be implemented.

The unittest library is included in a python distribution, eliminating the need for additional installation.  It's a simple, straightforward approach that is suited for smaller projects.  As you scale the size of your application, it may make sense to move on to more powerful, flexible and robusts libraries such as pytest, and eventually even utilizing platforms such as SonarQube.

Today, we'll cover running some basic unit tests for a mock Flask application in a Github Actions Workspace.

## Repository Set Up

You should already be familiar with how to do this through the Github UI, or possibly even the Git CLI.

But did you know there's a [Github CLI](https://cli.github.com/) as well?  The GH CLI was created not to replace the Git CLI, but to complement it.  

```bash

gh repo create # When you run gh repo create, you'll be prompted in your terminal
cd repo-name
```

Repo create is an extremely handy command that initiates an interactive terminal session, prompting you for all the details necessary to create a new repo.

It even clones the repo down for you.  This can be a lot faster than switching between the Github UI and local Git CLI commands.

You can also bypass the prompts completely, if you know all the parameters you need to pass in.  It's a fairly straightforward tool, with a clean and simple [manual](https://cli.github.com/manual/).

## Flask Application Set up

Since Flask is created entirely with Python, we'll want to set up a Python virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

We'll then install flask, flask-sqlalchemy (for MySQL.  Feel free to use a different library if you'd prefer), and flask-login.

```bash
pip install flask flask-sqlalchemy flask-login
```

## Basic File Set Up

We're not going to spend too much time building out the Flask app for now.  We'll only need enough content to write a few simple tests.  A skeleton app will do.

```bash
mkdir project && cd project
code __init__.py main.py auth.py tests.py
```

In our project folder, we'll create these four files.  Since we're just writing a few simple mock tests, you can skip `main.py` and `auth.py` if you'd like, but we're including them here so we can test more than one script and provide some into on Flask Blueprints.

### __init__.py

`__init__.py` in used in order for Python to treat directories containing the file as packages.  This isn't the only way, as you could use a namespace package as well, but that method is more complicated and suited for more complex applications.

```python
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
```

The first thing we do is import the Flask class from the flask module.  We've also included additional code for setting up SQLAlchemy, but it's commented out because we won't be using this today.  The database portion will be covered on Day 3.

```python
def create_app(env='dev'):

  app = Flask(__name__)

  # app.config['SECRET_KEY'] = ''
  # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

  # db.init_app(app)

  if __name__ == '__main__':
    app.run(debug=True)

  return app
```

When defining our method, we can set a default value for the string parameter that it takes in.  We'll use this for the main and auth blueprints, so if you're skipping that portion, you don't need this (though it doesn't hurt to leave in).

What we want this script to do is to instantiate an app object, so we write out a method called create_app.  `app = Flask(__name__)` creates a Flask application object, a datatype that can include functions, methods and attributes.

You may remember `if __name__ == '__main__'` from a previous lesson, so no need to explain that here.  

Notice at the end that we're returning the Flask application object that we created.

From here, we can add some routes.  Mind your indentation, as these need to exist inside the `create_app` method.

```python
  @app.route('/')
  def index():
    return "Index"
  
  @app.route('/profile')
  def profile():
    return "Profile"
```

### Running the App

Remember how we named our main file that funky name?  Since it allows us to treat the directory it's contained in as a package, we'll be able to call the directory using the flask run command.  But first, we'll need to export an environment variable.

```bash

EXPORT FLASK_APP=project 
EXPORT FLASK_DEBUG=1

flask run

```

This approach only applies to your current terminal session.  You can add this export to your virtual environment activate file if you want it to be more permanent.  Otherwise, simply run this command again if you open up a new terminal.

Check that your Flask app is running and that you can access both routes.

### Write Initial Tests

Do you remember how to write unit tests?  As a reminder, it will require a few imports, a class, a method for setting up the test, and a method for each individual test you want to write.

<details>
  <summary>Hint</summary>
  
```python
from __init__ import create_app
import unittest

class Test(unittest.TestCase):
  def setUp(self):
    self.app = create_app('test')
    self.client = self.app.test_client()

  def test_index(self):
    response = self.client.get("/")
    print (response.data)
    self.assertEqual(response.data, b"Index")

if __name__ == '__main__':
  unittest.main()

```

> When writing our test, we use b to convert the string into bytes so that we can compare it against the raw response data.

</details>

Now run your tests and confirm they work.

```bash
python project/tests.py   # if you're at the root directory of your repository
python tests.py           # if you're at the root directory of your application
```

## Set up GH Actions Workflow for simple Flask App

We'll save the main and auth blueprint portions for the end, which we're including to demonstrate additional tests, as well as some quirks revolving around file path relativity.

Let's go ahead and set up a Github Actions Workflow.

```bash
code .github/workflows/push.py
```

### Standard Details

Let's name it, set a trigger, and set permissions.

```yml
name: Flask App

on:
  push:
    branches: [ "main" ]

permissions:
  contents: read
```

### Jobs & Steps

Before we can run our tests, we'll have to set up our environment.  We're going to this by checking out our repo files into the workspace and then setting up Python, and we do all of this using actions.

```yml
jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python 3.12.4
      uses: actions/setup-python@v3
      with:
        python-version: "3.12.4"
    

```

The action `actions/checkout@v4` lets us move over all the files in the repo over to the workspace.

The action `actions/setup-python@v3`, as its name suggests, sets up Python.  We use a `with:` line to specify the version we want to use.  You'll probably want the use the version your interpreter is pointing to in the environment where you're writing your code.

With these actions set up, we can simply pass in commands as additional steps.

```yml
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
```

A few things to note here... We use the pipe character to allow for a multi-line command.

We then use an if expression in shell syntax to prevent an error in case there is no requirements.txt to install.  We also excluded the `pip freeze > requirements` command from the code above to trigger this failure for anyone who is just blazing through the instructions.


```yml
    - name: Run unittests
      run: |
        python project/tests.py
```

With the environment set up, we can call our tests script within the Github Actions Workspace.

<!-- ### Blueprints

tbd -->
