# React.js and Requests

## What are we trying to accomplish?

In this lesson, the goal is to help students understand how modern front-end applications communicate with external systems and why asynchronous behavior is required for that communication to function correctly. Rather than treating requests as magical or abstract, students are guided through the full lifecycle of a request, from initiation in the browser, to processing on an API server, and finally back to UI updates in the client.

This lesson intentionally reinforces fundamentals by avoiding React state and hooks. By relying on Axios, promises, async/await, and direct DOM manipulation, students build a concrete mental model for how data flows into an application and why the browser must never be blocked while waiting for a response. By the end of the lesson, students should feel confident reasoning about asynchronous code, handling request failures, and transforming remote data into visible UI changes.

---

## Lectures & Assignments

### Lectures

- [React and Vite](./1-react-and-vite.md)
- [Asynchronous Requests](./2-async-requests.md)

### [Assignments](./assignments.md)

---

## Enabling Learning Objectives (ELO's)

- Understand what an HTTP request represents and why front-end applications rely on servers for data  
- Explain asynchronous execution in a single-threaded JavaScript environment  
- Describe why synchronous requests would block the user interface  
- Understand what promises are, why they exist, and how they represent future values  
- Explain what an API server is doing while the front end waits for a response  
- Recognize that delays, failures, and errors are normal parts of network communication  

---

## Tangible Learning Objectives (TLO's)

- Install and use Axios to perform HTTP requests in a front-end application  
- Consume a third-party API and inspect the structure of its responses  
- Extract relevant data from API responses for use in the UI  
- Handle asynchronous logic using both `.then().catch().finally()` and `async/await`  
- Dynamically create and insert DOM elements based on received data  
- Properly handle request errors and provide feedback in the UI  
- Reason about when and how UI updates occur in relation to asynchronous operations  
