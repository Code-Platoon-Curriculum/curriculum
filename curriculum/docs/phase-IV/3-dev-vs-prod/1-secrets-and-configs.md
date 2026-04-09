# Secrets and Configurations

## Intro

Our application is live. HTTPS is active, traffic is encrypted, and the domain resolves. But stop and look at what we left behind: database passwords sitting in plain text inside `settings.py`, a wildcard `ALLOWED_HOSTS` that lets any server on the internet impersonate a legitimate request, a CORS policy that opens our API to every website ever built, and Docker exposing our database port directly to the internet.

None of these were mistakes during development — they were deliberate shortcuts to keep things moving. Now it's time to close every one of them. This lesson is about the gap between a working application and a *secured* one.

---

## Lesson

### What is Dev vs Prod

Think of a test kitchen at a restaurant. The chefs experiment freely — recipes are written on whiteboards, the walk-in cooler stays unlocked, anyone on the team can taste anything, and no one worries if an experiment fails spectacularly. That openness is what makes the test kitchen productive. But the moment food goes out to paying customers, none of that looseness survives. Recipes become proprietary. The supply chain locks down. Every dish is checked before it leaves the kitchen. What was a feature in the test environment — accessibility, flexibility, visibility — becomes a liability the moment real people and real money are involved.

Software works the same way. A development environment is a test kitchen: open ports, printed credentials, verbose error messages, and permissive configurations keep development fast and debugging easy. A production environment is the restaurant floor: every door is locked, every secret is hidden, and the application should reveal as little as possible about its internals.

Every setting we change in this lesson is closing a door that was intentionally left open during development.

---

### The Importance of our Back-End Server

Open `server/task_proj/settings.py`. Right now it contains several configurations that are appropriate for development but dangerous in production. We'll work through each one.

Before we change anything, add `import os` at the top of the file — we'll be reading every sensitive value from environment variables instead of hardcoding them.

```python
import os
from pathlib import Path
```

#### ALLOWED_HOSTS

`ALLOWED_HOSTS` is a list of domain names and IP addresses that Django considers valid targets for requests arriving at the server. If a request's `Host` header does not appear in this list, Django rejects it outright with a 400 Bad Request before it ever reaches a view.

Right now our setting looks like this:

```python
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '*']
```

The `'*'` is the problem. It tells Django to accept requests claiming to be destined for *any* hostname. This means a bad actor could point crafted requests at our server while spoofing a `Host` header for a completely different domain — a technique used in **HTTP Host Header Attacks** that can bypass security middleware, poison caches, or trigger password-reset emails to attacker-controlled addresses.

In production, `ALLOWED_HOSTS` should list exactly the domains that legitimately serve our application — nothing else:

```python
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
```

In the `.env` file on the server this becomes:

```
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

The `.split(',')` call converts the comma-separated string from the environment into the list Django expects. The default of `'localhost'` means the development environment still works if `ALLOWED_HOSTS` is not set.

#### CORS ALLOW ORIGINS

CORS — **Cross-Origin Resource Sharing** — is the browser mechanism that decides whether a web page loaded from one domain is allowed to make JavaScript requests to a different domain. Our Nginx configuration routes `/api/` requests to Django, but the browser enforces CORS *before* those requests even leave the client machine.

Right now our setting looks like this:

```python
CORS_ALLOW_ALL_ORIGINS = True
```

This tells the `corsheaders` middleware to attach an `Access-Control-Allow-Origin: *` header to every response, which instructs browsers that *any* origin is allowed to call our API. That means a malicious website could make authenticated requests to our API on behalf of a logged-in user.

Replace it with an explicit allowlist:

```python
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost').split(',')
```

In the `.env` file:

```
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

Now the browser will only allow JavaScript from your own domain to communicate with the API. Any other origin gets blocked before the request is sent.

#### Database Configuration

Look at the database block in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'task_db',
        'USER': 'cp_user',
        "PASSWORD": "password",
        'HOST': 'postgres-container',
        'PORT': '5432'
    }
}
```

Every credential is hardcoded. If this file ever makes it into a public repository — even for a moment, even in a commit that was later deleted — those credentials are compromised permanently. Git history is forever. Additionally, the `SECRET_KEY` Django uses for signing sessions and tokens is also hardcoded, and `DEBUG = True` causes Django to render full stack traces in the browser on every unhandled exception.

Replace all three with environment variables:

```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'local-dev-secret-key')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'postgres-container'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

The `.env` file carries all the real values:

```
SECRET_KEY=your-long-random-secret-key-here
DEBUG=False
POSTGRES_DB=task_db
POSTGRES_USER=cp_user
POSTGRES_PASSWORD=a-strong-password-here
DB_HOST=postgres-container
DB_PORT=5432
```

`DEBUG = False` has a critical side effect beyond hiding stack traces: it activates several Django security hardening behaviors, including stricter cookie settings and disabling the browseable API renderer in DRF.

#### Non-Existent URL Patterns

Open `server/task_proj/urls.py`. Right now the URL configuration handles four specific paths and silently falls through to Django's default 404 handler for everything else:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/test/', connection),
    path('api/v1/tasks/', include('task_app.urls')),
    path('api/v1/users/', include('user_app.urls')),
]
```

Django's default 404 handler returns an HTML page — a page full of Django version information and debug hints when `DEBUG = True`, and a barebones "Page not found" HTML document in production. Neither is appropriate for a JSON API. A client application expecting JSON receives HTML it cannot parse, and even the production version reveals that the backend is Django.

Add a catch-all at the end of `urlpatterns` that returns a consistent JSON response:

```python
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse

def connection(request):
    return JsonResponse({"connected": True})

def not_found(request, *args, **kwargs):
    return JsonResponse({"error": "The requested resource was not found."}, status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/test/', connection),
    path('api/v1/tasks/', include('task_app.urls')),
    path('api/v1/users/', include('user_app.urls')),
    re_path(r".*", not_found),
]
```

`re_path(r".*", not_found)` matches any URL that did not match a pattern above it. Because Django evaluates URL patterns in order and stops at the first match, the catch-all must always be last. The result is a predictable JSON 404 response for any unknown path — no HTML, no Django fingerprinting.

#### Managing Views

An unhandled exception inside a view method causes Django to return a 500 Internal Server Error. With `DEBUG = True` that response includes a full stack trace. With `DEBUG = False` it returns a generic HTML error page. In neither case does the client receive a useful JSON response, and in the debug case the server is actively leaking implementation details.

Every view method should be wrapped in a `try/except` block so exceptions are caught and returned as structured JSON. But writing the same `try/except` pattern in every single method violates the **DRY principle** — Don't Repeat Yourself. If we ever need to change how errors are formatted, we'd have to update every method individually.

The DRY solution is a **decorator** — a function that wraps another function, adding behavior before and after it runs. We write the error-handling logic once and apply it with a single line anywhere it's needed.

Create a new file at `server/task_proj/utils.py`:

```python
from functools import wraps
from rest_framework.response import Response
from rest_framework import status as s

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=s.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper
```

`@wraps(func)` preserves the original function's name and docstring so Django's introspection tools still work correctly. The decorator returns either the view's normal response or a clean JSON error — the caller always receives something it can parse.

Now apply it to every view method. In `user_app/views.py`:

```python
from django.contrib.auth import authenticate
from .models import AppUser
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status as s
from task_proj.utils import handle_exceptions

class CreateUser(APIView):
    authentication_classes = []
    permission_classes = []

    @handle_exceptions
    def post(self, request):
        data = request.data.copy()
        data['username'] = data.get('email')
        new_user = AppUser.objects.create_user(**data)
        new_user.full_clean()
        new_user.save()
        token = Token.objects.create(user=new_user)
        return Response({"token": token.key, "email": new_user.email}, status=s.HTTP_201_CREATED)


class LogIn(APIView):
    authentication_classes = []
    permission_classes = []

    @handle_exceptions
    def post(self, request):
        data = request.data.copy()
        data['username'] = data.get('email')
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "email": user.email})
        return Response("No user matching credentials", status=s.HTTP_404_NOT_FOUND)


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class Info(UserView):
    @handle_exceptions
    def get(self, request):
        user = request.user
        return Response({"token": user.auth_token.key, "email": user.email})


class LogOut(UserView):
    @handle_exceptions
    def post(self, request):
        user = request.user
        user.auth_token.delete()
        return Response(f"{user.email} has been logged out")
```

And in `task_app/views.py`:

```python
from user_app.views import UserView
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework import status as s
from django.shortcuts import get_object_or_404, get_list_or_404
from task_proj.utils import handle_exceptions


class AllTasks(UserView):

    @handle_exceptions
    def get(self, request):
        return Response(TaskSerializer(get_list_or_404(request.user.tasks), many=True).data)

    @handle_exceptions
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        ser_task = TaskSerializer(data=data)
        if ser_task.is_valid():
            ser_task.save()
            return Response(ser_task.data, status=s.HTTP_201_CREATED)
        return Response(ser_task.errors, status=s.HTTP_400_BAD_REQUEST)


class ATask(UserView):

    @handle_exceptions
    def get(self, request, task_id):
        return Response(TaskSerializer(get_object_or_404(request.user.tasks, id=task_id)).data)

    @handle_exceptions
    def put(self, request, task_id):
        data = request.data.copy()
        ser_task = TaskSerializer(
            get_object_or_404(request.user.tasks, id=task_id),
            data=data,
            partial=True
        )
        if ser_task.is_valid():
            ser_task.save()
            return Response(ser_task.data)
        return Response(ser_task.errors, status=s.HTTP_400_BAD_REQUEST)

    @handle_exceptions
    def delete(self, request, task_id):
        task = get_object_or_404(request.user.tasks, id=task_id)
        return_string = f"{task.title} has been deleted"
        task.delete()
        return Response(return_string)
```

One decorator, written once, protecting every method. When the error format changes — and it will — there is exactly one place to update it.

---

### Tightening Docker Compose

Open `docker-compose.yml`. Two categories of problems need addressing: **hardcoded credentials** and **exposed ports**.

```yaml
# Current — insecure
services:
  db:
    image: postgres:15
    container_name: postgres-container
    environment:
      - POSTGRES_USER=cp_user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=task_db
    ports:
      - "5433:5432"
  backend:
    build: ./server
    container_name: django-container
    command: sh -c "gunicorn task_proj.wsgi --bind 0.0.0.0:8000 --reload"
    ports:
      - "8000:8000"
    volumes:
      - ./server:/app
    depends_on:
      - db
```

**The credentials problem:** `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` are written in plain text. The Compose file will almost certainly end up in version control — and now so will your database password.

**The port exposure problem:** `"5433:5432"` maps the database's internal port to the host machine. Anyone who can reach the EC2 instance on port 5433 has direct access to the database — no application layer in the way. `"8000:8000"` exposes the Django server directly, bypassing Nginx entirely. Traffic can reach Django without going through the reverse proxy, without HTTPS, and without any of the routing rules Nginx enforces.

Inside a Docker network, containers communicate with each other by service name. Nginx reaches Django by calling `http://backend:8000` and Django reaches Postgres by calling `postgres-container:5432`. These paths never touch the host machine's network. The ports in `docker-compose.yml` are for *external* access only — and for the database and backend, external access should not exist.

Here is the secured version:

```yaml
version: '3.9'

services:
  db:
    image: postgres:15
    container_name: postgres-container
    env_file:
      - .env
  backend:
    build: ./server
    container_name: django-container
    command: sh -c "gunicorn task_proj.wsgi --bind 0.0.0.0:8000"
    env_file:
      - .env
    volumes:
      - ./server:/app
    depends_on:
      - db

  frontend:
    build: ./client
    container_name: nginx-container
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./client/dist:/usr/share/nginx/html
      - ./default.conf:/etc/nginx/conf.d/default.conf
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - backend
```

`env_file: .env` tells Docker Compose to read the `.env` file and inject every variable it contains into the container's environment. The credentials leave the Compose file entirely. Ports for `db` and `backend` are gone — they're only reachable from inside the Docker network now. Only `frontend` exposes ports because Nginx is the intended public entry point.

Note the `--reload` flag was also removed from the Gunicorn command. `--reload` tells Gunicorn to watch the source files and restart workers when they change — a development convenience that adds unnecessary overhead and risk in production.

---

### .gitignore and .dockerignore

Two separate tools prevent sensitive files from accidentally leaving your machine: **Git** and **Docker**. Each needs its own ignore file.

**`.gitignore`** tells Git which files and directories to never track. If a file is listed here, `git add .` will never touch it and it will never appear in a commit.

**`.dockerignore`** tells Docker which files to exclude from the build context — the set of files sent to the Docker daemon when you run `docker build`. Even if a file is gitignored, Docker will still copy it into a container image unless you explicitly tell it not to.

Create or update `.gitignore` in your project root:

```
# Environment secrets — NEVER commit these
.env

# Python artifacts
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/

# Virtual environments
.venv/
venv/
env/

# Database volume data
db/

# OS artifacts
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/
```

Create `.dockerignore` in your project root:

```
# Environment secrets
.env

# Git history — no reason to copy this into an image
.git
.gitignore

# Python cache — rebuilt inside the container
__pycache__/
*.pyc
*.pyo

# Virtual environments — the container uses its own
.venv/
venv/

# Database volume — managed by the db container, not the build
db/

# Local docs and editor configs
*.md
.vscode/
.idea/
```

The overlap is intentional. They are solving different problems: `.gitignore` keeps secrets out of version control history, `.dockerignore` keeps secrets out of container images. A file needs to be in both to be fully protected.

---

### .env.example

The `.env` file is gitignored — it will never appear in the repository. But a developer who clones the project for the first time has no way of knowing which variables they need to create. The solution is an `.env.example` file: a template that **is** committed to the repository, containing every variable key with placeholder values instead of real secrets.

Create `.env.example` in your project root:

```
# Django
SECRET_KEY=your-long-random-secret-key-here
DEBUG=False

# Allowed origins
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database
POSTGRES_DB=task_db
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password
DB_HOST=postgres-container
DB_PORT=5432
```

Every developer who clones the project runs:

```bash
cp .env.example .env
```

Then fills in the real values. The `.env.example` acts as living documentation for the application's configuration contract — every variable the app expects, with no secrets attached.

---

## Conclusion

Moving from development to production is not just about flipping a switch — it is about systematically closing every door that was left open to make development convenient.

- **`ALLOWED_HOSTS`** was locked down from `'*'` to a specific domain list, preventing Host Header attacks.
- **`CORS_ALLOWED_ORIGINS`** replaced the blanket `CORS_ALLOW_ALL_ORIGINS = True`, restricting API access to our own frontend.
- **Credentials and secret keys** were moved out of source files entirely and into environment variables loaded at runtime.
- **A catch-all URL pattern** ensures every unknown route returns a consistent JSON 404 rather than an HTML error page.
- **The `handle_exceptions` decorator** gave every view method consistent, DRY error handling without repeating the `try/except` pattern across the codebase.
- **Docker Compose** stopped advertising credentials in plain text and stopped exposing the database and backend ports to the outside world.
- **`.gitignore` and `.dockerignore`** create two independent barriers ensuring sensitive files never leave the local machine.
- **`.env.example`** documents every variable the application needs without exposing a single real secret.

None of these changes alter what the application *does*. They only change how much of it is visible to the outside world. In production, the answer should always be: as little as possible.
