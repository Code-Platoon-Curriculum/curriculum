# ALB: Connecting the Architecture

## Introduction

At the end of Lecture 1, your React app was loading from CloudFront but every API call was failing. CloudFront had no route to your Django server, and Route53 was still pointing to the old EC2 address. Today you will close that gap.

You will create an **Application Load Balancer (ALB)** to sit in front of your EC2 and handle incoming API traffic. Then you will register the ALB as a second origin in your CloudFront distribution and add a routing rule: any request matching `/api/*` gets forwarded to the ALB instead of S3. Once that is wired up, you will update Route53 to point your custom domain to CloudFront, making the distribution the single entry point for your entire application.

When this lecture is done, the architecture will look like this:

```
Route53 → your-domain.com
               │
        CloudFront (single distribution)
        ├── /api/* → ALB → EC2 (Django + Gunicorn)
        └── /*     → S3 bucket (React build)
```

The NGINX container in your Docker Compose will be gone. SSL termination moves to the ALB using an ACM certificate instead of Certbot. The EC2 only runs Django and PostgreSQL.

---

### What Is an ALB?

An **Application Load Balancer** is a managed AWS service that distributes incoming HTTP/HTTPS traffic across one or more backend targets — in this case, EC2 instances. It operates at Layer 7 (the application layer), meaning it can make routing decisions based on the URL path, host header, or other request attributes.

The key components you will configure:

- **Security Group** — controls which traffic the ALB accepts. You will open ports 80 and 443 to the internet.
- **Target Group** — the set of backends the ALB routes traffic to. You will register your EC2 instance here on port 8000 (where Gunicorn listens).
- **Health Check** — the ALB periodically sends a request to each target to confirm it is alive. If a target fails health checks, the ALB stops sending it traffic. This is what enables horizontal scaling: you can add more EC2s to the target group and the ALB distributes load across all healthy ones automatically.
- **Listener** — a rule attached to a port that tells the ALB what to do with incoming connections. You will create two: one on port 80 that redirects to HTTPS, and one on port 443 that forwards to the target group.

The ALB also handles **SSL termination**. HTTPS connections terminate at the ALB using an ACM certificate. Traffic from the ALB to EC2 travels over your private VPC network on plain HTTP — the EC2 never deals with SSL. This replaces Certbot entirely.

---

### Refactoring Docker Compose

Before touching AWS, update your `docker-compose.yml` on EC2. The NGINX container served the React build and proxied API traffic. Both of those jobs are now handled by AWS services (S3/CloudFront and ALB respectively), so the container is no longer needed.

Your current `docker-compose.yml` has three services: `db`, `backend`, and `frontend` (the NGINX container). Remove the `frontend` service entirely and expose port 8000 on the `backend` service so the ALB can reach Gunicorn directly.

```yaml
# docker-compose.yml (updated)
services:
  db:
    image: postgres:15
    container_name: postgres-container
    env_file:
      - .env

  backend:
    build: ./server
    container_name: django-container
    command: sh -c "gunicorn task_proj.wsgi --bind 0.0.0.0:8000"
    env_file:
      - .env
    ports:
      - "8000:8000"   # ALB health checks and traffic reach Gunicorn here
    volumes:
      - ./server:/app
    depends_on:
      - db
```

You can also delete `default.conf` from the project root — it was the NGINX configuration and is no longer referenced.

SSH into your EC2, pull the updated `docker-compose.yml`, and redeploy:

```bash
# On the EC2 instance
docker compose down
docker compose up -d --build
```

Confirm Gunicorn is listening:

```bash
curl http://localhost:8000/api/v1/test/
# Expected: {"connected": true}
```

---

### Setting Up the ALB

**Step 1 — Request an ACM certificate for the ALB**

The ACM certificate you created in Lecture 1 was in `us-east-1` for CloudFront. The ALB requires its own certificate in the **same region as the ALB** — this is a separate certificate even if the domain names are identical.

Switch the console to your EC2's region. Navigate to ACM and request another public certificate with the same domain names (`your-domain.com`, `www.your-domain.com`). Use DNS validation and create the Route53 records. If the CNAME records from the first cert already exist in Route53, validation will complete immediately.

**Step 2 — Create the ALB Security Group**

Navigate to EC2 → Security Groups → **Create security group**.

- Name: `alb-sg`
- VPC: your default VPC
- Inbound rules:
  - HTTP (port 80) from `0.0.0.0/0`
  - HTTPS (port 443) from `0.0.0.0/0`
- Outbound rules: leave defaults (all traffic)

**Step 3 — Update the EC2 Security Group**

Your EC2's security group currently allows inbound traffic on ports 80 and 443 from anywhere (NGINX was handling those). Remove those rules and replace them with a single rule that allows port 8000 from the ALB security group only. This ensures Django is only reachable through the ALB, never directly from the internet.

Navigate to the EC2 security group and edit inbound rules:

- Remove HTTP (80) and HTTPS (443) inbound rules
- Add: Custom TCP, port **8000**, source: **alb-sg** (select the security group you just created by name)

**Step 4 — Create a Target Group**

Navigate to EC2 → Target Groups → **Create target group**.

- Target type: **Instances**
- Protocol: **HTTP**
- Port: **8000**
- VPC: your default VPC
- Health check protocol: HTTP
- Health check path: `/api/v1/test/`

The `/api/v1/test/` endpoint is unauthenticated and always returns a 200 response — this makes it a reliable health check target. Endpoints that require authentication will return 401, which the ALB would interpret as an unhealthy target.

On the next screen, select your EC2 instance from the list and click **Include as pending below**, then **Create target group**.

**Step 5 — Create the ALB**

Navigate to EC2 → Load Balancers → **Create load balancer** → **Application Load Balancer**.

- Name: `app-alb`
- Scheme: **Internet-facing**
- IP address type: IPv4
- VPC: your default VPC
- Availability zones: select **at least two** AZs and their corresponding subnets (the ALB requires a minimum of two for high availability)
- Security groups: select **alb-sg**

Under **Listeners and routing**:

- **HTTP (port 80)**: action → Redirect to HTTPS (port 443)
- **HTTPS (port 443)**: action → Forward to your target group; select the ACM certificate you just created

Click **Create load balancer**.

Wait for the ALB state to change from `provisioning` to `active`. Then go to your target group and confirm the registered EC2 shows a health status of **Healthy**. If it shows **Unhealthy**, verify:

1. The EC2 security group allows port 8000 from `alb-sg`
2. Gunicorn is running (`curl http://localhost:8000/api/v1/test/` from inside EC2 returns 200)
3. The health check path is exactly `/api/v1/test/`

---

### Adding the ALB as a CloudFront Origin

With the ALB healthy, navigate to your CloudFront distribution from Lecture 1.

**Step 1 — Create the ALB origin**

Go to the **Origins** tab and click **Create origin**.

- **Origin domain**: paste the ALB's DNS name (found on the load balancer detail page — it looks like `app-alb-1234567890.us-east-1.elb.amazonaws.com`)
- **Protocol**: HTTPS only
- **HTTPS port**: 443

Click **Create origin**.

**Step 2 — Create the `/api/*` behavior**

Go to the **Behaviors** tab and click **Create behavior**.

- **Path pattern**: `/api/*`
- **Origin**: select the ALB origin you just created
- **Allowed HTTP methods**: GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE — the API uses all of them
- **Cache policy**: **CachingDisabled** — API responses contain user-specific data and must never be cached
- **Origin request policy**: **AllViewer** — this forwards the original Host header, all cookies (including your JWT access and refresh tokens), and all query strings to the ALB

The `AllViewer` origin request policy is critical for authentication. Your JWT tokens live in HttpOnly cookies. If CloudFront strips cookies before forwarding to the ALB, Django will never see them and every request will return 401.

Click **Save changes**. CloudFront will take a few minutes to deploy the new behavior to all edge locations.

**Understanding behavior priority**: CloudFront evaluates behaviors from most specific to least specific. The `/api/*` behavior takes priority over the default `/*` behavior automatically because it is more specific. Requests to `/api/anything` go to the ALB; all other requests go to S3.

---

### Cutting Over Route53

Navigate to Route53 → Hosted zones → your domain → find the **A record** for `your-domain.com`.

Click **Edit record**:

- **Alias**: Yes
- **Route traffic to**: Alias to CloudFront distribution
- **Select distribution**: your CloudFront distribution

Save the record. DNS propagation typically takes 1–5 minutes.

If you also have an A record for `www.your-domain.com`, update it the same way to point to the same CloudFront distribution.

---

### Verifying the Full Stack

Once DNS propagates, open your browser and navigate to `https://your-domain.com`.

Work through the following checks:

**Frontend delivery**

The React app loads. Open DevTools → Network, reload, and inspect any `.js` bundle. The response header `x-cache: Hit from cloudfront` confirms the file was served from a CDN edge location, not from EC2.

**Authentication**

Register a new user or log in. The `/api/v1/users/login/` request goes through CloudFront → ALB → EC2. On success, the response sets two HttpOnly cookies (`access`, `refresh`). Confirm this in DevTools → Application → Cookies.

**JWT token refresh**

The axios interceptor in `utilities.jsx` automatically calls `/api/v1/users/refresh/` when a 401 response is received and the request has not already been retried. The access token cookie is set to expire in 1 minute (see `create_time_for_cookie(minutes=1)` in `views.py`) while the JWT claim itself is valid for 15 minutes (configured via `SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]` in `settings.py`). The browser drops the cookie after 1 minute, causing the next API call to return 401 and triggering the interceptor. Wait at least 1 minute after logging in, then perform any authenticated action and verify that the interceptor silently refreshes the token and retries the original request.

**Data operations**

Create a task, edit it, and delete it. Each operation calls a different HTTP method (`POST`, `PUT`, `DELETE`) against `/api/v1/tasks/`. Confirm all return expected status codes in DevTools.

**EC2 process check**

SSH into your EC2 and run:

```bash
docker ps
```

You should see exactly two containers running: `django-container` and `postgres-container`. The `nginx-container` is gone.

**ALB target health**

In the AWS console, navigate to your target group. The registered EC2 instance should show **Healthy** status.

---

## Conclusion

The architecture is now fully decoupled and horizontally scalable:

```
Route53 → your-domain.com
               │
        CloudFront (single distribution)
        ├── /api/* → ALB → EC2 (Django + Gunicorn)
        └── /*     → S3 bucket (React build)
```

What changed and why it matters:

- **NGINX is gone.** Its three responsibilities were split to the right tools: S3 and CloudFront serve static files, the ALB handles routing and SSL termination, and Gunicorn focuses purely on running Django.
- **SSL is managed by ACM.** No more manual Certbot renewals. ACM auto-renews certificates before they expire.
- **The frontend is globally cached.** Static assets are served from the edge location closest to each user, not from a single EC2 in one region.
- **The backend is load-balanced.** Right now there is one EC2 in the target group. To scale horizontally, you launch additional EC2 instances with the same Docker Compose configuration, register them in the target group, and the ALB distributes traffic across all healthy instances automatically — no changes to CloudFront, Route53, or the application code required.
