# Authentication

## Introduction

Welcome to the lecture on connecting Axios and views in a full-stack development environment! By the end of this lecture, you will have a full-stack application running with a React + Vite frontend and a Django backend with a PostgreSQL database.

## Project Overview

### Front-End

We are not making this project from scratch but lets take some time to look at our project and understand everything going on.

Currently our React + Vite project is running with the following dependencies:

- Axios
- React BootStrap
- BootStrap
- React Router DOM

Our React application has two pages with all of the Front-End components, utilities, states that are needed to mimick the overall application functionality:

- AuthPage
- HomePage

### Back-End

Our Django API holds the following models with full CRUD capabilities:

- AppUser: The default authentication user model for Token based Authentication with DRF
- Task: Many to One relationship to an AppUser along with an attribute of title

Additionally, our Django API also has the following endpoints:

- `/api/v1/test/` GET
- `/api/v1/users/` GET 
- `/api/v1/users/create/` POST
- `/api/v1/users/login/` POST
- `/api/v1/users/logout/` POST
- `/api/v1/tasks/` POST || GET
- `/api/v1/tasks/<int:task_id>/` GET | PUT | DELETE

## Connecting API Views and Axios

Currently our React application is not sending any requests to our Django API, it's a purely Front-End application. Lets get these two to communicate with each-other by sending a get request to the `api/v1/test/` endpoint.

```jsx
// App.jsx
  const test_connection = async() =>{
    let response = await axios.get("/api/v1/test/")
    console.log(response)
  }

  useEffect(()=>{
      test_connection()
  },[])
```

> Even though Django runs on port 8000 inside Docker, the frontend never talks to Django directly. All browser requests go to Nginx on port 80, and Nginx proxies /api/ traffic to the backend container. This keeps the frontend decoupled from backend infrastructure details and mirrors how production systems are deployed.

If we take a look at our terminal hosting our Django server, we can see the `GET` request was both sent, and processed. 

> This process is successful because we are all working within one Docker Network, if this request was coming from an outside source you would have to manage this connection by adding *CORS* onto your Django Application.

## Handling Authentication

### Creating an Axios instance

We know that we are going to be sending requests to our Django Back-End frequently so instead of typing our our Back-End url pattern over and over again we should create an `axios instance` that will have our Back-End frameworks url pattern already built into it.

```jsx
// utilities.jsx
import axios from "axios";

export const api = axios.create({
  baseURL: "/api/v1/", 
});
```


Now we can import `api` into other JSX files within our React project to ping our Django Back-End as such:

```jsx
  const test_connection = async() =>{
    let response = await api.get("test/")
    console.log(response)
  }

  useEffect(()=>{
    test_connection()
  },[])
```

You'll see our React project still pings the correct endpoint and receives the appropriate Response.

### Implementing the Registration and Log In Methods

#### Obtaining User Tokens Upon Authentication

Now that we have an `axios instance` to avoid repeated code we can start building our Authentication form utilities within our React Front-End. Within *utilities.jsx* go ahead and add the following:


```jsx
// utilities.jsx
export const userAuth = async (email, password, create) => {
  let response = await api.post(create ? "users/create/" : "users/login/", {
    email: email,
    password: password,
  });
  if (response.status === 201 || response.status === 200) {
    let { email, token } = response.data;
    // Store the token securely (e.g., in localStorage or HttpOnly cookies)
    localStorage.setItem("token", token);
    api.defaults.headers.common["Authorization"] = `Token ${token}`;
    return email;
  }
  alert(response.data);
  return null;
};
```

#### Handling Tokens in Development

Our token needs to be accessible to our application regardless whether our User refreshes their application or not. So we know the token of a user can't exist within the React DOM since it's re-rendered everytime the browser is refreshed... instead we will ask the browser to hold on to our users token through local storage.

Additionally we are adding this token to our `axios instance` Authorization header so any following requests made by the browser will contain the users token within it.

##### Local Storage

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

#### Updating `handleSubmit` Method

First let's make sure we have a method for confirming a user changed within App.jsx and pass down the `setUser` function to our pages:


Now lets add our `userAuth` method as part of the `handleSubmit` method of our form while preventing the default behavior.

```jsx
    const handleSubmit = async(e) => {
        e.preventDefault()
        let userDict = {
            email:email,
            password: password
        }
        let method = create ? 'CREATE ACCT' : 'LOGIN ACCT'
        console.log(userDict, method)
        let user = await userAuth(email, password, create)
        console.log(user)
        setUser(user)
        setCreate(true)
        setEmail('')
        setPassword('')
        navigate('/home')
    }
```

This will do the following upon submit:

1. Set the user as the users `email` 
2. Set the user token within `dev tools > application > local storage`
3. Set the user token within `api Authorization Headers`


### Implementing Confirmation Method

#### Confirming with Token from LocalStorage

We need to create a method that checks the following before `App.jsx` even renders on our Front-End application. This way if there is a user that has already logged in and refreshes the page, our app will confirm the user and set the user back to an appropriate value.

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
      return response.data.email;
    }
    return null
  }
  return null;
};
```

This is great!

#### Updating `router.jsx

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

### Implementing Logging Out

#### Deleting Tokens from all sources

Now that our user is able to both register and/or log in to our application, lets implement a method that will allow them to log out and remove their token from the application and set our user back to `null`.

```jsx
// utilities.jsx
export const userLogOut = async () => {
  let response = await api.post("users/logout/");
  if (response.status === 200) {
    localStorage.removeItem("token");
    delete api.defaults.headers.common["Authorization"];
    return null;
  }
  alert("Something went wrong and logout failed");
  return null
};
```

#### Updating LogOut Button

Now lets implement this method within our Log Out button for logging out.:

```jsx
<h1>Welcome {user && user}: Here are your Tasks <button onClick={async()=>setUser(await userLogOut())}>Log Out</button></h1>
```

## Application User Flow

Now our users have the ability to register, log in, and log out of our application, but we need to create a pleasant interaction with our Front-End application upon log in. Lets start by solving the problem of refreshing our Front-End application.


### Handling Null User Pages

We can create a `useEffect` within our App.jsx that will evaluate if there's a current user present and that they are within allowed urlpatterns using `useNavigate and useLocation` from react-router-dom.

```jsx
// App.jsx
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    let nullUserUrls = ["/"];
    let isAllowed = nullUserUrls.includes(location.pathname);
    if (user && isAllowed) {
      navigate("/home");
    } else if (!user && !isAllowed) {
      navigate("/");
    } 
  }, [location.pathname, user]);
```

And that's it, we have now connected our React Front-End to our Django Back-End RESTful API.

Congratulations, you are now a full-stack developer!!!

## Conclusion

Congratulations on completing this lecture! You've learned how to connect Axios with views in a full-stack development environment, enabling seamless communication between a React frontend and Django backend. By implementing user authentication, you've enhanced the security and functionality of your application. Keep exploring and building amazing projects!
