# Server Side Logging

## Intro

As web applications grow in complexity and scale, understanding what is happening on the server becomes just as important as making the server fast. Server-side logging provides visibility into application behavior, errors, performance bottlenecks, and security events. In Django and Django REST Framework (DRF) applications, logging is a foundational tool for debugging, monitoring, and operating APIs reliably in production—especially when multiple users, background processes, and external services are involved.

---

## What is Logging

Logging is the practice of recording structured or semi-structured messages about what an application is doing at runtime. These messages may describe normal application flow (e.g., requests received), unexpected conditions (e.g., errors or exceptions), or significant events (e.g., authentication failures). Server-side logging occurs entirely on the backend and is independent of the client. Logs are typically written to files, standard output, or centralized logging systems where they can be searched and analyzed later.

---

### Why Logging

Server-side logging solves several critical problems that arise in real-world systems:

- **Debugging**: Understand why something broke after it already happened
- **Observability**: See how the system behaves under real usage
- **Accountability**: Track actions taken by users or services
- **Incident response**: Investigate outages, security issues, or data anomalies

Without logging, production systems become opaque—issues may only surface as vague user complaints with no actionable information for developers.

---

### Real World Relevance

Consider an application like Instagram. When a user uploads a photo, dozens of things happen behind the scenes: authentication checks, file processing, database writes, cache updates, and background tasks. If something fails (e.g., the image processing service times out), logs allow engineers to trace exactly where and why the failure occurred. Logging ensures that issues can be diagnosed quickly without relying on users to describe technical problems.

---

### When to use logging

| Scenario | Use Logging? | Reason |
|--------|--------------|--------|
| API request received | ✅ Yes | Trace application flow |
| Authentication or permission failure | ✅ Yes | Security and auditing |
| Expected validation errors | ⚠️ Sometimes | Log sparingly to avoid noise |
| Unhandled exceptions | ✅ Yes | Critical debugging information |
| High-frequency internal loops | ❌ No | Excessive noise and log volume |

---

## Applying it to a Django API View

### Step 1: Configure Logging in Django

Django uses Python’s built-in `logging` module. Logging behavior is configured centrally in `settings.py`.

```python
# settings.py
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
```

This configuration:

* Sends logs to standard output (ideal for Docker and cloud environments)
* Logs messages at `INFO` level and above
* Applies globally across the Django application

---

### Step 2: Using a Logger in a View

Django applications typically create a module-level logger.

```python
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

logger = logging.getLogger(__name__)
```

```python
class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info("Profile requested", extra={"user_id": request.user.id})
        return Response({
            "username": request.user.username,
            "email": request.user.email,
        })
```

**What this does:**

* Creates a logger scoped to the module
* Records an informational message when the endpoint is accessed
* Adds contextual data (user ID) for traceability

**Why it’s necessary:**
Logs allow you to reconstruct what happened on the server long after a request has completed.

---

### Step 3: Logging Errors and Exceptions

Errors should be logged with appropriate severity.

```python
class UpdateProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            update_user_profile(request.user, request.data)
        except Exception as e:
            logger.exception(
                "Failed to update profile",
                extra={"user_id": request.user.id}
            )
            raise
```

Using `logger.exception()`:

* Automatically includes the stack trace
* Preserves context for debugging
* Ensures critical failures are visible

---

### Step 4: Logging Levels (Choosing the Right One)

| Level    | When to Use                           |
| -------- | ------------------------------------- |
| DEBUG    | Development-only diagnostic details   |
| INFO     | Normal application events             |
| WARNING  | Unexpected but recoverable conditions |
| ERROR    | Failed operations                     |
| CRITICAL | System-level failures                 |

Choosing correct levels ensures logs remain useful instead of overwhelming.

---

### Step 5: Logging vs Caching (Important Contrast)

| Caching                 | Logging                          |
| ----------------------- | -------------------------------- |
| Optimizes performance   | Optimizes visibility             |
| Stores data temporarily | Records events permanently       |
| Avoids repeated work    | Explains what work occurred      |
| Impacts response speed  | Impacts debugging and monitoring |

Both are server-side concerns, but they solve entirely different problems and are often used together in production systems.

---

## Logging Considerations for Authenticated APIs

When logging authenticated requests:

* **Never log secrets** (tokens, passwords, API keys)
* Prefer logging user IDs over usernames or emails
* Be mindful of privacy and compliance requirements
* Avoid logging full request bodies unless necessary

> ⚠️ Logs are often centralized and retained long-term—treat them as sensitive data.

---

## Conclusion

Server-side logging is an essential operational tool for Django and DRF applications. While caching improves performance, logging provides insight, accountability, and confidence in production systems. By logging thoughtfully—using appropriate levels, structured context, and secure practices—developers can build APIs that are not only fast, but also observable, debuggable, and reliable at scale.

