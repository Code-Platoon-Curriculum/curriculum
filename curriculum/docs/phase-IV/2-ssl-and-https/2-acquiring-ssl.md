# Acquiring SSL

## Intro

In the previous lesson we established why HTTP is insufficient for a production application, how SSL/TLS works, and acquired a domain name pointing to our EC2 instance. Now we will use that domain to obtain a certificate — two approaches, in order:

1. **Set up Certbot** — a free, open-source tool that installs a certificate directly on your server
2. **Set up ACM + ALB** — the AWS-native approach where a load balancer handles SSL termination on your behalf

By the end, your application will be served exclusively over HTTPS.

---

## Lesson

### Part 1 — Certbot / Let's Encrypt

#### What is Certbot?

**Certbot** is a free, open-source tool maintained by the Electronic Frontier Foundation (EFF) that automates the process of obtaining and renewing certificates from **Let's Encrypt** — a free, automated, open Certificate Authority.

Certbot handles:
- Communicating with Let's Encrypt to request a certificate
- Proving you control the domain (via an HTTP challenge on port 80)
- Writing the certificate files to `/etc/letsencrypt/live/yourdomain.com/`
- Setting up automatic renewal (certs expire after 90 days; Certbot renews them automatically)

#### Updating Your Project

Before installing the certificate, we need to update two things in the project:

1. **The NGINX configuration** — to support HTTPS and redirect HTTP traffic
2. **The docker-compose.yml** — to expose port 443 and give the NGINX container access to the cert files

**Update `default.conf`** — replace the existing configuration with the following:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri /index.html;
    }
}
```

> Replace `yourdomain.com` with your actual domain name in both `server` blocks.

The first server block listens on port 80 and immediately redirects all traffic to HTTPS (301 permanent redirect). The second block handles HTTPS on port 443 and references the certificate files that Certbot will create on the EC2 host.

**Update `docker-compose.yml`** — add port 443 and a volume mount for the certificate files to your `frontend` service:

```yaml
frontend:
  build: ./client
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - /etc/letsencrypt:/etc/letsencrypt:ro
  depends_on:
    - backend
```

> **Keep your existing volume mounts.** The snippet above only shows the fields that change. If your `frontend` service already has volume mounts (e.g., for your built files or `default.conf`), keep them — just add the `/etc/letsencrypt` line alongside them.

The `:ro` flag mounts the directory as read-only — the container reads the cert files but cannot modify them.

**Update Django `settings.py`** — replace the wildcard `ALLOWED_HOSTS` with your actual domain:

```python
ALLOWED_HOSTS = ['yourdomain.com']
```

**Update Django CORS** — replace `CORS_ALLOW_ALL_ORIGINS` with a specific allowed origin:

```python
CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
]
# Remove CORS_ALLOW_ALL_ORIGINS = True
```

**Update the Axios `baseURL`** — in `utilities.jsx`, change the `baseURL` to use your domain over HTTPS:

```js
export const api = axios.create({
    baseURL: 'https://yourdomain.com/api/v1/'
})
```

**Push all changes to GitHub:**

```bash
git add .
git commit -m "configure app for HTTPS and domain"
git push origin main
```

---

#### Installing the Certificate

SSH into your EC2 instance:

```bash
ssh -i my-ec2-key.pem ubuntu@<ipv4_address>
```

Pull the latest code:

```bash
cd <your-project-folder>
git pull origin main
```

Stop all running containers so port 80 is free for Certbot:

```bash
sudo docker compose down
```

> Certbot will temporarily start its own HTTP server on port 80 to complete the Let's Encrypt HTTP challenge. If a container is already bound to port 80, Certbot will fail.

Install Certbot using **snap** (the officially recommended method from the EFF/Certbot team):

```bash
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

> **Why snap?** The Certbot team maintains the snap package directly and it always ships the latest version. The `apt` package exists but often lags behind on updates and security fixes.

Run Certbot in standalone mode:

```bash
sudo certbot certonly --standalone -d yourdomain.com
```

Certbot will:
1. Start a temporary HTTP server on port 80
2. Let's Encrypt will reach out to `http://yourdomain.com/.well-known/acme-challenge/...`
3. Certbot serves the expected response
4. Let's Encrypt verifies ownership and issues the certificate
5. Certbot writes the cert files to `/etc/letsencrypt/live/yourdomain.com/`

On success you will see:

```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/yourdomain.com/fullchain.pem
Key is saved at: /etc/letsencrypt/live/yourdomain.com/privkey.pem
```

#### Verifying Auto-Renewal

Before restarting the containers, verify that Certbot's renewal configuration is working. Certbot renews using standalone mode — which needs port 80 free — so run this now while the containers are still stopped:

```bash
sudo certbot renew --dry-run
```

A successful dry run confirms that Certbot can reach Let's Encrypt and that your renewal configuration is correct.

> **Renewal caveat:** Certbot's auto-renewal timer will attempt to renew every 12 hours. Since standalone mode needs port 80, renewal will fail while your containers are running. You can solve this by registering pre/post hooks that stop and restart your containers around the renewal:

```bash
sudo sh -c 'printf "#!/bin/sh\ndocker compose -f /home/ubuntu/<your-project-folder>/docker-compose.yml down\n" > /etc/letsencrypt/renewal-hooks/pre/stop-containers.sh && chmod +x /etc/letsencrypt/renewal-hooks/pre/stop-containers.sh'

sudo sh -c 'printf "#!/bin/sh\ndocker compose -f /home/ubuntu/<your-project-folder>/docker-compose.yml up -d\n" > /etc/letsencrypt/renewal-hooks/post/start-containers.sh && chmod +x /etc/letsencrypt/renewal-hooks/post/start-containers.sh'
```

> This causes a brief downtime (~30 seconds) during renewal. In the next section, we will set up ACM + ALB, which handles renewal automatically with zero downtime.

Now restart the containers:

```bash
sudo docker compose up -d
```

This time, the NGINX container starts with the updated `default.conf` and has access to the certificate files via the volume mount.

#### Verifying HTTPS

Open a browser and navigate to:

```
https://yourdomain.com
```

You should see the padlock icon in the address bar and your application loading normally. Any request to `http://yourdomain.com` will be automatically redirected to HTTPS.

---

### Part 2 — ACM + ALB (AWS-Native Approach)

#### Why Use ACM + ALB?

Certbot is excellent for smaller deployments and gives you full visibility into the certificate files and configuration. In enterprise AWS environments, however, SSL is typically handled differently:

- Certificates are managed centrally through **AWS Certificate Manager (ACM)**
- SSL **terminates at the load balancer** — the ALB handles the HTTPS connection and forwards plain HTTP to your EC2 instance
- You never touch certificate files or nginx SSL config
- Auto-renewal is handled by AWS with no expiry management required

> **Key idea:** With ACM + ALB, your EC2 instance never sees HTTPS traffic. The load balancer decrypts the request and forwards it internally over HTTP. NGINX goes back to listening on port 80 only.

This architecture also provides the foundation for horizontal scaling — when you eventually want to run multiple EC2 instances, requests are distributed across them by the same ALB.

---

#### Step 1 — Request an ACM Certificate

1. In the AWS Console, navigate to **Certificate Manager (ACM)**

    > **Important:** Request the certificate in the **same AWS region** where you will create your ALB. ACM certificates are region-specific — an ALB in `us-east-2` cannot use a certificate issued in `us-east-1`.

2. Click **Request** → **Request a public certificate** → **Next**
3. Under **Fully qualified domain name**, enter `yourdomain.com`
4. Choose **DNS validation** (recommended — Route 53 can add the required record automatically)
5. Click **Request**

After the request is created, click into it. You will see the **Domains** section showing a status of **Pending validation** and a CNAME record that needs to be added to your DNS.

If your domain is in Route 53, click **Create records in Route 53** — AWS will add the CNAME record automatically. Within a few minutes the certificate status will change to **Issued**.

> If you are using an external DNS provider, copy the CNAME name and value and add it manually in your registrar's DNS settings.

---

#### Step 2 — Create a Target Group

A **Target Group** tells the ALB which servers to forward traffic to and how to check if they are healthy.

1. In the EC2 console, navigate to **Load Balancing** → **Target Groups** → **Create target group**
2. Configure:
   - **Target type**: Instances
   - **Target group name**: a descriptive name (e.g., `my-app-targets`)
   - **Protocol**: HTTP
   - **Port**: 80
   - **IP address type**: IPv4
   - **VPC**: select the default VPC (the same one your EC2 instance is in — if you only have one VPC it will be pre-selected)
   - **Protocol version**: HTTP1 (the default — leave this as-is)
3. Under **Health checks**:
   - **Protocol**: HTTP
   - **Path**: `/` (or `/api/v1/` if your root returns a 404)
4. Click **Next** → on the **Register targets** screen, select your EC2 instance → click **Include as pending below**
5. Click **Create target group**

---

#### Step 3 — Create an Application Load Balancer

1. In the EC2 console, navigate to **Load Balancing** → **Load Balancers** → **Create load balancer**
2. Select the **Application Load Balancer** card and click **Create**
3. Configure:
   - **Name**: a descriptive name (e.g., `my-app-alb`)
   - **Scheme**: Internet-facing
   - **IP address type**: IPv4
   - **VPC**: default VPC
   - **Mappings**: select at least two Availability Zones (required for ALBs)
4. Under **Security groups**: create or select a security group that allows inbound traffic on ports **80** and **443** from `0.0.0.0/0`. You can use the same security group as your EC2 instance if it already allows these ports, or create a dedicated one for the ALB.
5. Under **Listeners and routing**:
   - **HTTP (port 80)**: set the default action to **Redirect to HTTPS** (port 443, status code 301)
   - **Add a listener** for **HTTPS (port 443)**: set the default action to **Forward to** your target group
   - In the HTTPS listener row, under **Default SSL/TLS server certificate**, choose **From ACM** and select your issued certificate from the dropdown
6. Click **Create load balancer**

> **Note:** You may see a "Resource map" panel in the wizard showing a visual diagram of your listener-to-target-group routing. This is informational only — no action is needed there.

---

#### Step 4 — Update DNS to Point to the ALB

Now that the ALB is handling traffic, your domain's A record should point to the ALB instead of directly to your EC2 instance.

In Route 53 → Hosted zones → your domain:

1. Click the existing A record and edit it
2. Enable the **Alias** toggle
3. Under **Route traffic to**, select **Alias to Application and Classic Load Balancer**
4. Select your region and choose your ALB from the dropdown
5. Save the record

> **Why Alias instead of CNAME?** ALBs have DNS names (e.g., `my-app-alb-1234567890.us-east-1.elb.amazonaws.com`), not IP addresses — and those DNS names can resolve to different IPs over time. Route 53 Alias records are AWS-specific and handle this gracefully. Standard CNAME records cannot be used at the root of a domain (`yourdomain.com` without a subdomain).

If you are using an external DNS provider, add a **CNAME** record pointing `yourdomain.com` to your ALB's DNS name. Note: CNAME at the root domain is not supported by all providers — you may need to use `www.yourdomain.com` or consult your provider's documentation.

---

#### Step 5 — Revert NGINX to HTTP Only

With the ALB handling SSL termination, NGINX no longer needs to serve HTTPS. Traffic from the ALB to your EC2 instance arrives on port 80 as plain HTTP.

Update `default.conf` back to a simple HTTP configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri /index.html;
    }
}
```

Update `docker-compose.yml` — remove port 443 and the `/etc/letsencrypt` volume mount:

```yaml
frontend:
  build: ./client
  ports:
    - "80:80"
  depends_on:
    - backend
```

> **Keep your existing volume mounts.** As before, this snippet only highlights the fields that change. Preserve any other volume mounts your `frontend` service already has.

Push the changes, pull on EC2, and restart:

```bash
# Locally
git add .
git commit -m "revert NGINX to HTTP — SSL terminates at ALB"
git push origin main

# On EC2
git pull origin main
sudo docker compose down
sudo docker compose up -d
```

---

#### Step 6 — Verify HTTPS via the ALB

Once DNS propagates (which may take a few minutes), navigate to:

```
https://yourdomain.com
```

HTTPS is now handled entirely by the ALB and ACM. Your EC2 instance receives plain HTTP traffic internally. The padlock in the browser reflects the ALB's ACM certificate.

---

#### Optional — Harden Security Groups

With the ALB in front of your EC2 instance, there are now two security groups in play:

| Security Group | Needs Inbound | From |
|---|---|---|
| **ALB security group** | Port 80 (HTTP) and Port 443 (HTTPS) | `0.0.0.0/0` (the internet) |
| **EC2 security group** | Port 80 (HTTP) | The ALB security group only |

By default, your EC2 instance's security group allows HTTP traffic from anywhere (`0.0.0.0/0`) on port 80. Now that all traffic arrives through the ALB, you can restrict port 80 to accept traffic only from the ALB — reducing the direct attack surface on your instance.

1. In EC2 → Security Groups, find the security group attached to your EC2 instance
2. Edit the inbound rules for port 80
3. Change the source from `0.0.0.0/0` to the **security group ID** of the ALB's security group (start typing `sg-` and select it from the dropdown)

This way, only the ALB can reach your instance on port 80. Direct HTTP requests to the EC2 public IP will be rejected at the network level.

---

## Conclusion

Your application is now fully secured with HTTPS. You have gone from a raw HTTP deployment to a production-grade setup where every request is encrypted in transit.

In this lesson you:

- Obtained a free TLS certificate using Certbot and updated your NGINX and Docker configuration to serve HTTPS
- Requested and validated an ACM certificate through the AWS console
- Created a Target Group and Application Load Balancer with HTTP-to-HTTPS redirect
- Updated DNS to route traffic through the ALB and reverted NGINX to HTTP-only
- Optionally hardened your EC2 security group to allow traffic only from the ALB
