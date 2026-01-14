# Phase II – Full Stack Development

## Overview

Phase II transitions students from foundational programming concepts into the world of **full stack application development**. In this phase, students learn how modern web applications are designed, built, tested, deployed, and maintained across the front-end, back-end, and database layers. The emphasis shifts from isolated code exercises to **connected systems**, where multiple technologies work together to deliver real user-facing functionality.

By the end of Phase II, students will understand how data flows through an application—from user interaction in the browser, through API requests, into a database, and back again as structured responses. They will gain hands-on experience building React front-end applications, designing RESTful APIs with Django, managing relational databases with PostgreSQL, and orchestrating full-stack systems using Docker and Docker Compose. This phase establishes the technical depth required for production-ready applications and prepares students for cloud infrastructure and advanced system design in later phases.

---

## Modules

### [Module 4 – Front-End Development (React & Docker)](./04-Front-End/README.md)

Module 4 introduces students to the front-end layer of modern web applications, beginning with a conceptual overview of full stack development. Students explore how the internet works, the role of the browser, and how front-end, back-end, and databases interact within a complete system. This foundational understanding helps students contextualize every tool they use moving forward.

The module then focuses on HTML, CSS, and JavaScript, with an emphasis on DOM manipulation and event-driven programming. Students build interactive interfaces served locally through development servers, learning how JavaScript dynamically updates the user interface in response to user actions. Fetch and AJAX are introduced to enable communication with third-party APIs, allowing students to retrieve and display external data within their applications.

React is introduced as a component-based framework for building scalable user interfaces. Students create React projects using Vite and learn core hooks such as `useState` and `useEffect` to manage state and side effects. The Single Responsibility Principle is reinforced through component design, with props used to manage data flow between parent and child components. Styling strategies are expanded through utility-first and component-based libraries such as Tailwind CSS and React Bootstrap, enabling rapid UI development.

Routing is introduced through React Router DOM, where students build Single Page Applications that respond to browser URL changes. Advanced routing concepts are explored using React Router hooks such as `useLoaderData`, `useLocation`, `useNavigation`, and `useOutletContext`. The module concludes with front-end testing using Cypress for end-to-end testing and continuous deployment using GitHub Actions to deploy React applications to GitHub Pages.

---

### [Module 5 – Back-End Development (Django & Docker)](./05-Back-End/README.md)

Module 5 shifts focus to the server-side of full stack applications. Students begin by learning how relational database management systems work, with PostgreSQL serving as the primary database. They explore schema design, table relationships, SQL queries, and joins, using tools like drawSQL to visualize database structures. Concepts such as normalization are introduced to promote clean and maintainable data design.

Students then move into Django, learning the framework’s project structure and how the Django ORM bridges Python code and relational databases. Emphasis is placed on secure application development through environment variables, `.env` files, and `.gitignore` usage to protect sensitive credentials. Unit testing is introduced within Django to reinforce test-driven development and prepare students for CI pipelines.

Data validation and serialization are covered using Django’s built-in validators and Django REST Framework ModelSerializers. Students learn how to normalize and validate incoming data while enabling create, read, update, and delete operations on model instances. Relationships between models—including one-to-one, many-to-one, and many-to-many—are explored, alongside serializer adjustments to represent related data accurately.

The module continues with API development using Django REST Framework APIViews and class-based views. Students implement full CRUD functionality mapped to HTTP methods and appropriate response status codes, reinforcing RESTful API design principles. Authentication is introduced through token-based authentication and JWT using `djangorestframework_simpleJWT`, enabling secure user access. The module concludes with advanced topics such as API caching, logging, and asynchronous request handling using tools like Redis.

---

### [Module 6 – Full Stack Integration (Docker Compose)](./06-Full-Stack/README.md)

Module 6 brings all layers of the application together into a cohesive full stack system. Students are introduced to Docker Compose as a tool for orchestrating multiple services, including React, Django, PostgreSQL, NGINX, and Gunicorn. They learn how container networking works and how services communicate with one another within a composed environment.

This module emphasizes real-world workflows, demonstrating how front-end applications communicate with back-end APIs using tools like Axios, and how those requests are handled by Django views and persisted in the database. Students gain a holistic understanding of how full stack applications are built, deployed, and scaled, reinforcing the end-to-end development process from browser to database and back again.

---

## Technologies

Throughout Phase II, students work with the following tools and technologies:

<p align="left">

<a href="https://developer.mozilla.org/en-US/docs/Web/HTML" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg" alt="html" width="40" height="40"/>
</a>

<a href="https://developer.mozilla.org/en-US/docs/Web/CSS" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original.svg" alt="css" width="40" height="40"/>
</a>

<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/>
</a>

<a href="https://react.dev/" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/react/react-original.svg" alt="react" width="40" height="40"/>
</a>

<a href="https://www.docker.com/" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/>
</a>

<a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-plain.svg" alt="django" width="40" height="40"/>
</a>

<a href="https://www.postgresql.org/" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg" alt="postgresql" width="40" height="40"/>
</a>

<a href="https://www.nginx.com/" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nginx/nginx-original.svg" alt="nginx" width="40" height="40"/>
</a>

<a href="https://www.cypress.io/" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/cypressio/cypressio-original.svg" alt="cypress" width="40" height="40"/>
</a>

<a href="https://vite.dev/" target="_blank" rel="noreferrer">
<img src="https://vite.dev/logo.svg" alt="vite" width="40" height="40"/>
</a>

<a href="https://gunicorn.org/" target="_blank" rel="noreferrer">
<img src="https://habrastorage.org/r/w120/web/334/300/762/3343007626ed4bb2a3cde09be8ae9da2.png" alt="gunicorn" width="40" height="40"/>
</a>

<a href="https://docs.docker.com/compose/" target="_blank" rel="noreferrer">
<img src="https://i0.wp.com/codeblog.dotsandbrackets.com/wp-content/uploads/2016/10/compose-logo.jpg?resize=622%2C678&ssl=1" alt="docker-compose" width="40" height="40"/>
</a>

<a href="https://www.django-rest-framework.org/" target="_blank" rel="noreferrer">
<img src="https://cdn.brandfetch.io/django-rest-framework.org/fallback/lettermark/theme/dark/h/256/w/256/icon?c=1bfwsmEH20zzEfSNTed" alt="drf" width="40" height="40"/>
</a>

<a href="https://www.psycopg.org/psycopg3/docs/" target="_blank" rel="noreferrer">
<img src="https://www.psycopg.org/psycopg3/docs/_static/psycopg.svg" alt="psycopg3" width="40" height="40"/>
</a>

<a href="https://requests.readthedocs.io/en/latest/" target="_blank" rel="noreferrer">
<img src="https://requests.readthedocs.io/en/latest/_static/requests-sidebar.png" alt="requests" width="40" height="40"/>
</a>

</p>
