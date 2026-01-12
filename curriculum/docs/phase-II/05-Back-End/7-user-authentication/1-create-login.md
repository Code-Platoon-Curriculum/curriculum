# Django Auth & the AbstractUser

## Intro

Today we will learn how to add Users authentication to our API's.

## Django Authentication

Django provides several forms of authentication that can be used to secure your web applications. Each form has its own capabilities, limitations, and scenarios where it is best suited. Let's explore the common forms of authentication in Django:

### 1. Basic Authentication

- **Capabilities**: Basic Authentication is the simplest form of authentication, where the user's credentials (username and password) are sent with each request as a Base64-encoded header (`Authorization: Basic <credentials>`). It is easy to implement and widely supported by browsers.
- **Limitations**: Basic Authentication transmits credentials in plain text, making it susceptible to security risks. It is recommended to use it with HTTPS for secure communication.
- **Scenarios**: Basic Authentication can be suitable for simple internal applications or API endpoints that require minimal security.

### 2. Session Authentication

- **Capabilities**: Session Authentication uses server-side sessions to authenticate users. Upon successful login, a session is created, and a session ID is stored in a cookie on the client-side. Subsequent requests include this session ID for authentication.
- **Limitations**: Session Authentication requires cookies to be enabled on the client-side. It may not be suitable for stateless architectures like RESTful APIs.
- **Scenarios**: Session Authentication is commonly used in web applications that require user-specific functionalities, such as user profiles, shopping carts, or personalized experiences.

### 3. Token Authentication

- **Capabilities**: Token Authentication involves generating a unique token for each user upon login. This token is then used to authenticate subsequent requests by including it in the `Authorization` header (`Authorization: Token <token>`). Tokens can be stored on the client-side (e.g., in local storage or cookies) or provided through an API.
- **Limitations**: Token Authentication requires clients to manage and include the token with each request. It is not suitable for browser-based applications that rely on cookies for authentication.
- **Scenarios**: Token Authentication is commonly used in REST APIs, since Token Authentication requires no server-side "state", and satisifies the "stateless" constraint of REST API's, mobile applications, or scenarios where cross-origin requests are involved.

## The AbstractUser Model

> We will create a subclass of django's built-in `AbstractUser` class. This is a full, functional user model, that we can also extend with custom properties. We'll use this option today to get a balance between convenience and flexibility.

> Let's go ahead and create a trainer_app to manage all of our users/trainers that have accounts on our API. Don't forget to add the app under `INSTALLED_APPS` in the `pokedex_proj/settings.py`

```bash
    python manage.py startapp trainer_app
```

> Now let's enter the `trainer_app/models.py` and create our `Trainer` model that will inherit from AbstractUser

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

# Inheriting from 'AbstractUser' lets us use all the fields of the default User,
# and overwrite the fields we need to change
# This is different from 'AbstractBaseUser', which only gets the password management features from the default User,
# and needs the developer to define other relevant fields.
class Trainer(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # notice the absence of a "Password field", that is built in.
    # django uses the 'username' to identify users by default, but many modern applications use 'email' instead
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.
```

> Since we're not using the default built-in User model, we have to tell django where to find the User we've created.

```python
# pokedex_proj/settings.py
AUTH_USER_MODEL = 'trainer_app.Trainer' #<-- tells our Django Project to utilize the Trainer model
```

> Finally we can `makemigrations` and `migrate` our model into our database. You'll notice an error populate when attempting to `migrate` migrations onto the database. Hopefully, this is a new error that you haven't encountered before. We have added a dependency to a user model to our Django Project that did not exist before. When we try to migrate our migrations our Django project checks the migration history and database to ensure the user model is properly connected, in this case it's not because we are just now adding/changing the user model we want for our project. This means we will have to drop and recreate the database:

```bash
python manage.py makemigrations
dropdb pokedex_db && createdb pokedex_db
python manage.py migrate
python manage.py loaddata moves_data.json
python manage.py loaddata pokemon_data.json
```

## Django Rest Framework Token Authentication

> Django Rest Framework (DRF) provides an additional layer of authentication specifically designed for building APIs. DRF's Token Authentication is a widely-used authentication scheme in Django-based APIs. Let's understand how it works and how it integrates with APIViews for authentication and permission classes.

### Integrating Token Authentication

> First we will need to add both `rest_frameworks` and `rest_framework.authtoken` into our `INSTALLED_APPS` to tell our Django Project that it can reference these two installed apps to grab models and to establish an authentication method.

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.authtoken',
]
```

> Then we will need to specify to `rest_framework` that the only authentication method we want to allow to happen in our application is the TokenAuthentication method.

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

### Token Authentication Workflow

1. User Registration/Login: Upon user registration or login, a unique authentication token is generated for the user.

2. Token Retrieval: The token is provided to the client-side application, either through a JSON response or by storing it in the user's session or local storage.

3. Subsequent Requests: The client includes the token in the `Authorization` header of each request to authenticate the user. The header value follows the format: `Authorization: Token <token>`.

4. Token Verification: DRF checks the validity of the token by matching it with the tokens stored in the database. If the token is valid, the request is considered authenticated.

## User Registration and Logging Functionality

> Now that we've defined our user model by extending `AbstractUser`, we can define APIViews that will leverage DRF's Token based Authentication. Let's create some routes to connect to our `trainer_app` urls and views.

```python
#pokedex_proj.urls

urlpatterns = [
    #.........
    path('api/v1/moves/', include("move_app.urls")),
    path('api/v1/noun/', include("api_app.urls")),
    path('api/v1/users/', include("trainer_app.urls")),
]
```

```python
#trainer_app.urls
from django.urls import path
from .views import Sign_up #, Log_in, Log_out, Info

urlpatterns = [
    path('signup/', Sign_up.as_view(), name='signup'),
    #path("login/", Log_in.as_view(), name="login"),
    #path("logout/", Log_out.as_view(), name="logout"),
    #path("info/", Info.as_view(), name="info")
]
```

> We've just created all of our url endpoints that we will be needing through out the lesson and for our user to accomplish their general functionalities. Next, lets go into creating these views and testing them out.

### User Registration

> The first thing we need to handle is creating a brand new user who comes onto our API. In this segment we will cover all the imports and functions we will need to construct an APIView that will allow users to sign up for our API.

```python
#trainer_app.views
from django.contrib.auth import authenticate, login, logout
from .models import Trainer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class Sign_up(APIView):
    def post(self, request):
        request.data["username"] = request.data["email"]
        trainer = Trainer.objects.create_user(**request.data)
        token = Token.objects.create(user=trainer)
        login(request, trainer)
        return Response(
            {"trainer": trainer.email, "token": token.key}, status=HTTP_201_CREATED
        )
```

> This class-based view (Sign_up) handles the user signup functionality. The post method is executed when an HTTP POST request is made to this view. It retrieves the user data from the request and assigns the email as the username to then create a new user using the `trainer.objects.create_user` method.

> Why `create_user` and not `create` what's the difference? Well `create_user` has a very specific functionality that will `HASH` our users password field when placed into the database (essentially just another layer of security)

> A token is then generated for the user using Token.objects.create. Finally, a JSON response is returned with the trainer's email and token, along with an HTTP 201 Created status.

> Notice that their plain-text password is not included in their record. The password field contains their password hash, which also contains the hashing algorithm and the salt, separated by `$`. Some of the other fields are empty, because they exist by default, but we never set them. Some of the fields will be automatically set by django, however. The fields `date_joined` and `last_login` are updated automatically, like you'd expect. The field `is_active` defaults to True. If you need to delete a user, you should set this to False instead of actually deleting the user. Modern applications rarely permanently delete data, but instead mark items as 'deleted' so that they can be ignored by other queries. Especially for users, it's important to never delete their database record, in case they want to reactivate their account, or if they had connections to other users.

### User Log In

> Now that our users have a way of signing up for our API but we currently don't have a way for them to acquire their token if they aren't signing up. That's where the Log_in method will come into play.

```python


class Log_in(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        trainer = authenticate(username=email, password=password)
        if trainer:
            token, created = Token.objects.get_or_create(user=trainer)
            return Response({"token": token.key, "trainer": trainer.email})
        else:
            return Response("No trainer matching credentials", status=HTTP_404_NOT_FOUND)
```

> This class-based view (Log_in) handles the user login functionality. The post method is executed when an HTTP POST request is made to this view. It retrieves the email and password from the request data and then uses the authenticate function to validate the credentials and retrieve the authenticated trainer object if there are any trainers who match these credentials.

> If the trainer is authenticated, a token is either grabbed or created for the trainer using Token.objects.get_or_create. `get_or_create` returns a tupil with two elements, the first being the object you are looking for and the second a boolean that will state `True` if the item was created and `False` if the item already existed and was grabbed instead of created.

> Finally a JSON response is returned with the token and trainer email if the trainer exists. Otherwise a "No trainer matching credentials" response with an HTTP 404 status is returned.
