# Project Layout

Prior to starting this lesson please create a project with the following folder structure:

```bash
root/
├── client/                     # React + Vite frontend
│   ├── index.html
│   ├── package.json
│   ├── Dockerfile
│   ├── vite.config.js
│   ├── public/
│   │   └── favicon.svg
│   └── src/
│       ├── assets/
│       ├── components/
│       ├── pages/
│       ├── services/           # API calls 
│       ├── App.jsx
│       ├── router.jsx
│       └── main.jsx
│
├── db/  
│   └── Dockerfile
│
├── server/                     # Django backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env
│   ├── Dockerfile
│   │
│   ├── task_api/                 # Django project settings
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── user_app/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── tests.py
│   │
│   └── task_app/
│       ├── migrations/
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── urls.py
│       ├── serializers.py
│       ├── views.py
│       └── tests.py
│   
│
├── README.md
└── .gitignore
```

Now that your project structure has been created, please fill in the projects with the following template code. We will be utilizing this codebase through out this project making it essential for you to conduct this step correctly:

* [Server](./1-back-end.md)
* [Client](./2-front-end.md)


**ENSURE ALL FILES ARE COPIED CORRECTLY AND PROJECTS FUNCTIONALITY PRIOR TO STARTING THIS LECTURE**