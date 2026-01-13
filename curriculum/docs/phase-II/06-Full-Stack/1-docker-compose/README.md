# Docker Compose & Full-Stack Orchestration

## What are we trying to accomplish

In this module, we focus on **orchestrating full-stack applications as cohesive systems** rather than isolated containers. While Dockerfiles allow us to package individual services, real-world applications require multiple services—databases, backend APIs, and frontends—to run together, communicate reliably, and mirror production behavior.

Through Docker Compose, you will learn how backend and frontend services are **declared, networked, and coordinated** using a single source of truth. You’ll move from manually running containers to defining reproducible infrastructure that reflects real deployment patterns, including service discovery, reverse proxies, environment configuration, and production-minded servers.

By the end of this module, you will understand how to **model a complete full-stack system**, how containers communicate over Docker networks, and how tools like Gunicorn and Nginx fit into modern deployment architectures. These skills are foundational for transitioning from local development to cloud-based environments such as ECS, Kubernetes, or managed PaaS platforms.

---

## Lectures & Assignments

### Lectures

- [Lecture – Intro to Docker Compose (Backend & Database)](./1-back-end.md)
- [Lecture – Docker Compose Full Stack (Frontend & Nginx)](./2-full-stack.md)

### [Assignments](./assignments.md)

---

## Terminal Learning Objectives (TLO's) executable

* Explain why Docker Compose is necessary for multi-container applications
* Describe the role of services, networks, and volumes in Docker Compose
* Orchestrate a backend API and database using Docker Compose
* Configure Django to connect to PostgreSQL over a Docker network
* Replace Django’s development server with Gunicorn in a containerized environment
* Serve a React frontend as static assets using Nginx
* Proxy API requests from Nginx to a backend service
* Treat a full-stack application as a single deployable system
* Reason about host vs container ports and service-to-service communication
* Execute operational tasks (migrations) inside running containers

---

## Enabling Learning Objectives (ELO's) enabling

* Define Docker Compose terminology: service, network, volume, depends_on
* Explain how Docker Compose performs service discovery using service names
* Differentiate between development servers and production servers
* Identify why databases are treated as managed services in containerized systems
* Understand the role of Gunicorn as a WSGI application server
* Explain Nginx’s responsibilities as a static file server and reverse proxy
* Interpret Nginx configuration files in the context of SPAs and APIs
* Apply environment variables using `.env` files in Docker Compose
* Reason about container isolation and explicit state management
* Connect Docker Compose concepts to real-world deployment and scaling strategies
