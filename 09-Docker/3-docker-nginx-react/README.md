# Vite + React.js in Docker

## What are we Trying to Accomplish?

In this lesson, we aim to containerize a Vite + React.js application using Docker and Nginx. By doing so, we ensure a consistent and portable environment for both development and production. We'll set up Docker to build and serve our React app with Nginx, which will handle static content and proxy API requests, ultimately deploying the application on port 80.

## Lectures and Assignments

* [Lesson - Vite, React, Nginx in Docker](./3-vite-react-in-Docker.md)

## TLO's(Terminal Learning Objectives)

- **Docker's role**: Understand what Docker is and its role in application deployment.
- **Create a Dockerfile**: Define the container's configuration.
- **Host with Nginx on port 80**: Configure Nginx to serve static content from the React 'dist' directory to port 80 using a container.
- **Build a Docker image**: Generate an image from the Dockerfile.
- **Run a Docker container**: Host the Vite + React.js + Nginx project on port 80.

## ELO's(Enabling Learning Objectives)

- **Basic Docker Commands**: Use basic Docker commands to manage containers effectively.
- **Docker Configuration**: Configure the Vite + React.js + Nginx project to run in the Docker container.