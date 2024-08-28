# Container Deployment with Docker Hub and AWS EC2

In this lesson, we will cover the basics of using `Docker Hub` to store and manage Docker images and then demonstrate how to deploy these images on an `AWS EC2 instance`. By the end of this lesson, you'll have a solid understanding of Docker Hub, how to push images to it, and how to deploy these images onto a cloud server.

## Learning Objectives

* Understand what Docker Hub is and its role in managing Docker images.
* Learn how to push Docker images to Docker Hub.
* Deploy Docker images from Docker Hub to an AWS EC2 instance.

## Introduction to Docker Hub

### What is Docker Hub?

Docker Hub is a cloud-based repository where Docker users can store, share, and manage Docker images. It acts as a centralized location where Docker images can be easily accessed and used by anyone or by specific collaborators.

### Key Features

* __Public and Private Repositories:__ Docker Hub offers both public and private repositories. Public repositories can be accessed by anyone, while private repositories are restricted to specific users or teams.
* __Automated Builds:__ Docker Hub can automatically build Docker images from GitHub or Bitbucket repositories, making continuous integration seamless.
* __Webhooks:__ Docker Hub supports webhooks to trigger actions after an image is pushed or updated.

## Step-by-Step Guide to Using Docker Hub

### Step 1: Setting Up Docker Hub

1. __Create an Account:__ Start by creating an account on [Docker Hub](https://hub.docker.com/). If you already have an account, log in.

2. __Create a Repository:__ Once logged in, create a new repository by clicking the `Create Repository` button from the `hub.docker.com` not the `app.docker.com`. Name your repository and choose whether it should be public or private. 
* `Note`: For this lesson, we will create the repositories from the command line so __`this is not necessary`__.

### Step 2: Pushing Docker Images to Docker Hub

Once you have your `Dockerfiles` made, you will need to `build them into images`. When you are done, you should do the following steps to push them to Dockerhub. 

1. __Log in to Docker from the CLI:__

```bash
docker login
```

If you have `permission denied`, you must add user to the `docker group`, which is explained in the setting up the [Pulling Docker Images on the EC2 section](#pulling-and-running-docker-images-from-docker-hub).

2. __Tag your Docker Image:__ Before pushing your Docker image to Docker Hub, tag it with your Docker Hub username and the repository name.

```bash
docker tag <image-name> <dockerhub-username>/<repository-name>:<tag>
```

__Example:__

```bash
docker tag my-app ava/dockerhub-demo:latest
```

3. __Push the Image to Docker Hub:__ Push your tagged image to your Docker Hub repository.

```bash
docker push <dockerhub-username>/<repository-name>:<tag>
```

__Example:__

```bash
docker push ava/dockerhub-demo:latest
```

After a successful push, your Docker image will be available in the Docker Hub repository you created.

### Step 3: Deploying Docker Images on AWS EC2

#### Setting Up an AWS EC2 Instance

1. __Launch an EC2 Instance:__
    * Go to AWS Management Console.
    * Navigate to the EC2 dashboard and click `Launch Instance`.
    * Give a name for the EC2 Instance you are creating
    * Choose an Amazon Machine Image (AMI), such as `Ubuntu Server`.
    * Select an instance type (e.g., `t2.micro` for free tier)
    * Make a key pair name by clicking the `Create new key pair` link in the __Key pair (login)__ section.
        * This will download a `.pem file` locally which is used for secure EC2 access.
        * You should store this in your `.ssh` folder using the `mv command`.
    * Configure security groups to allow HTTP, HTTPS, and SSH access.
    * Only allow My IP to access the EC2 instance instead of __Anywhere__ at __0.0.0.0__.
    * Review and launch the instance. It will take a while for AWS to provision the EC2 instance.

2. __Connect to your EC2 Instance:__
    * Change the permission of the `.pem file` to be `600` so that the ssh command will work as expected.
    ```bash
    chmod 600 ~/.ssh/your-key.pem
    ```

    * Once the instance is running and the `.pem file` permissions are updated, connect to it using SSH.
        * You may get the ec2 public ip by accessing your instance and noting the public ip.
        * You must use your generated `.pem file` that was stored in the `.ssh` folder previously.
    ```bash
    ssh -i ~/.ssh/your-key.pem ubuntu@<ec2-public-ip>
    ```
    * It will ask for confirmation and if your file permissions for the `.pem file` is correct, then it will allow you to proceed.
    * __ssh__ allows you to access the EC2 instance remotely through a secure shell.
    * `If you can not connect` due to a time out, check and see if the VPC is allowing connections if all else appears correct. [EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-prerequisites.html)

#### Install Docker on EC2
Do the following bash commands from inside the EC2 Instance.

1. __Update the Package Manager:__
```bash
sudo apt-get update
```

2. __Install Docker:__
```bash
sudo apt-get install docker.io -y
```

3. __Start and Enable Docker:__
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

#### Install Docker Compose on EC2
Do the following bash commands from inside the EC2 Instance.

1. __Curl latest docker compose release:__
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

2. __Apply Executable Permissions:__
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

3. __Verify:__
```bash
docker-compose --version
```

#### Pulling and Running Docker Images from Docker Hub
Do the following bash commands from inside the EC2 Instance.

1. __Add ubuntu user to the docker group:__
```bash
sudo usermod -aG docker $USER
``` 
This adds the current user `$USER` to the `docker` group, so that you will have access to log in later.

2. __New group:__

To apply the group membership changes, you need to log out and log back in or do the following.

```bash
newgrp docker
```

This command applies the group changes to your current session.

3. __Verify Docker Group Membership:__

```bash
groups
```

You should see docker listed.

4. __Log In to Docker Hub:__
```bash
docker login
```

5. __Pull the Docker Image:__
```bash
docker pull <dockerhub-username>/<repository-name>:<tag>
```

__Example:__
```bash
docker pull ava/dockerhub-demo:latest
```

6. __Run the Docker Container:__
```bash
docker run -d -p 80:80 <dockerhub-username>/<repository-name>:<tag>
```

This command will run the container in detached mode and map port 80 of the EC2 instance to port 80 of the container.

## Conclusion

You've successfully pushed a Docker image to Docker Hub and deployed it on an AWS EC2 instance. Docker Hub simplifies the management and distribution of Docker images, while AWS EC2 provides a scalable environment to deploy your applications.