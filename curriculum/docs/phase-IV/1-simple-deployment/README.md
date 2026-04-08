# Simple Deployment

## What are we trying to accomplish?

You have been building full-stack applications locally. Every service — the database, the back end, the front end — runs on your machine, talking to itself through `localhost`. That works perfectly for development, but it means nobody outside your machine can use it.

In this module, we close that gap. We will take a Dockerized full-stack application and deploy it to a real server running in a data center — an AWS EC2 instance — so that it is accessible from any browser, anywhere in the world.

Along the way we will demystify how the internet actually routes requests, why cloud providers exist, what an EC2 instance is under the hood, and how to operate a remote Linux server over SSH.

---

## Terminal Learning Objectives

By the end of this module, you will be able to:

- Deploy a Dockerized full-stack application to an AWS EC2 instance and verify it is publicly accessible from a browser

---

## Enabling Learning Objectives

To reach the TLO, you will work through the following milestones:

- Explain how IPv4 addresses and DNS work together to route traffic on the internet
- Compare major cloud hosting providers and identify appropriate use cases for each
- Launch an EC2 instance with a configured AMI, instance type, key pair, and security group
- Connect to a remote server over SSH using a PEM key and resolve common permission errors
- Install Docker on a fresh Ubuntu Server instance
- Clone a GitHub repository and start a multi-container application in detached mode
- Run Django migrations against a live database running inside a Docker container
- Monitor running containers and application logs to verify a successful deployment

---

## Lessons

1. [Internet and AWS](./1-internet-and-aws.md)
2. [Deploying your App](./2-deploying-your-app.md)

---

## Assignments

[Module Assignments](./assignments.md)
