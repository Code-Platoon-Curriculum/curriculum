## Introduction to Docker with Vite + React and Nginx

When Docker is integrated with Vite + React, developers experience an unparalleled development and deployment workflow. Docker provides a unified environment, ensuring that the Vite + React application performs consistently, whether in development, testing, or production stages. The containerized setup eliminates discrepancies between development and production environments, addressing the infamous "it works on my machine" dilemma and fostering seamless collaboration among team members.

Moreover, Docker's containerization allows for efficient resource utilization and effortless scaling of Vite + React applications. Developers can confidently deploy their web applications, knowing they will operate consistently across various platforms, from local development machines to cloud-based servers.

## Learning Objectives

- Understand what Docker is and its role in application deployment.
- Create a Dockerfile with Nginx and React.
- Configure Nginx to serve static content from the React 'dist' directory.
- Build a Docker image from the Dockerfile.
- Run a Docker container to host the Vite + React.js + Nginx project on port 80.
- Use basic Docker commands to manage containers effectively.
- Configure the Vite + React.js + Nginx project to run in the Docker container.

## Concepts and Steps

### Step 1: Configure Vite + React.js + Nginx Project

Before integrating Docker and Nginx, we'll set up a Vite + React.js + Nginx project.

#### Install Vite + React.js 

Install the Vite + React.js template with the following commands.

```bash
npm create vite@latest my-react-app -- --template react
y
cd my-react-app
npm install
```

#### Configure Vite

Before we build the Docker image, we need to configure the Vite + React.js + Nginx project to run on a specific port. By default, Vite runs on port 5173 in development mode. To correctly expose the development port, update your Vite configuration.

Open the `vite.config.js` (or `vite.config.ts`) file in the root of your Vite + React.js + Nginx project. Locate the `server` section and update the `port` setting to the desired port (e.g., 5173):

```javascript
// vite.config.js (or vite.config.ts)
export default defineConfig({
  server:{
    host:"0.0.0.0",
    port:5173,
  },
  plugins: [react()],
})
```

### Step 2: Create the Nginx Configuration File

Create an Nginx configuration file [__nginx.conf__](./nginx.conf) in the root directory of your project. This file will configure Nginx to serve the static files and proxy API requests.

```nginx
server {
    listen 80;

    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 3: Create the Dockerfile

Now, create a [__Dockerfile__](./Dockerfile) in the root directory of your project. This file will build your React app, copy the files to the Nginx directory, and set up Nginx:

```Dockerfile
# Stage 1: Build React app
FROM node:latest as build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the entire project to the container
COPY . .

# Build the React app
RUN npm run build

# Stage 2: Setup Nginx to serve the React app
FROM nginx:alpine

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Remove default Nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy React build output to Nginx static files directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
```

#### Explanation:

- `FROM node:latest as build`: This line sets the base image for the first stage of our Docker build process. We're using the official Node.js image to build the React app.

- `WORKDIR /app`: Sets the working directory inside the container to /app. This is where the application code will reside.

- `COPY package*.json ./`: Copies the package.json and package-lock.json files from the host machine to the container's working directory. This is necessary to install project dependencies.

- `RUN npm install`: Installs the project dependencies inside the container based on the package.json files.

- `COPY . .`: Copies the entire project from the host machine to the container's working directory. This includes the source code and configuration files.

- `RUN npm run build`: Builds the production version of the Vite + React.js + Nginx project. The build artifacts are output to the dist directory.

- `FROM nginx:alpine`: This line starts the second stage of the Docker build process using the Nginx base image. This stage is responsible for serving the built React application.

- `COPY nginx.conf /etc/nginx/conf.d/default.conf`: Copies the Nginx configuration file from the host machine to the container. This file configures Nginx to serve the static files and proxy API requests.

- `RUN rm -rf /usr/share/nginx/html/*`: Removes the default static files provided by the Nginx image. This ensures that only the files we want to serve are included.

- `COPY --from=build /app/dist /usr/share/nginx/html`: Copies the React build output from the first stage (/app/dist) to the Nginx static files directory (/usr/share/nginx/html). This allows Nginx to serve the static assets of the React application.

- `EXPOSE 80`: Exposes port 80 on the container. This port is used by Nginx to serve the application and handle incoming requests.

- `CMD ["nginx", "-g", "daemon off;"]`: Specifies the command to run when the container starts. In this case, it starts Nginx in the foreground, keeping the container running and serving the application.

### Step 4: Build the Docker Image

With the Dockerfile in place, we can now build the Docker image for our Vite + React.js + Nginx project.

Open the terminal and navigate to the directory containing the Dockerfile and your Vite + React.js + Nginx project files. Then, run the following command:

```bash
docker build -t my-vite-react-nginx-app .
```

#### Explanation:

- `docker build`: This is the command to build a Docker image.
- `-t my-vite-react-nginx-app`: The `-t` flag is used to tag the image with a name (in this case, `my-vite-react-nginx-app`).
- `.`: The period `.` indicates that the Dockerfile is in the current directory.

This command will build the Docker image `my-vite-react-nginx-app` using the Dockerfile located in the current directory.

### Step 5: Run the Docker Container

Now that we have the Docker image built, we can create

 and run a Docker container based on that image.

Run the following command:

```bash
docker run -d -p 80:80 my-vite-react-nginx-app
```

#### Explanation:

- `docker run`: This command creates and runs a Docker container based on the specified image.
- `-d`: The `-d` flag runs the container in detached mode, which means it runs in the background.
- `-p 80:80`: The `-p` flag maps port 80 from the container to port 80 on your local machine, allowing you to access the application at `http://localhost`.
- `my-vite-react-nginx-app`: The name of the Docker image to use when creating the container.

### Step 6: Access Your Vite + React.js + Nginx Application

Congratulations! Your Vite + React.js + Nginx application is now running in a Docker container and is accessible at `http://localhost` on port 80 of your local machine. You should see your application running successfully in the web browser.

### Step 7: Exiting the Docker Container

If you want to stop the Docker container, you can use the `docker stop` command. First, find the container ID or name:

```bash
docker ps
```

Locate the container ID or name in the output. Then, stop the container:

```bash
docker stop <container_id_or_name>
```

### Step 8: Starting a Container with --rm

By default, Docker retains stopped containers. If you want to automatically remove the container when it stops, you can use the `--rm` flag when running the container:

```bash
docker run -d -p 80:80 --rm my-vite-react-nginx-app
```

#### Explanation:

- `--rm`: The `--rm` flag automatically removes the container when it stops running. This can help keep your system clean and organized.

## Conclusion

In this lesson, you've learned how to deploy a simple Vite + React.js + Nginx project in a Docker container and bind it to port 80 on your local machine. You've seen the essential Docker commands and what each command does. Additionally, you've configured the Vite + React.js + Nginx project to run inside the Docker container.

Docker provides a convenient way to package and deploy applications, ensuring consistency and portability across different environments. Now you can use Docker to deploy and manage more complex applications with ease. Happy coding!
