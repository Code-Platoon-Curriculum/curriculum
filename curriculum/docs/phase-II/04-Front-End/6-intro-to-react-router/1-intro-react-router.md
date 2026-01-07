# Intro React Router Dom

## Introduction

As React applications grow, rendering everything inside a single component quickly becomes unmanageable. Real-world applications require multiple “pages” such as home views, detail views, forms, and dashboards. React Router Dom is the library that allows React applications to support **URL-based navigation** while remaining a single-page application (SPA).

In this lesson, we will integrate React Router Dom into the existing PokemonCard project and restructure the application so that different views are rendered based on the browser’s URL. This introduces a new way of thinking about application structure, navigation, and component responsibility.

---

## What is React Router Dom?

React Router Dom is the standard routing library for React applications running in the browser. It allows you to map URL paths to React components and ensures that the UI stays in sync with the browser’s address bar.

Instead of manually showing and hiding components, React Router Dom renders components **based on the current route**, allowing React applications to behave like traditional multi-page websites without full page reloads.

Key ideas introduced by React Router Dom include:

- Declarative routing
- Nested layouts
- URL-driven state
- Client-side navigation

> Think of it as `urlPattern === '/' ? <HomePage/> : <DetailPage/>`

---

## Why and When to Use React Router Dom?

React Router Dom becomes necessary once an application needs more than a single view.

In the context of the PokemonCard project, routing allows us to:

- Separate the Pokemon list view from other application views
- Prepare for features such as a Pokémon detail page
- Make application state shareable via URLs
- Improve code organization by separating “pages” from reusable components

React Router Dom is especially useful when:

- Your app needs multiple screens or views
- You want bookmarkable and shareable URLs
- You want browser back/forward navigation to work correctly
- You want to structure your app around layouts and nested views
- You want to scale your project without turning `App.jsx` into a monolith

---

## Installing React Router Dom

To add routing to the PokemonCard project, install React Router Dom:

```bash
npm install react-router-dom
```

This library integrates directly with React and works seamlessly with Vite.

---

## Organizing the Project for Routing

Before adding routes, it is important to organize the project correctly.

A common convention is to separate **pages** from **reusable components**.

Inside `src`, create a `pages` directory:

```bash
mkdir src/pages
```

* Components represent reusable UI building blocks (e.g., PokemonCard, PokemonForm)
* Pages represent full-screen views that are tied to routes (e.g., HomePage)

This separation helps enforce clarity as the application grows.

---

## Creating Pages for the Pokemon Application

Create a `HomePage.jsx` file inside `src/pages`. This file is pretty much going to hold the current state of `App.jsx` this way we can isolate the Home behavior and separate it from other pages.

```jsx
import { useState, useEffect } from "react";
import axios from "axios";
import PokemonCard from "../components/PokemonCard";
import PokemonForm from "../components/PokemonForm";

const HomePage = () => {
  const [pokemonsData, setPokemonsData] = useState([]);

  const addCard = async (name, event = null) => {
    event && event.preventDefault();
    try {
      let searchUrl = `https://pokeapi.co/api/v2/pokemon/${name}`;
      let response = await axios.get(searchUrl);
      setPokemonsData([...pokemonsData, response.data]);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    addCard("Pikachu");
  }, []);

  return (
    <>
      <div id="cardHolder">
        {pokemonsData.map((data) => (
          <PokemonCard key={data.id} data={data} />
        ))}
      </div>
      <PokemonForm addCard={addCard} />
    </>
  );
}

export default HomePage;
```

The HomePage component represents a **route-level view**, not a generic component.

---

## Creating the Browser Router

Create a new file at `src/router.jsx`.

```jsx
import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import HomePage from "./pages/HomePage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
    ],
  },
]);

export default router;
```

Key concepts introduced here:

* The root route (`/`) renders `App`
* Child routes render inside `App` using `<Outlet />`
* The index route represents the default child route

---

## Connecting the Router to the Application

By default, Vite renders `App.jsx` directly. To enable routing, we must replace that behavior.

Update `src/main.jsx`:

```jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router-dom";
import router from "./router";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <RouterProvider router={router} />
);
```

At this point, React Router Dom controls which components are rendered based on the URL.

---

## Updating App.jsx to Act as a Layout

With routing in place, `App.jsx` no longer renders page content directly. Instead, it acts as a **layout component**.

```jsx
import { Outlet } from "react-router-dom";
import "./App.css";

function App() {
  return (
    <>
      <Outlet />
    </>
  );
}

export default App;
```

This pattern allows for a clear and clean separation of routing and UI logic

---

## Understanding the Mental Model

With React Router Dom:

* URLs determine which components render
* Pages represent routes
* Components remain reusable and route-agnostic
* `App.jsx` becomes a layout instead of a page
* Navigation does not reload the browser

This is a fundamental shift from manually showing and hiding components to **URL-driven rendering**.

---

## Conclusion

React Router Dom introduces a scalable architecture for React applications by allowing the UI to respond directly to the browser’s URL. By integrating routing into the PokemonCard project, we moved from a single-view application to a multi-view SPA with clear separation between pages, layouts, and reusable components.

Understanding routing early enables students to reason about application structure, navigation, and long-term scalability. With routing in place, the PokemonCard application is now prepared for additional features such as detail pages, navigation bars, and nested views.
