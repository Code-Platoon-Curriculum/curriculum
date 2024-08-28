# Deploy Full Stack Container in AWS EC2

In this lesson, we'll deploy a full-stack `Django + React + Nginx application`, from [Lesson 4](../4-docker-compose/1-Docker-Compose-Full-Stack.md), on an `EC2 instance` using `Docker`. By the end of this lesson, you'll have a live application accessible via the internet.

## Prerequisites

* `AWS EC2 instance` is set up.
* `Docker` and `Docker Compose` installed on EC2 instance.
* You have SSHed into the EC2 instance.
* A `Docker Hub` repository is ready for pushing images.
* [Lesson 4](../4-docker-compose/1-Docker-Compose-Full-Stack.md) is completed with the front and back end Docker files set up.

## Learning Objectives

* Learn how to deploy a full-stack `Django + React application`.
* Configure `Nginx` on `AWS EC2 instance`.
* Make use of `Docker Hub` on `AWS EC2 instance`.

## Step 1: Push your Docker Images to Docker Hub

Using the `React + Django + Nginx project` from [Lesson 4](../4-docker-compose/1-Docker-Compose-Full-Stack.md), we need to push this to the Docker Hub repository.

### 1. Log in to Docker Hub

```bash
docker login
``` 

### 2. Tag Your __(username)/backend__ Image

Navigate to the `lesson 4 backend directory` then do the following.

```bash
docker build -t <username>/backend:latest .
```

### 3. Tag your __(username)/frontend__ Image

Navigate to the `lesson 4 frontend directory` then do the following.

```bash
docker build -t <username>/frontend:latest .
```

### 3. Push Your Images

```bash
docker push <username>/your_repo_name:tag
```

#### Example

```bash
docker push <username>/backend:latest
```

Repeat this for each image you need to push ((username)/backend and (username)/frontend).

## Step 2. Set up your EC2 Instance

Before proceeding, ensure your EC2 instance is up and running, and you're connected via SSH. You should also have `Docker` and `Docker Compose` installed on your instance.

### 1. Log in to Docker Hub from EC2

```bash
docker login
```

### 2. Pull the Docker Images

```bash
docker pull your_dockerhub_username/your_repo_name:tag
```

Pull each of your images ((username)/backend and (username)/frontend) to the EC2 instance.

### 3. Prepare `docker-compose.yml`

Make sure your [docker-compose.yml](./resources/docker-compose.yml) file is ready on the EC2 instance. You need to securely copy it from your local machine, you can use scp `(secure copy protocol)` to transfer the file. `Note:` Do this in your host machine, not from inside the SSH.
* `Note:` To avoid errors, you should use the new [docker-compose.yml](./resources/docker-compose.yml) provided in resources as it works even in the EC2 environment.

```bash
scp -i /path/to/your-key.pem /path/to/docker-compose.yml ubuntu@your_ec2_ip:/home/ubuntu/
```

### 4. Copy the Frontend, Backend, and Nginx files

To ensure the docker compose will work fine, we will need the files securely copied to the EC2. 
* `Note:` Usually the easiest way to do this is to do a git clone from github, but since our files are not source controlled, it will be done __manually__. 

#### Minimum files needed

```plain-text
project/
├── backend/
│   ├── Dockerfile             # Dockerfile for the backend service
|   ├── requirements.txt       # requirements.txt
│   └── myproject/
│       └── wsgi.py            # WSGI entry point for the Django project
├── frontend/
│   └── my-react-app/
│       ├── Dockerfile         # Dockerfile for the frontend service
│       ├── package.json       # Node.js package file with "dev" script
|       └── ...rest            # Everything except node modules
├── nginx/
│   └── nginx.conf             # Nginx configuration file
└── docker-compose.yml         # Docker Compose file
```

#### Front End Secure Copy
 
```bash
scp -i /path/to/your-key.pem /path/to/frontend/my-react-app/Dockerfile ubuntu@your_ec2_ip:/home/ubuntu/frontend/my-react-app/
```

```bash
scp -i /path/to/your-key.pem /path/to/frontend/my-react-app/package.json ubuntu@your_ec2_ip:/home/ubuntu/frontend/my-react-app/
```

... continue for all files except for node_modules folder

_If we used source control it wouldn't be this manual._

#### Backend End Secure Copy

```bash
scp -i /path/to/your-key.pem -r /path/to/backend/ ubuntu@your_ec2_ip:/home/ubuntu/
```

#### Nginx End Secure Copy

```bash
scp -i /path/to/your-key.pem -r /path/to/nginx ubuntu@your_ec2_ip:/home/ubuntu
```

`Note:` You may have to use the updated nginx config [here](./resources/nginx.conf).

### 5. Run the Docker Compose Application

Navigate to the directory where your `docker-compose.yml` file is located and `run the application` from inside your `EC2 Instance`.

```bash
docker-compose up -d
```

This command will start all the services defined in your docker-compose.yml file in detached mode.

#### Troubleshooting Docker Compose not working

So you may encounter an error where some dependencies don't install for whatever reason. 
You can manually install them by opening the container and doing so, or use the updated [docker-compose.yml](./resources/docker-compose.yml) to get around this error.

##### Manually installing to frontend service
```bash
docker-compose run frontend /bin/sh
npm install
```

##### View images, processes, and prune

* View images
```bash
docker images
```

* View processes
```bash
docker ps -a
```

* Prune
```bash
docker image prune
docker system prune
```

## Step 3. Verify the Deployment

### 1. Check Running Containers

In the EC2 Instance:

```bash
docker ps
```

Ensure that all your services ((username)/backend and (username)/frontend) are running.

### 2. Access your Application

* Open a browser and navigate to `http://your-ec2-public-ip`. You should see your application running.

## Managing your Application

### Stop the services

```bash
docker-compose down
```

### View the logs

```bash
docker-compose logs -f
```

## Conclusion

In this lesson, you successfully deployed your `Django + React + Nginx application` on an `EC2 instance` using `Docker` and `Docker Compose`. You learned how to push `Docker images` to `Docker Hub`, pull them on your EC2 instance, and run the application seamlessly.