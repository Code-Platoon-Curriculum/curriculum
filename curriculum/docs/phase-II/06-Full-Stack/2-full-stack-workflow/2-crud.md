# Full-Stack CRUD

## Intro

Now that our React frontend is fully authenticated and connected to our Django REST API, we can move into the core responsibility of most full-stack applications: **CRUD operations**.

CRUD stands for:

- **Create**
- **Read**
- **Update**
- **Delete**

In this lecture, we will implement full CRUD functionality for our `Task` model, allowing authenticated users to manage their own tasks. All operations will be performed through our Dockerized Django API and consumed by our React frontend using Axios.

Because authentication is already handled via DRF Token Authentication, every request we make in this lecture will automatically be associated with the currently logged-in user.

---

## Tasks Model CRUD Operations

Our backend exposes the following task-related endpoints:

- `GET /api/v1/tasks/`
- `POST /api/v1/tasks/`
- `GET /api/v1/tasks/<id>/`
- `PUT /api/v1/tasks/<id>/`
- `DELETE /api/v1/tasks/<id>/`

We will now connect each of these endpoints to our frontend and manage state updates accordingly.

---

### Get all Tasks (GET)

When a user navigates to the Home page, we want to immediately fetch all tasks associated with their account. This is a perfect use case for a **React Router Loader**, ensuring the data exists before the page renders. All of this said, we currently don't have a function meant to fetch this data from our Django API. Within *utilities.jsx* lets add the following:

```jsx
export const getTasks = async() => {
    let response = await api.get("tasks/")
    if (response.status === 200){
        let tasks = response.data
        return tasks
    }
    alert(response.data)
    return []
}
```

Now this function sends a GET request with a user token within the Authorization header to our Django Back-End. It always returns an array, if the response status is 200 (i.e. successful) we return the data within the response which we know is an array of objects where each object represents a task. Otherwise we return an empty array. Now all we have to do is connect the dots: 

- We define a loader on the `/home` route:

```jsx
// router.jsx
{
    path:"home",
    element: <HomePage />,
    loader: getTasks
}
```

- we utilize the loader data as the initial state of *tasks* within *HomePage.jsx*:

```jsx
// HomePage.jsx
const [tasks, setTasks] = useState(useLoaderData())
```

This pattern ensures:

* Clean separation of data fetching and rendering
* No “loading flashes” in the UI
* Predictable application state

---

### Create a Task (POST)

Next, we allow users to create new tasks. The API expects a simple object with the key of *title* assigned to a value of string type. Again this request should only be accessible if there's a logged in user, meaning that the axios instance *api* already holds an Authorization header with the users token. This allows our Django API to create tasks that will directly wrap to our current user.

```jsx
// utilities.jsx
export const createTask = async(taskObj) => {
    let response = await api.post("tasks/", taskObj)
    if (response.status === 201){
        return response.data
    }
    alert(response.data)
    return null
}
```

Again, we check if the response status code is of *201*, meaning the request was successful and has returned the task object within the data of the response. If the request failed we alert the user of the error messages and return `null`.

Inside our form component, we handle submission as follows:

```jsx
// TaskForm.handleSubmit
const handleSubmit = async(e) => {
    e.preventDefault()
    let newTask = await createTask({ title: taskTitle })
    if (newTask){
        addTask(newTask)
    }
    setTaskTitle('')
}
```

Here we immediately update the frontend state after a successful API response, keeping the UI in sync **without requiring a refetch.**

---

### Update a Task (PUT)

Updating a task requires sending the task’s ID along with the updated data. We will send our `PUT` request to the endpoint that includes our tasks id and the object holding the edited state of the task. We ensure the request is successful and return the updated task or if unsuccessful we return `null`.

```jsx
// utilities.jsx
export const updateTask = async(taskObj) => {
    let response = await api.put(`tasks/${taskObj.id}/`, taskObj)
    if (response.status === 200){
        return response.data
    }
    alert(response.data)
    return null
}
```

In the *TaskDisplay* component, we construct the edited object and submit it:

```jsx
// TaskDisplay.editTaskHandle
const editTaskHandle = async() => {
    let editedTask = {
        id: task.id,
        title: editTitle
    }
    editedTask = await editTask(editedTask)
    if (editedTask){
        updateTask(editedTask)
    }
    setEdit(!edit)
}
```

This approach ensures:

* Backend validation occurs before updating state
* Only confirmed changes are reflected in the UI
* Each task remains user-scoped through token authentication

---

### Delete a Task (DELETE)

Finally, we allow users to delete tasks. Similarly to our `PUT` request we need to capture the tasks *id* in order to tell the Django API which users task must be deleted. Finally we can return whether the request was successful or not based on the response status.

```jsx
// utilities.jsx
export const deleteTask = async(taskId) => {
    let response = await api.delete(`tasks/${taskId}/`)
    alert(response.data)
    return response.status === 200
}
```

The task component invokes this method and updates state on success:

```jsx
// TaskDisplay.jsx
const deleteTaskHandle = async() => {
    let taskDeleted = await deleteTask(task.id)
    if (taskDeleted){
        rmTask(task)
    }
}

<Button variant='danger' onClick={deleteTaskHandle}>
    Delete
</Button>
```

By removing the task from state after a successful response, the UI remains responsive and consistent with the backend.

---

## Conclusion

At this point, your application supports **full authenticated CRUD operations** across the entire stack.

You have successfully:

* Connected a React frontend to a Dockerized Django REST API
* Scoped all data access using token-based authentication
* Implemented GET, POST, PUT, and DELETE operations
* Used loaders and state updates to maintain UI consistency
* Built a real-world, production-aligned full-stack workflow

With authentication and CRUD complete, your application now mirrors the core architecture of many modern web systems. From here, you are well-positioned to explore enhancements such as pagination, filtering, permissions, or deployment to cloud infrastructure.

Well done — this is real full-stack development.
