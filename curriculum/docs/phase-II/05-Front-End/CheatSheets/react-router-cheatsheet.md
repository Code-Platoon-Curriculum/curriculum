# React Router Cheatsheet

## Installation

```bash
npm install react-router-dom
```

## Basic Setup

### 1. Create Router Configuration

```jsx
// router.jsx
import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import HomePage from "./pages/HomePage";
import AboutPage from "./pages/AboutPage";
import ContactPage from "./pages/ContactPage";
import NotFoundPage from "./pages/NotFoundPage";

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
        path: "contact",
        element: <ContactPage />,
      },
    ],
    errorElement: <NotFoundPage />,
  },
]);

export default router;
```

### 2. Connect Router to Main App

```jsx
// main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router-dom";
import router from "./router";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <RouterProvider router={router} />
);
```

### 3. App Component with Outlet

```jsx
// App.jsx
import { Outlet, Link } from "react-router-dom";

function App() {
  return (
    <>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/contact">Contact</Link>
      </nav>
      <Outlet />
    </>
  );
}

export default App;
```

## Quick Reference

### Hooks

| Hook | Purpose | Import | Example Usage |
|------|---------|--------|---------------|
| `useNavigate` | Programmatically navigate to routes | `import { useNavigate } from "react-router-dom"` | `const navigate = useNavigate(); navigate("/about");` |
| `useParams` | Extract URL parameters | `import { useParams } from "react-router-dom"` | `const { id } = useParams();` |
| `useOutletContext` | Access context from parent route | `import { useOutletContext } from "react-router-dom"` | `const { favorites, setFavorites } = useOutletContext();` |
| `useLocation` | Get current location object | `import { useLocation } from "react-router-dom"` | `const location = useLocation(); console.log(location.pathname);` |
| `useSearchParams` | Read/write URL search parameters | `import { useSearchParams } from "react-router-dom"` | `const [searchParams, setSearchParams] = useSearchParams();` |

### Components

| Component | Purpose | Import | Example Usage |
|-----------|---------|--------|---------------|
| `<Link>` | Create navigation links | `import { Link } from "react-router-dom"` | `<Link to="/about">About</Link>` |
| `<NavLink>` | Link with active state styling | `import { NavLink } from "react-router-dom"` | `<NavLink to="/about" className={({isActive}) => isActive ? "active" : ""}>About</NavLink>` |
| `<Outlet>` | Render child route components | `import { Outlet } from "react-router-dom"` | `<Outlet />` or `<Outlet context={{data}} />` |
| `<Navigate>` | Programmatic redirect component | `import { Navigate } from "react-router-dom"` | `<Navigate to="/login" replace />` |
| `<RouterProvider>` | Provide router to app | `import { RouterProvider } from "react-router-dom"` | `<RouterProvider router={router} />` |

### Router Configuration

| Property | Purpose | Example | Description |
|----------|---------|---------|-------------|
| `path` | Define route URL pattern | `"/user/:id"` | Static or dynamic path with parameters |
| `element` | Component to render | `<UserPage />` | React component for this route |
| `index` | Default child route | `index: true` | Renders when parent path matches exactly |
| `children` | Nested routes array | `children: [...]` | Array of child route objects |
| `errorElement` | Error boundary component | `<NotFoundPage />` | Renders when route throws error |
| `loader` | Data loading function | `loader: async () => {...}` | Function to load data before rendering |

### useNavigate Options

| Method | Purpose | Example | Description |
|--------|---------|---------|-------------|
| `navigate(path)` | Navigate to path | `navigate("/about")` | Basic navigation |
| `navigate(-1)` | Go back in history | `navigate(-1)` | Browser back button |
| `navigate(1)` | Go forward in history | `navigate(1)` | Browser forward button |
| `navigate(path, {replace: true})` | Replace current entry | `navigate("/home", {replace: true})` | Don't add to history |
| `navigate(path, {state: data})` | Pass state data | `navigate("/user", {state: {userId: 123}})` | Pass data to destination |

### Route Patterns

| Pattern | Matches | Example | Description |
|---------|---------|---------|-------------|
| `/` | Root path only | `/` | Home page |
| `/about` | Static path | `/about` | Static route |
| `/user/:id` | Dynamic segment | `/user/123` | Parameter route |
| `/user/:id?` | Optional parameter | `/user` or `/user/123` | Optional param |
| `/files/*` | Wildcard/splat | `/files/docs/readme.txt` | Catch remaining path |
| `*` | Catch-all | Any unmatched route | 404 fallback |

### URL Structure Examples

Common patterns from curriculum assignments:

```jsx
// Character list and details
"/characters"              // List all characters
"/character/:id"           // Character detail page
"/character/:id/episodes"  // Character's episodes

// User profiles
"/user/:userId"            // User profile
"/user/:userId/settings"   // User settings
"/user/:userId/favorites"  // User's favorites

// Admin routes
"/admin/users"             // Admin user list
"/admin/users/:id"         // Admin edit user
"/admin/users/:id/delete"  // Admin delete confirmation
```

## Common Patterns

### Conditional Redirect

```jsx
// LoginPage.jsx
import { Navigate } from "react-router-dom";

const LoginPage = () => {
  const user = getCurrentUser();
  
  // Redirect if already logged in
  if (user) {
    return <Navigate to="/dashboard" replace />;
  }
  
  return (
    <div>
      <h1>Login</h1>
      <LoginForm />
    </div>
  );
};
```

### Layout Route

```jsx
// Layout.jsx
import { Outlet, Link } from "react-router-dom";

const Layout = () => {
  return (
    <div>
      <header>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/about">About</Link>
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
      <footer>My App</footer>
    </div>
  );
};

// In router.jsx
{
  path: "/",
  element: <Layout />,
  children: [
    { index: true, element: <HomePage /> },
    { path: "about", element: <AboutPage /> },
  ],
}
```

### Index Route

```jsx
// In router.jsx - Default child route
{
  path: "/dashboard",
  element: <DashboardLayout />,
  children: [
    {
      index: true,  // Renders at /dashboard
      element: <DashboardHome />
    },
    {
      path: "settings",  // Renders at /dashboard/settings
      element: <SettingsPage />
    },
  ],
}
```

### Error Boundary

```jsx
// ErrorPage.jsx
import { useRouteError, Link } from "react-router-dom";

const ErrorPage = () => {
  const error = useRouteError();
  
  return (
    <div>
      <h1>Oops! Something went wrong</h1>
      <p>{error.statusText || error.message}</p>
      <Link to="/">Go back home</Link>
    </div>
  );
};

// In router.jsx
{
  path: "/",
  element: <App />,
  errorElement: <ErrorPage />,
  children: [...],
}
```

### Nested Routes

```jsx
// In router.jsx
{
  path: "/admin",
  element: <AdminLayout />,
  children: [
    {
      path: "users",
      element: <UsersLayout />,
      children: [
        { index: true, element: <UsersList /> },
        { path: ":id", element: <UserDetail /> },
        { path: ":id/edit", element: <UserEdit /> },
      ],
    },
    {
      path: "settings",
      element: <AdminSettings />,
    },
  ],
}

// Results in routes:
// /admin/users - UsersList
// /admin/users/123 - UserDetail
// /admin/users/123/edit - UserEdit
// /admin/settings - AdminSettings
```