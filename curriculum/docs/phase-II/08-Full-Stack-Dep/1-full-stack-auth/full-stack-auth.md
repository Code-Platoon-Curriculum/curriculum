# Connecting Axios and Views

## Introduction

Welcome to the lecture on connecting Axios and views in a full-stack development environment! By the end of this lecture, you will have a full-stack application running with a React + Vite frontend and a Django backend with a PostgreSQL database.

In this lecture we will be utilizing the [Task Manager Repo](https://github.com/Code-Platoon-Curriculum/deployment-app.git) please clone if you would like to follow along.

## Familiarizing ourselves with the project

### Front-End

We are not making this project from scratch but lets take some time to look at our project and understand everything going on.

Currently our React + Vite framework is running with the following dependencies:

- Axios
- React BootStrap
- React Router DOM

Our React application has three pages that render an `h1` element with the text to represent each page. Each one of these Pages is referenced to within the router and have a path built in to display each one.

- HomePage
- SignUp
- LogIn

Finally, we have App.jsx that calls a NavBar component from React BootStrap and an Outlet which will connect the children pages of our Router to our App.

### Back-End

Our Django API holds the following models with full CRUD capabilities:

- App_user: The default authentication user model for Token based Authentication with DRF
- List: Many to One relationship to a user
- Task: Many to One relationship to a List
- Subtasks: Many to One relationship with a Task

Additionally, our Django API also has the following endpoints:

- `/api/test/` GET
- `/api/users/` GET || PUT
- `/api/users/signup/` POST
- `/api/users/login/` POST
- `/api/users/logout/` POST
- `/api/lists/` POST || GET
- `/api/lists/<int:id>/` GET | PUT | DELETE
- `/api/lists/<int:id>/tasks/` GET || POST
- `/api/lists/<int:id>/tasks/<int:task_id>/` GET | PUT | DELETE
- `/api/lists/<int:id>/tasks/<int:task_id>/subtasks/` GET || POST
- `/api/lists/<int:id>/tasks/<int:task_id>/subtasks/<int:subtask_id>/` GET | PUT | DELETE

## Connecting API Views and Axios

Currently our React application is not sending any requests to our Django API, it's a purely Front-End application. Lets get these two to communicate to eachother by sending a get request to the `api/test/` endpoint.

```jsx
// App.jsx
  const test_connection = async() ={
    let response = await axios.get("http://127.0.0.1:8000/api/test/")
    console.log(response)
  }

  useEffect(()=>{
    test_connection()
  },[])
```

If we take a look at our terminal hosting our Django server, we can see the `GET` request was both sent, and processed. Yet, if we take a look at the console in our browser hosting our React Project we receive the following error:

```bash
Access to XMLHttpRequest at 'http://127.0.0.1:8000/api/test/' from origin 'http://localhost:5173' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

Well we are trying to contact a separate server so it only makes sense that Django's safety features would block this communication unless I explicitly tell it to allow this server to communicate with us. So let's take a step back and reassess our Django Project to allow ALL origins to ping our API.

Where is this coming from and why is this happening if Django is stating it returned it 200 response?

### Handling CORS in Django

- What is CORS?

CORS stands for Cross-Origin Resource Sharing. It is a security feature implemented by web browsers to prevent web pages from making requests to a different domain than the one that served the original web page. This security measure is in place to protect users from potential malicious activities that could occur if a web page gains unauthorized access to resources on other domains.

- When should I use CORS?

When developing web applications using Django, you might encounter CORS-related issues if you want to make AJAX requests from your frontend JavaScript code to a Django backend running on a different domain. By default, web browsers block such cross-origin requests.

To enable CORS in a Django application, you need to add the appropriate headers to the HTTP response. Django does not have CORS support built into its core, but you can handle CORS using middleware or external packages like `django-cors-headers`.

- How do I utilize CORS

The `django-cors-headers` package is a popular choice for handling CORS in Django applications. Once installed and configured, it adds the necessary CORS-related headers to your responses, allowing your frontend code to make cross-origin requests to the Django backend securely.

Here's a quick overview of the steps to enable CORS using `django-cors-headers`:

1. Install the package:

```bash
pip install django-cors-headers
```

2. Add `'corsheaders'` to your `INSTALLED_APPS` in the Django settings.py file:

```python
#settings.py
INSTALLED_APPS = [
    # ...
    'corsheaders',
    # ...
]
```

3. Add the `CorsMiddleware` to the middleware list in settings.py. Ensure it comes before the `CommonMiddleware`:

```python
#settings.py
MIDDLEWARE = [
    # ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ...
]
```

4. Configure the CORS settings according to your requirements. For example, you can specify which origins are allowed, which headers are allowed in requests, and other options:

```python
CORS_ALLOWED_ORIGINS = [
    "https://example.com", #domain
    "https://sub.example.com", #subdomain
    "http://localhost:5173", #development server
]

# or to allow all origins
CORS_ALLOW_ALL_ORIGINS = True
```

You can find more configuration options in the documentation of [django-cors-headers](https://www.stackhawk.com/blog/django-cors-guide/).

With CORS properly configured in your Django application, your frontend will be able to make cross-origin requests to the backend, provided the allowed origins match those defined in the CORS settings. This helps you maintain security while enabling communication between different parts of your web application.

Now lets run the server and send our request to `api/test/` one more time and see our API Response display on the browsers console.

You did it! Your React Front-End is now speaking to your Django Back-End..... we aren't done yet though. Lets move into handling authentication within the Full-Stack environment.

## Handling Authentication

### Creating an Axios instance

We know that we are going to be sending requests to our Django Back-End frequently so instead of typing our our Back-End url pattern over and over again we should create an `axios instance` that will have our Back-End frameworks url pattern already built into it.

```jsx
// utilities.jsx
import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});
```

Now we can import `api` into other JSX files within our React project to ping our Django Back-End as such:

```jsx
const test_connection = async () => {
  let response = await api.get("test/");
  console.log(response.data);
};

useEffect(() => {
  test_connection();
}, []);
```

You'll see our React project still pings the correct endpoint and receives the appropriate Response.

### Obtaining User Tokens Upon Authentication

Now that we have an `axios instance` to avoid repeated code we can start building our Authentication form within our React Front-End.
Let's grab a form template from React-BootStrap and place it within our `SignUp.jsx` file.

```jsx
//SignUp.jsx
import { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

const SignUp = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <>
      <h1>SignUp</h1>
      <Form>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control
            onChange={(e) => setEmail(e.target.value)}
            value={email}
            type="email"
            placeholder="Enter email"
          />
          <Form.Text className="text-muted">
            We'll never share your email with anyone else.
          </Form.Text>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            onChange={(e) => setPassword(e.target.value)}
            value={password}
            type="password"
            placeholder="Password"
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </>
  );
};

export default SignUp;
```

This gives the user a Form to be able to sign up, but we currently don't have a function that will make an API call to authenticate our user and grab our users APIToken.

```jsx
// utilities.jsx
export const userRegistration = async (email, password) => {
  let response = await api.post("users/signup/", {
    email: email,
    password: password,
  });
  if (response.status === 201) {
    let { user, token } = response.data;
    // Store the token securely (e.g., in localStorage or HttpOnly cookies)
    localStorage.setItem("token", token);
    api.defaults.headers.common["Authorization"] = `Token ${token}`;
    return user;
  }
  alert(response.data);
  return null;
};
```

### Handling Tokens in Development

Our token needs to be accessible to our application regardless whether our User refreshes their application or not. So we know the token of a user can't exist within the React DOM since it's re-rendered everytime the browser is refreshed... instead we will ask the browser to hold on to our users token through local storage.

Additionally we are adding this token to our `axios instance` Authorization header so any following request made by the user will contain its token within it.

#### Local Storage

> Browser localStorage is a crucial web development tool that enables developers to store key-value pairs locally within a web browser. This feature allows web applications to persistently store data on a user's device, even after the user navigates away from the webpage or closes the browser. Understanding the key factors related to localStorage is essential for developers to make the most of this powerful and versatile tool.

Here are a couple of key factors to keep in mind when utilizing `localStorage`:

1. **Data Persistence:** `localStorage` enables data to persist across sessions, even after the browser is closed and reopened.

2. **Key-Value Pairs:** Data is stored in `localStorage` as key-value pairs, with both the key and value represented as strings.

3. **Storage Limit:** Each browser has a storage limit for `localStorage`, usually around 5 to 10 MB per domain.

4. **Single-Origin Policy:** `localStorage` follows the same-origin policy, restricting access to data from other domains.

5. **Data Access:** Accessing data from `localStorage` is done using the `localStorage` object in JavaScript.

6. **No Expiry:** Unlike cookies, `localStorage` data does not have an expiration date and remains stored indefinitely.

7. **Synchronous API:** The `localStorage` API is synchronous, potentially affecting page performance for large or multiple operations.

8. **Security Considerations:** Avoid storing sensitive data in `localStorage` due to potential vulnerabilities like cross-site scripting (XSS) attacks.

9. **Event Mechanism:** `localStorage` lacks a built-in event mechanism, requiring custom event handling or third-party libraries for data change notifications.

10. **Fallback Mechanisms:** Plan for fallback options in case `localStorage` is not supported by some browsers.

Remember to use `localStorage` responsibly, considering security and storage limitations, to enhance the user experience and build efficient web applications.

### Implementing the registration method

First let's make sure we have a method for confirming a user changed within App.jsx and pass down the `setUser` function to our pages:

```jsx
// App.jsx
function App() {
  const [user, setUser] = useState(null);

  const test_connection = async () => {
    let response = await api.get("test/");
    console.log(response.data);
  };

  useEffect(() => {
    test_connection();
  }, []);

  useEffect(() => {
    console.log(user);
  }, [user]);

  return (
    <>
      <NavBar />
      <Outlet context={{ user, setUser }} />
    </>
  );
}

export default App;
```

Now lets add our `userRegistration` method as the `onSubmit` method of our form while preventing the default behavior.

```jsx
// SignUp.jsx
<Form
  onSubmit={async(e) => [
    e.preventDefault(),
    setUser(await userRegistration(email, password)),
  ]}
>
```

This will do the following upon submit:

1. Set the user as the users `display_name` which is currently defaulted to unknown or return null if a new user failed to be created.
2. Set the user token within `dev tools > application > local storage`
3. Set the user token within `api Authorization Headers`

### Implementing the LogIn method

Now that we have a users ability to Register to our application lets create a method that will give them the ability to log in.

```jsx
// utilities.jsx
export const userLogIn = async (email, password) => {
  let response = await api.post("users/login/", {
    email: email,
    password: password,
  });
  if (response.status === 200) {
    let { user, token } = response.data;
    localStorage.setItem("token", token);
    api.defaults.headers.common["Authorization"] = `Token ${token}`;
    return user;
  }
  alert(response.data);
  return null;
};
```

Now lets create a form that will call this method uppon submit:

```jsx
// LogIn.jsx
import { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useOutletContext } from "react-router-dom";
import { userLogIn } from "../utilities";

const LogIn = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { setUser } = useOutletContext();

  return (
    <>
      <h1>Log In</h1>
      <Form
        onSubmit={async (e) => [
          e.preventDefault(),
          setUser(await userLogIn(email, password)),
        ]}
      >
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control
            onChange={(e) => setEmail(e.target.value)}
            value={email}
            type="email"
            placeholder="Enter email"
          />
          <Form.Text className="text-muted">
            We'll never share your email with anyone else.
          </Form.Text>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            onChange={(e) => setPassword(e.target.value)}
            value={password}
            type="password"
            placeholder="Password"
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </>
  );
};

export default LogIn;
```

You'll notice there's quite a bit of repeated code in between these methods and components, so you may want to look into how to refactor this code and place all your logic under one method and one component.

### Implementing Logging Out

Now that our user is able to both register and/or log in to our application, lets implement a method that will allow them to log out and remove their token from the application and set our user back to `null`.

```jsx
// utilities.jsx
export const userLogOut = async () => {
  let response = await api.post("users/logout/");
  if (response.status === 204) {
    localStorage.removeItem("token");
    delete api.defaults.headers.common["Authorization"];
    return null;
  }
  alert("Something went wrong and logout failed");
};
```

Now lets implement this method within our NavBars button for logging out. Don't forget to pass down `setUser` as a prop to the NavBar:

```jsx
//NavBar.jsx
<Button
  variant="outline-danger"
  onClick={async () => setUser(await userLogOut())}
>
```

## Application User Flow

Now our users have the ability to register, log in, and log out of our application, but now we need to create a pleasent interaction with our Front-End application uppon log in. Lets start by solving the problem of refreshing our Front-End application.

### Handling Refresh

We need to create a method that checks the following as before `App.jsx` even renders on our Front-End application.

- Check if there's a token within local storage
- If there is a token:
  - set it as the Authorization header of our `axios instance`
  - send a request to confirm a valid token and return the user name
- or return `null` if the token doesn't exist or is not valid.

```jsx
// utilities.jsx
export const userConfirmation = async () => {
  let token = localStorage.getItem("token");
  if (token) {
    api.defaults.headers.common["Authorization"] = `Token ${token}`;
    let response = await api.get("users/");
    if (response.status === 200) {
      return response.data.user;
    }
  }
  return null;
};
```

This is great!

but... how do I implement this prior to `App.jsx` being able to render. Well I would need to tell my browser that this `App.jsx` element has a `loader` function that it needs in order to render properly. Let's take a look at how that works:

```jsx
// router.jsx
{
  path:"/",
  element: <App/>,
  loader: userConfirmation,
  children: ["..."],
}
```

Now the router know not to render this element until the behavior of our method is completed. But how do we access this data from within our App.jsx? Let's call this data and use it to initialize the state of the `user` and display it within our `Home.jsx` page.

```jsx
// App.jsx
const [user, setUser] = useState(useLoaderData()) //<== import from react-router-dom

// HomePage.jsx
<h1>Welcome{user && ` ${user}`}</h1>
```

## Handling Null User Pages

This takes care of being able to refresh pages but now we want to take away links to pages that our user can't go into if they're logged in and vise versa. This should be a simple ternirary statement within the NavBar so let's implement it.

```jsx
//NavBar.jsx
{
  !user ? (
    <>
      <Nav.Link as={Link} to="/signup/">
        Sign Up
      </Nav.Link>
      <Nav.Link as={Link} to="/login/">
        Log In
      </Nav.Link>
    </>
  ) : (
    <Button
      variant="outline-danger"
      onClick={async () => setUser(await userLogOut())}
    >
      Log Out
    </Button>
  );
}
```

That takes care of display.... but what if a user manually types in the url pattern into our application?

We can create a `useEffect` within our App.jsx that will evaluate if there's a current user present and that they are within allowed urlpatterns using `useNavigate and useLocation` from react-router-dom.

```jsx
// App.jsx
useEffect(() => {
  let nullUserUrls = ["/login/", "/signup/"];
  let isAllowed = nullUserUrls.includes(location.pathname);
  if (user && isAllowed) {
    navigate("/");
  } else if (!user && !isAllowed) {
    navigate("/");
  }
}, [location.pathname, user]);
```

And that's it, we have now connected our React Front-End to our Django Back-End RESTful API.

Congratulations, you are now a full-stack developer!!!

## Conclusion

Congratulations on completing this lecture! You've learned how to connect Axios with views in a full-stack development environment, enabling seamless communication between a React frontend and Django backend. By implementing user authentication, you've enhanced the security and functionality of your application. Keep exploring and building amazing projects!
