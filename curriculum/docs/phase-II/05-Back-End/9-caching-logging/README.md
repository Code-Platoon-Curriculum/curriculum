# Server Side Performance (Caching) & Observability (Logging)

## What are we trying to accomplish

In this module, we focus on **operating and scaling backend APIs responsibly in real-world environments**. Building a correct API is only the first step—production systems must also be **fast, observable, and debuggable**. Through server-side caching and server-side logging, you will learn how backend engineers reduce load, improve response times, and gain visibility into application behavior once software is deployed.

By the end of this module, you will understand how to **optimize read-heavy workloads using caching**, how to **avoid common pitfalls with authenticated data**, and how to **instrument your Django and DRF applications with meaningful logs**. These concepts form the foundation of production readiness and are critical for debugging issues that cannot be reproduced locally.

---

## Lectures & Assignments

### Lectures

- [Lecture - Server Side Caching](./1-caching.md)
- [Lecture - Server Side Logging](./2-logging.md)

### [Assignments](./assignments.md)

---

## Terminal Learning Objectives (TLO's) executable

* Explain the role of server-side caching in performance optimization
* Identify when caching is appropriate and when it is harmful
* Configure Django cache backends for development environments
* Apply view-level caching and understand its limitations with authenticated users
* Implement per-user caching using Django’s low-level cache API
* Explain the purpose of server-side logging in production systems
* Configure Django logging using Python’s logging framework
* Log application events, errors, and exceptions using appropriate log levels
* Distinguish between caching and logging as operational concerns
* Apply security-conscious logging practices for authenticated APIs

---

## Enabling Learning Objectives (ELO's) enabling

* Define key caching terminology: cache backend, TTL, cache key, cache-aside pattern
* Compare in-memory caching with production-grade solutions such as Redis
* Identify and prevent data leakage caused by improper cache key design
* Reason about per-user cache strategies in token-authenticated APIs
* Define logging terminology: logger, handler, formatter, log level
* Differentiate between DEBUG, INFO, WARNING, ERROR, and CRITICAL logs
* Instrument Django API views with contextual logging
* Analyze how logs support debugging, monitoring, and incident response
* Recognize common anti-patterns such as over-logging or logging sensitive data
* Connect caching and logging decisions to real-world system reliability and maintainability
