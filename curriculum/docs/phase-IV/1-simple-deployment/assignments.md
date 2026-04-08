# Simple Deployment — Assignments

## Part I

These assignments reinforce the core concepts and hands-on skills from the lessons. Complete all of them before moving on.

### Deploy Your Application

Follow the lessons in this module to deploy your Phase II full-stack project to AWS EC2:

1. Launch an EC2 instance (Ubuntu Server 24.04 LTS, t3.micro, key pair, security group with ports 22/80/443)
2. Update your Django project to support CORS and accept requests from `ALLOWED_HOSTS = ['*']`
3. Update your front-end Axios instance to point at your EC2's public IPv4 address
4. Push your changes to GitHub
5. SSH into your EC2 instance and install Docker
6. Clone your repository and start the application with `docker compose up -d`
7. Run Django migrations against the live database
8. Verify your application is reachable in a browser at `http://<your-ec2-ipv4>`

Document your EC2 instance's public IPv4 address and share your deployed URL with your instructor.

---

### Conceptual Questions

Answer the following questions in your own words:

1. What is an IPv4 address? What is DNS, and why does it exist?
2. What is the difference between stopping and terminating an EC2 instance?
3. Why does the `.pem` key file require `chmod 600` permissions before SSH will use it?
4. What does the `-d` flag do in `docker compose up -d`? Why is it important for a deployed server?
5. Why does Django's `ALLOWED_HOSTS` setting need to be updated before deploying to EC2?

---

## Part II

These assignments ask you to apply the deployment skills in new contexts.

### Explore Your Running Instance

SSH into your deployed EC2 instance and answer the following using only terminal commands:

1. What processes are currently running? (hint: `ps aux` or `top`)
2. How much disk space is being used? (`df -h`)
3. How much memory is available? (`free -h`)
4. What Docker containers are running and what are their names? (`sudo docker ps`)
5. View the last 50 lines of logs from your NGINX container

---

### Add an Environment Variable

Your application likely has at least one secret (Django `SECRET_KEY`, a database password, or an API key). Currently it may be hardcoded or committed to your repository.

1. Create a `.env` file on your EC2 instance in your project directory
2. Move the secret value into the `.env` file
3. Ensure `.env` is listed in `.gitignore` so it is never committed
4. Update your `docker-compose.yml` to read the value using `env_file:` or `environment:`
5. Restart the containers and verify the application still works

---

## Stretch

These are optional and open-ended.

### Auto-Start on Reboot

EC2 instances can be stopped and restarted — for example, during maintenance or after an unexpected shutdown. By default, your Docker containers will not restart automatically when the EC2 instance comes back up.

Research Docker's `restart` policy and configure your `docker-compose.yml` so that all containers restart automatically when the instance reboots. Test it by rebooting the EC2 instance from the AWS console and verifying the app comes back up on its own.

---

### Explore AWS CloudWatch

AWS CloudWatch provides monitoring and logging for EC2 instances. Explore the CloudWatch console and:

1. Find the CPU utilization graph for your running instance
2. Identify what metrics are available by default without any additional configuration
3. Research what "CloudWatch Logs" would require to capture your application's Docker logs — document the steps needed but do not implement them yet
