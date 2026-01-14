# Full-Stack Workflow

## What are we trying to accomplish

In this lesson, we focus on **building and reasoning about a complete full-stack application workflow**, specifically centered around **authentication and CRUD operations**. Rather than treating the frontend and backend as separate exercises, this lesson emphasizes how the two layers **communicate, share responsibility, and maintain state together** in a real-world system.

You will learn how a React frontend interacts with a Django REST API using Axios, how authentication state is established and persisted using tokens, and how protected backend endpoints enforce access control. From there, you will extend this authenticated connection to support full CRUD operations against a relational data model, ensuring that all data access is scoped to the authenticated user.

By the end of this lesson, you will understand how **frontend routing, API design, authentication, and state management work together** to form a cohesive application. These skills are foundational for building production-ready full-stack applications and directly transfer to larger systems involving more complex permissions, relationships, and deployment environments.

---

## Lectures & Assignments

### Lectures

- [Lecture – Full-Stack Authentication](./1-authentication.md)
- [Lecture – Full-Stack CRUD ](./2-crud.md)

### [Assignments](./assignments.md)

---

## Terminal Learning Objectives (TLO's)

* Explain how a React frontend communicates with a Django REST API
* Implement token-based authentication across the full stack
* Persist authentication state across page refreshes
* Protect backend endpoints using DRF permissions
* Connect Axios requests to authenticated API views
* Perform full CRUD operations from the frontend
* Synchronize frontend state with backend data mutations
* Reason about user-scoped data access and ownership
* Design a clean user flow for login, logout, and protected pages
* Debug authentication and authorization issues in a full-stack system

---

## Enabling Learning Objectives (ELO's)

* Define the role of Axios in frontend-to-backend communication
* Explain how DRF Token Authentication works
* Differentiate between authenticated and unauthenticated API views
* Understand how React Router loaders affect application initialization
* Use localStorage to persist authentication tokens
* Apply Authorization headers correctly in API requests
* Interpret HTTP status codes in the context of CRUD operations
* Manage frontend state updates after create, update, and delete actions
* Reason about CSRF, tokens, and stateless APIs
* Connect full-stack patterns to real-world application architectures
