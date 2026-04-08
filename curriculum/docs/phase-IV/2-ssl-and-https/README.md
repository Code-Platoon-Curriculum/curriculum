# SSL and HTTPS

## What are we trying to accomplish?

Your application is deployed and accessible over the internet — but if you look at the browser address bar you will see a "Not Secure" warning. Every piece of data traveling between your users and your server (login credentials, tokens, application data) is sent as unencrypted plaintext.

In this module, we fix that. We will understand why HTTP is insufficient for production, acquire a domain name, and secure the application with HTTPS using two approaches: **Certbot** (free, installed directly on the server) and **AWS Certificate Manager + Application Load Balancer** (the AWS production pattern).

---

## Terminal Learning Objectives

By the end of this module, you will be able to:

- Secure a deployed web application with HTTPS using both a server-installed certificate and an AWS-managed certificate with a load balancer

---

## Enabling Learning Objectives

To reach the TLO, you will work through the following milestones:

- Explain why HTTP exposes users to man-in-the-middle attacks and why modern browsers restrict features to HTTPS
- Describe how Certificate Authorities, the certificate chain, and the TLS handshake establish trust
- Compare SSL providers (Let's Encrypt, AWS ACM, commercial CAs) and explain when to use each
- Register a domain name and configure DNS A records to point the domain to a server
- Obtain a free TLS certificate using Certbot in standalone mode and configure NGINX and Docker Compose to serve HTTPS
- Request and DNS-validate an ACM certificate through the AWS console
- Create a Target Group and Application Load Balancer with HTTP-to-HTTPS redirect and an HTTPS listener using an ACM certificate
- Update Route 53 DNS records to route traffic through an Application Load Balancer

---

## Lessons

1. [Why SSL](./1-why-ssl.md)
2. [Acquiring SSL](./2-acquiring-ssl.md)

---

## Assignments

[Module Assignments](./assignments.md)
