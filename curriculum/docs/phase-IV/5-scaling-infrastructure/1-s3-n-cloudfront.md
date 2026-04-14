# S3 + CloudFront: Hosting a React SPA on the Edge

## Introduction

Your application is currently running entirely on a single EC2 instance. NGINX handles three jobs at once: serving the React build, proxying API traffic to Gunicorn, and terminating SSL. That setup got you to production, but it has a structural problem — if that EC2 goes down, everything goes down. The frontend, the API, and the SSL termination all disappear at once.

Today you will pull the React frontend out of EC2 entirely and hand it off to two AWS services designed specifically for serving static files: **S3** for storage and **CloudFront** for global delivery. By the end of this lecture, your React app will be accessible via a CloudFront URL and will be cached at AWS edge locations around the world. The API will still be unreachable until Lecture 2 — that is intentional. You are migrating one piece at a time so the deployment is never in an unpredictable broken state.

---

### What Is Object Storage?

A traditional file system stores files in directories on a disk attached to a machine. Object storage works differently — files are stored as independent objects in a flat namespace called a **bucket**, each identified by a unique key. There are no folders in the traditional sense; the key `/assets/index-abc123.js` just looks like a path, but it is simply the object's name.

**Amazon S3 (Simple Storage Service)** is AWS's object storage service. Every file you put into S3 is an object. Buckets are the containers that hold objects, and each bucket lives in a specific AWS region.

When you run `npm run build`, Vite generates a `dist/` directory:

```
dist/
├── index.html
├── vite.svg
└── assets/
    ├── index-[hash].js
    └── index-[hash].css
```

Vite appends a content hash to each filename (e.g., `index-CvJ6JpQi.js`) so browsers never serve stale cached bundles after a new deploy. The exact filenames will differ between builds — that is intentional. These files are entirely static — no server needed to compute them. They are exactly what object storage was built for. You upload the contents of `dist/` to an S3 bucket and S3 can serve them over HTTP.

---

### What Is a CDN and CloudFront?

A **Content Delivery Network (CDN)** is a globally distributed network of servers called **edge locations**. When a user requests a file, the CDN routes that request to the edge location geographically closest to them rather than to the origin server. The edge location either returns a cached copy immediately or fetches it from the origin once and caches it for future requests.

**Amazon CloudFront** is AWS's CDN. A CloudFront **distribution** is the configuration that tells CloudFront where to get your content (the **origin**), how to cache it, and what domains to respond on.

Key concepts:

- **Origin** — where CloudFront fetches content from when its cache is empty. In this lecture, S3 is the origin.
- **Behavior** — a rule that matches a URL path pattern and defines cache settings and which origin to use. Every distribution has at least one default behavior (`/*`).
- **OAC (Origin Access Control)** — a CloudFront identity that S3 trusts. This lets you keep the S3 bucket fully private (no public access) while CloudFront can still read from it. Users never talk to S3 directly.
- **Distribution domain** — every CloudFront distribution gets a default domain like `d1a2b3c4xyz.cloudfront.net`. You can attach your own custom domain on top of it.

For a React SPA, the CDN benefit is significant: your JavaScript bundles are large and identical for every user. CloudFront caches them at edge locations and serves them with sub-50ms latency regardless of where your EC2 lives.

---

### Setting Up S3

**Step 1 — Create the bucket**

Go to the AWS Console, navigate to S3, and click **Create bucket**.

- **Bucket name**: use something descriptive and globally unique, e.g., `your-domain-frontend`. Bucket names are globally unique across all AWS accounts.
- **Region**: select the same region your EC2 is in.
- **Block Public Access**: leave all four checkboxes checked. You do not want the bucket publicly accessible — CloudFront's OAC will be the only entity reading from it.

Click **Create bucket**.

**Step 2 — Build the React app**

On your local machine, inside the `client/` directory:

```bash
npm run build
```

Confirm the `dist/` directory was generated and contains `index.html` and an `assets/` folder.

**Step 3 — Upload the build to S3**

Click into your new bucket. Click **Upload**, then drag and drop the **contents** of `dist/` — not the `dist/` folder itself. S3 should receive `index.html`, any top-level static assets (e.g., `vite.svg`), and the entire `assets/` folder with the hashed JS and CSS bundles.

If you have the AWS CLI configured, you can use sync instead:

```bash
# Upload from the client/dist directory
aws s3 sync dist/ s3://your-domain-frontend
```

The `sync` command only uploads files that changed, which makes future deployments fast.

---

### Setting Up CloudFront

**Step 1 — Request an ACM certificate**

CloudFront requires SSL certificates issued by **AWS Certificate Manager (ACM)**. There is a critical constraint: CloudFront only accepts ACM certificates created in the **us-east-1 (N. Virginia)** region, regardless of where your EC2 or S3 bucket lives.

Switch your console region to **us-east-1**. Navigate to ACM and click **Request a certificate**.

- Certificate type: **Public**
- Domain names: add both `your-domain.com` and `www.your-domain.com`
- Validation method: **DNS validation**

After requesting, ACM provides CNAME records you must add to Route53. Click into the certificate, expand the domain section, and click **Create records in Route53** — ACM does this automatically if your hosted zone is in the same account. Validation typically completes within a few minutes.

Keep this tab open — you will come back to select this certificate inside CloudFront.

**Step 2 — Create the CloudFront distribution**

Navigate to CloudFront and click **Create distribution**.

Under **Origin**:

- **Origin domain**: select your S3 bucket from the dropdown
- **Origin access**: select **Origin access control settings (recommended)**
- Click **Create new OAC** and accept the defaults

CloudFront will display a yellow banner after creation reminding you to update the S3 bucket policy. You will do that in a moment.

Under **Default cache behavior**:

- **Viewer protocol policy**: Redirect HTTP to HTTPS
- **Allowed HTTP methods**: GET, HEAD

Under **Settings**:

- **Alternate domain name (CNAME)**: add `your-domain.com` and `www.your-domain.com`
- **Custom SSL certificate**: select the ACM certificate you just created (it only appears here if it was created in us-east-1)

Click **Create distribution**. CloudFront will take 5–10 minutes to deploy to edge locations.

**Step 3 — Apply the S3 bucket policy**

After the distribution is created, you will see a banner at the top of the screen:

> "S3 bucket policy needs to be updated"

Click **Copy policy**, then navigate back to your S3 bucket → **Permissions** → **Bucket policy** → **Edit**, paste the policy, and save. This policy grants CloudFront's OAC permission to `GetObject` from the bucket. Without it, CloudFront cannot read your files.

The generated policy looks like this:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::your-domain-frontend/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::YOUR_ACCOUNT_ID:distribution/YOUR_DIST_ID"
                }
            }
        }
    ]
}
```

**Step 4 — Configure custom error pages for React Router**

React Router handles navigation client-side. When a user visits `your-domain.com/tasks` directly (or refreshes the page on that route), the request goes to S3 looking for an object at the key `/tasks`. That object does not exist — S3 returns a 403 or 404. Without correction, the user sees an error instead of your app.

The fix is to tell CloudFront: whenever S3 returns a 403 or 404, respond with the contents of `/index.html` and set the HTTP status code to 200. React Router then takes over from the browser and renders the correct component.

In your CloudFront distribution, go to the **Error pages** tab and click **Create custom error response**:

| HTTP error code | Response page path | HTTP response code |
|---|---|---|
| 403 | /index.html | 200 |
| 404 | /index.html | 200 |

Repeat for both error codes.

---

### Verifying the Frontend

Wait for the distribution status to show **Enabled** and the last modified timestamp to update. Then open your browser and navigate to the CloudFront distribution domain (e.g., `https://d1a2b3c4xyz.cloudfront.net`).

Your React app should load. Any API calls will fail with network errors — this is expected. CloudFront does not yet know how to reach your Django backend, and Route53 has not been updated to point your custom domain here. You will complete both in Lecture 2.

To confirm the CDN is working correctly, open your browser DevTools → Network tab. Reload the page and click on one of the JavaScript bundle requests. Look for the response header:

```
x-cache: Hit from cloudfront
```

A "Hit" means the file was served from an edge location cache. A "Miss" means CloudFront fetched it from S3 for the first time and will cache it for subsequent requests.

---

## Conclusion

You have decoupled the React frontend from EC2. The `dist/` build now lives in S3 and is distributed globally through CloudFront's edge network. NGINX no longer has to serve static files — that responsibility belongs to a managed service built specifically for it.

Here is the current state of the architecture:

```
Browser → CloudFront (d1a2b3c4xyz.cloudfront.net)
                │
                └── /* → S3 bucket (React build)
```

In Lecture 2, you will:

1. Modify `docker-compose.yml` to remove the NGINX container
2. Create an ALB that sits in front of your EC2's Django/Gunicorn process
3. Add the ALB as a second origin in this CloudFront distribution
4. Route `/api/*` through CloudFront → ALB → EC2
5. Update Route53 so your custom domain points to CloudFront

At that point the full architecture will be live and the app will be fully functional at your domain.
