# React Router DOM Pages

## Introduction

In the previous lesson, we introduced React Router Dom and restructured the PokemonCard application so that routing determines which views are rendered. At this point, the application has a single page — the Home page — but the routing infrastructure is already in place.

In this lesson, we will expand the application by adding additional pages and learning how navigation works inside a React Router Dom–powered application. The goal is to understand how URLs, pages, and navigation links work together to create multi-view experiences without full page reloads.

---

## Thinking in Pages, Not Components

Before adding new routes, it is important to reinforce the distinction between **pages** and **components**.

Pages are route-level views. They represent full sections of the application and are directly tied to URLs. Components, on the other hand, are reusable building blocks that can appear inside many pages and are not tied to navigation.

In the PokemonCard project:

- `HomePage` is a page because it represents a full screen of the application
- `PokemonCard` and `PokemonForm` are components because they can be reused and are not route-aware

This distinction becomes more important as the application grows.

---

## Adding a New Page

To demonstrate how routing scales, we will add a new page to the application. This page will live alongside `HomePage` inside the `pages` directory.

Create a new file at `src/pages/AboutPage.jsx`.

```jsx
function AboutPage() {
  return (
    <div>
      <h1>About This App</h1>
      <p>
        This application allows users to search for Pokémon and display them as
        cards using data from the PokéAPI.
      </p>
    </div>
  );
}

export default AboutPage;
```

This page does not need any state or logic. Its purpose is to demonstrate how React Router Dom swaps entire views based on the URL.

---

## Registering the New Page with the Router

Now that the page exists, React Router Dom needs to know when it should be rendered.

Open `src/router.jsx` and add the new route as a child of the root route.

```jsx
import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import HomePage from "./pages/HomePage";
import AboutPage from "./pages/AboutPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: "about",
        element: <AboutPage />,
      },
    ],
  },
]);

export default router;
```

At this point:

* Visiting `/` renders `HomePage`
* Visiting `/about` renders `AboutPage`
* Both pages render inside the `App` layout via `<Outlet />`

---

## Navigating Between Pages

Routing alone does not create navigation. To move between pages without refreshing the browser, React Router Dom provides the `Link` component.

Unlike traditional anchor tags, `Link` updates the URL and renders the new page **without reloading the application**.

Update `App.jsx` to include navigation links.

```jsx
import { Outlet, Link } from "react-router-dom";
import "./App.css";

function App() {
  return (
    <>
      <nav>
        <Link to="/">Home</Link> | <Link to="/about">About</Link>
      </nav>
      <Outlet />
    </>
  );
}

export default App;
```

Clicking these links updates the URL and swaps the rendered page instantly.

This is a core characteristic of single-page applications.

---

## Understanding Navigation Mentally

At runtime, React Router Dom evaluates the current URL and decides which page component to render inside the layout.

Conceptually, this behaves like:

```
URL === "/"       → HomePage
URL === "/about"  → AboutPage
```

The browser address bar becomes a **source of truth** for which page is visible.

---

## Adding a Not Found (404) Page

A well-structured application should gracefully handle invalid URLs. React Router Dom supports this by allowing you to define an error page.

Create a new file at `src/pages/NotFound.jsx`.

```jsx
function NotFound() {
  return (
    <div>
      <h1>404 - Page Not Found</h1>
      <p>The page you are looking for does not exist.</p>
    </div>
  );
}

export default NotFound;
```

Now register it in the router configuration.

```jsx
import NotFound from "./pages/NotFound";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: "about",
        element: <AboutPage />,
      },
      {
        path:"*",
        element: <NotFound />
      }
    ],
  },
]);
```

If a user navigates to a URL that does not match any defined route, React Router Dom will render the `NotFound` page.

## Adding an ErrorPage

Just like we are now handling invalid url patterns we must also effectively handle *errors* that may occur within our application logic. There is a plethora of things that can cause an issue but the following are some common concerns: A component throws an error, a loader/action throws, or an unexpected runtime failure occurs.

We can address this with the following:

```jsx
// ErrorPage.jsx
const ErrorPage = () => {
  return (
    <>
      <h1>Oops... Something went wrong</h1>
    </>
  )
}

export default ErrorPage

// router.jsx
const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: "about",
        element: <AboutPage />,
      },
      {
        path:"*",
        element: <NotFound />
      }
    ],
  },
]);
```

---

## Understanding Not Found vs Error Boundaries

| Concern      | Mechanism      | Why                   |
| ------------ | -------------- | --------------------- |
| Invalid URL  | `path: "*"`    | Routing problem       |
| App crash    | `errorElement` | Runtime failure       |
| Missing data | `errorElement` | Exception handling    |
| Typo in URL  | `path: "*"`    | User navigation issue |

> A 404 page means the app is working - the route just doesn't exist.
> An error page means something broke while trying to render

---

## Why This Structure Matters

By separating pages, components, and routing logic:

* The application becomes easier to reason about
* Each page has a clear responsibility
* Navigation logic stays centralized
* UI components remain reusable and isolated
* Scaling the app does not require rewriting existing views

This architecture is foundational for real-world React applications.

---

## Conclusion

In this lesson, you expanded the PokemonCard application by introducing additional pages and enabling navigation between them. You learned how pages differ from components, how routes map URLs to views, and how React Router Dom enables seamless navigation without reloading the browser.

With multiple pages in place, the application is now structured for growth and ready for more advanced routing patterns such as dynamic routes, nested layouts, and route-based data loading.
