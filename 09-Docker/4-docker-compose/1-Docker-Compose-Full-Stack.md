# Docker Compose Full Stack

In this lesson, we will build a complete web application environment using `Docker Compose`. This setup will include `Nginx` as a reverse proxy, `React` as the frontend, `Gunicorn` for serving the `Django` backend, and `PostgreSQL` as the database. Docker Compose will allow us to manage all these services together, ensuring a consistent and efficient development environment.

## Learning Objectives
* Understand how to define services in a docker-compose.yml file.
* Set up and connect a Django backend with a PostgreSQL database using Docker Compose.
* Configure Gunicorn to serve the Django application.
* Build and run the React frontend using Docker Compose.

## Project Setup

### Step 1: Setting Up the Project Structure

To get started, you need to initialize both the __`Django backend`__ and the __`React frontend`__, then set up your __`requirements.txt`__ file. Use the commands below to set everything up to match the [Project Structure](#project-structure) below.

#### Django initialization command
```bash
django-admin startproject myproject .
```

#### React initialization command
```bash
npm create vite@latest my-react-app -- --template react
```

#### Requirements.txt command
```bash
pip freeze > requirements.txt
```

#### Project structure
Using those commands, create a project directory with the following structure:

```plaintext
project/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── myproject/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── manage.py
├── frontend/my-react-app
│   ├── public
│   |── src/
│   |    └── main.jsx
│   ├── .gitignore
│   ├── Dockerfile
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── nginx/
│   └── nginx.conf
└── docker-compose.yml
```

### Step 2: Writing the Dockerfiles

#### Backend (Django with Gunicorn)

Create a __`Dockerfile`__ in the __`backend/`__ directory.

```Dockerfile
# backend/Dockerfile

FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose the Gunicorn port
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
```

##### Explanation

- __FROM python:3.10-slim__: Uses a lightweight Python 3.10 image as the base for the Docker container. The slim variant is smaller, reducing the overall image size.

- __ENV PYTHONDONTWRITEBYTECODE=1__: Sets an environment variable to prevent Python from writing .pyc files to disk, which can reduce the image size and prevent unnecessary file clutter.

- __ENV PYTHONUNBUFFERED=1__: Ensures that Python output is sent straight to the terminal without buffering. This helps in logging and debugging.

- __WORKDIR /app__: Sets the working directory inside the container to /app. All subsequent commands will run in this directory.

- __COPY requirements.txt .__: Copies the requirements.txt file from the host into the container's working directory.

- __RUN pip install --upgrade pip__: Upgrades pip to the latest version inside the container.

- __RUN pip install -r requirements.txt__: Installs the Python dependencies listed in requirements.txt.

- __COPY . .__: Copies the entire content of the current directory (excluding files in .dockerignore) into the container's working directory.

- __EXPOSE 8000__: Exposes port 8000 on the container, which is the port Gunicorn will use to serve the Django application.

- __CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]__: Specifies the command to run when the container starts. In this case, it runs Gunicorn to serve the Django application.

#### Frontend (React)

Create a __`Dockerfile`__ in the __`frontend/`__ directory.

```Dockerfile
FROM node:latest

WORKDIR /app

# Install dependencies
COPY package.json .
RUN npm install

# Copy all files and build the app
COPY . .

# Expose the port for the React app
EXPOSE 5173

# Start the React app
CMD ["npm", "run", "dev"]
```

##### Explanation

- __FROM node:latest__: Uses the latest Node.js image as the base for the Docker container. This includes the Node.js runtime and npm, which are needed to install dependencies and run the development server.

- __WORKDIR /app__: Sets the working directory inside the container to /app. This is where the application code will be placed and run.

- __COPY package.json .__: Copies the package.json file from the host into the container's working directory. This file lists the project’s dependencies.

- __RUN npm install__: Installs the project dependencies specified in package.json.

- __COPY . .__: Copies the entire content of the current directory (excluding files in .dockerignore) into the container's working directory.

- __EXPOSE 5173__: Exposes port __5173__ on the container, which is the port your React development server will use. This allows the app to be accessed from your host machine.

- __CMD ["npm", "run", "dev"]__: Specifies the command to run when the container starts. This starts the React application in development mode using Vite's development server on port 5173.

### Step 3: Setting up Nginx

Create an __`nginx.conf`__ file in the __`nginx/`__ directory.

```nginx
# nginx/nginx.conf

worker_processes auto;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Include configuration files from /etc/nginx/conf.d/
    include /etc/nginx/conf.d/*.conf;

    # Your server blocks
    server {
        listen 80;
        server_name yourdomain.com;

        location / {
            proxy_pass http://frontend:5173;
        }
    }
}
```

### Step 4: Configuring the React Frontend

Before we use Docker compose, we need to configure the React frontend to run on a specific port. By default, Vite runs on port 5173 in development mode. To correctly expose the development port, update your Vite configuration.

```javascript
// vite.config.js 
export default defineConfig({
  server:{
    host:"0.0.0.0",
    port:5173,
  },
  plugins: [react()],
})
```

### Step 5: Writing the Docker Compose File

Create a docker-compose.yml file in the root of the project.

```yaml
# docker-compose.yml

services:
  backend:
    build: ./backend
    command: gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - db

  frontend:
    build: ./frontend/my-react-app
    command: npm run dev
    volumes:
      - ./frontend/my-react-app:/app
    ports:
      - "5173:5173"
    depends_on:
      - backend

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    ports:
      - "5432:5432"

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend

volumes:
  postgres_data:
```

##### Explanation

- __services__: Defines the different containers that will run as part of this application.

    - __backend__: Configuration for the Django backend service.

        - __build__: `./backend`: Builds the Docker image for the backend service from the Dockerfile in the backend directory.
        - __command__: `gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application`: Overrides the default command to run Gunicorn with the Django application.
        - __volumes__: - `./backend:/app`: Mounts the backend directory from the host to the /app directory in the container, allowing for live updates and debugging.
        - __ports__: - `"8000:8000"`: Maps port 8000 on the host to port 8000 on the container.
        - __depends_on__: - `db`: Ensures that the backend service starts after the db service is up and running.
    - __frontend__: Configuration for the React frontend service.

        - __build__: `./frontend/my-react-app`: Builds the Docker image for the frontend service from the Dockerfile in the frontend directory.
        - __command__: `npm run dev`: Overrides the default command to start the React development server.
        - __volumes__: - `./frontend/my-react-app:/app`: Mounts the frontend directory from the host to the /app directory in the container.
        - __ports__: - `"5173:5173"`: Maps port 5173 on the host to port 5173 on the container.
        - __depends_on__: - `backend`: Ensures that the frontend service starts after the backend service is up and running.
    - __db__: Configuration for the PostgreSQL database service.

        - __image__: `postgres:13`: Uses the PostgreSQL 13 image as the base for the database container.
        - __volumes__: - `postgres_data:/var/lib/postgresql/data/`: Defines a named volume for persistent data storage.
        - __environment__: Sets environment variables for the PostgreSQL database.
        - __ports__: - `"5432:5432"`: Maps port 5432 on the host to port 5432 on the container.
    - __nginx__: Configuration for the Nginx service.

        - __image__: `nginx:latest`: Uses the latest Nginx image.
        - __ports__: - `"80:80"`: Maps port 80 on the host to port 80 on the container.
        - __volumes__: - `./nginx/nginx.conf:/etc/nginx/nginx.conf`: Mounts the Nginx configuration file from the host to the container.
        - __depends_on__: - `frontend`: Ensures that Nginx starts after the frontend service is up and running.
    - __volumes__: `Defines named volumes for persistent data storage`. In this case, it is used for the PostgreSQL data.

### Step 6: Configuring Django for PostgreSQL

Update the __`settings.py`__ in your Django project to connect with the PostgreSQL database.

```python
# backend/myproject/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'db',  # Docker Compose service name
        'PORT': '5432',
    }
}
```

## Managing the Application

### Running the Application
Now that everything is set up, you can start the application using Docker Compose.

```bash
docker-compose up --build
```

This command will build and start all the services defined in __`docker-compose.yml`__.

#### Accessing the Application

* `React` will be accessible at http://localhost:3000
* `Django` will be accessible at http://localhost:8000
* `Nginx` will be accessible at http://localhost:80

### Shutting down Application

To stop and remove the containers created by Docker Compose, use the following command.

```bash
docker-compose down
```

## Conclusion
In this lesson, you learned how to set up a full-stack web application using Docker Compose with Nginx, React, Gunicorn, Django, and PostgreSQL. Docker Compose simplifies managing multiple services, enabling efficient development and deployment of complex applications.