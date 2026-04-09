# Axios Interceptors

## Introduction

In the previous lesson we replaced DRF's stateful token system with JWTs. Our access token now expires after 15 minutes — intentionally. A short-lived token limits damage if it is ever intercepted. But that creates a new problem: after 15 minutes, every API call our React application makes will receive a `401 Unauthorized` response, and the user will appear to be logged out mid-session.

We already built a `refresh/` endpoint that silently issues a new access token using the long-lived refresh cookie. All that is left is to wire the frontend up so it calls that endpoint automatically whenever it encounters a 401, then retries the original request — without the user ever noticing. That is exactly what an **Axios interceptor** is for.

---

## Lesson

### What is an Axios Interceptor

Axios interceptors are functions that run automatically on every request or response that passes through an Axios instance — before the request reaches the server, or before the response reaches your component code. Think of them as **middleware for your HTTP client**.

Axios gives you two attachment points:

- **Request interceptors** — run before a request is sent. Useful for injecting headers, logging, or modifying the request config.
- **Response interceptors** — run after a response comes back. Useful for normalizing errors, logging, or — in our case — handling expired tokens.

Both types follow the same shape: a success handler and an error handler.

```javascript
axiosInstance.interceptors.response.use(
    (response) => response,        // success: pass the response through
    (error) => { /* handle */ }    // error: intercept failed responses
)
```

We only need a **response interceptor**. Our goal is to sit between the server's `401` response and our component code, perform a silent refresh, and retry — so the component never sees the failure.

---

### The Problem Without an Interceptor

Right now our `utilities.jsx` exports an `api` instance and a set of functions that call it. Every one of those functions will start returning `null` or throwing errors 15 minutes after the user logs in, because the access cookie will have expired.

Without an interceptor, the sequence looks like this:

```
1. User loads /home — access token is valid — tasks load ✓
2. User stays on the page for 16 minutes
3. User creates a new task → POST /api/v1/tasks/ → 401 Unauthorized
4. createTask() returns null → the task never appears
5. User is confused — they are still "logged in" but nothing works
```

With an interceptor, step 3 is handled transparently:

```
3. User creates a new task → POST /api/v1/tasks/ → 401 Unauthorized
   → interceptor catches the 401
   → interceptor calls POST /api/v1/users/refresh/ → new access cookie set
   → interceptor retries POST /api/v1/tasks/ → 201 Created ✓
4. Task appears normally
```

---

### Conceptually: The Security Badge Analogy

Imagine your office building uses key cards to access every door. Your card is programmed to expire every 15 minutes for security — but instead of making you walk back to HR each time it expires, the building has a guard at each door. When your card fails, the guard silently calls HR, gets your card renewed on the spot, and re-scans you in. You barely notice a pause.

Our Axios interceptor is that guard. It intercepts the rejection, calls HR (`/users/refresh/`), and retries the door (`the original request`) — all in the background, between the server's response and your component's code.

But what happens if HR itself says your credentials are invalid — your refresh token has expired too? Then the guard cannot help you. The guard sends you home (you must log in again).

---

### Implementing the Response Interceptor

Open `utilities.jsx`. We will add the interceptor directly below the `api` instance definition.

The first thing we need is a dedicated function to call the refresh endpoint. Notice it uses plain `axios` rather than our `api` instance:

```javascript
// client/src/utilities.jsx

import axios from "axios";

export const api = axios.create({
    baseURL: 'https://deployment-demo.com/api/v1/',
    withCredentials: true,
})

const refreshAccessToken = () => {
    // We call plain axios here instead of `api` on purpose.
    // If we used `api`, a failed refresh would trigger our interceptor again,
    // which would try to refresh again — an infinite loop.
    return axios.post(
        'https://deployment-demo.com/api/v1/users/refresh/',
        {},
        { withCredentials: true }
    )
}
```

Using plain `axios` for the refresh call keeps it outside the interceptor's reach. A failure there is a true failure — no retry, no loop.

Now attach the interceptor to `api`:

```javascript
// client/src/utilities.jsx

api.interceptors.response.use(
    // success handler: just pass the response through untouched
    (response) => response,

    // error handler: runs on any non-2xx response
    async (error) => {
        const originalRequest = error.config;

        // Only intercept 401s, and only once per request (_retry flag)
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;  // mark so we don't retry again
            try {
                await refreshAccessToken();
                // The server has now set a fresh access cookie.
                // Re-run the original request — it will succeed this time.
                return api(originalRequest);
            } catch (refreshError) {
                // Refresh also failed — the session is truly expired.
                // Propagate the error so the calling code can handle it.
                return Promise.reject(refreshError);
            }
        }

        // For all other errors (400, 403, 404, 500…) pass them through
        return Promise.reject(error);
    }
)
```

The `_retry` flag on `originalRequest` is the guard against infinite loops from the original request's side. Here is why it matters:

- First attempt: `POST /tasks/` → 401. `_retry` is `undefined` (falsy) → we enter the block, set `_retry = true`, call refresh.
- Refresh succeeds → we retry `POST /tasks/`. This time it returns 201 → success handler runs → done.
- Refresh fails → `Promise.reject(refreshError)` → error bubbles up to the calling utility function.

Without `_retry`, a 401 on the retry would trigger the interceptor a second time, creating a loop.

---

### The Complete Updated utilities.jsx

After adding the interceptor, the rest of the file stays exactly the same. The individual utility functions (`getAllTasks`, `createTask`, etc.) do not need to change — the interceptor operates transparently beneath them.

```javascript
// client/src/utilities.jsx

import axios from "axios";

export const api = axios.create({
    baseURL: 'https://deployment-demo.com/api/v1/',
    withCredentials: true,
})

const refreshAccessToken = () => {
    return axios.post(
        'https://deployment-demo.com/api/v1/users/refresh/',
        {},
        { withCredentials: true }
    )
}

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                await refreshAccessToken();
                return api(originalRequest);
            } catch (refreshError) {
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
)

export const deleteATask = async( id ) => {
    let response = await api.delete(`tasks/${id}/`)
    if(response.status === 200){
        return response.data
    }
    return null
}

export const putTask = async( id, title, dueDate ) => {
    let response = await api.put(`tasks/${id}/`,
        {'title':title, 'due_date': dueDate || null}
    )
    if (response.status === 200){
        return response.data
    }
    console.error(response.data)
    return null
}

export const getAllTasks = async() => {
    try{
        let response = await api.get("tasks/")
        if (response.status === 200){
            return response.data
        }
    } catch(error){
        console.error(error)
        return []
    }
}

export const createTask = async( title, dueDate ) => {
    let response = await api.post('tasks/',
        {'title':title, 'due_date': dueDate || null}
    )
    if (response.status === 201){
        return response.data
    }
    else{
        console.error(response.data)
        return null
    }
}

export const logoutUser = async() => {
    let response = await api.post('users/logout/')
    if (response.status === 200){
        return null
    }
    alert("Something went wrong")
    return null
}

export const userConfirmation = async() => {
    try{
        let response = await api.get('users/')
        if (response.status === 200){
            let user = response.data.email
            return user
        }
        console.error(response.data)
        return null
    } catch(error){
        console.error(error)
        return null
    }
}

export const handleUserAuth = async( data, create ) => {
    try{
        let response = await api.post(`users/${create ? 'create' : 'login'}/`,
            data
        )
        if (response.status === 201 || response.status === 200){
            return response.data.email
        }
        else{
            console.error(response.data)
            return null
        }
    }
    catch(error){
        console.error(error)
        return null
    }
}
```

---

### How the Full Auth Flow Now Works

> With both lessons applied, here is the complete lifecycle of a user session:

| Event | What Happens |
|---|---|
| Sign up / Log in | Server generates JWT pair, sets `access` cookie (15 min) and `refresh` cookie (7 days) |
| Every API request | `api` sends both cookies automatically (`withCredentials: true`) |
| Access token valid | Server authenticates with `CookieAuthentication`, responds normally |
| Access token expired (401) | Interceptor calls `refresh/`, server issues new `access` cookie (and rotates `refresh`) |
| Original request retried | Succeeds with the fresh token — user never notices |
| Refresh token expired (401 on refresh) | Error propagates — user must log in again |
| Log out | Server blacklists refresh token, both cookies deleted from browser |

---

## Conclusion

We added twelve lines to `utilities.jsx` and the entire authentication layer is now self-healing. The interceptor sits silently on every response, only activating when a `401` appears, and the `_retry` flag ensures it never spirals. The individual utility functions — `getAllTasks`, `createTask`, `logoutUser` — required zero changes.

The combination of a short-lived access token, a rotating refresh token, a server-side blacklist, and a client-side interceptor gives us a session model that is both secure and seamless for the user.
