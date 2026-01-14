# FRONT-END Template Code

## Dependencies

Once you create your project ensure to install both *axios*, react-bootstrap and *react-router-dom*:

```bash
npm install axios react-router-dom react-bootstrap bootstrap
```

## Package.json `scripts`

```json
{
  "scripts": {
    "dev": "vite --host",
    "build": "vite build",
    "watcher": "vite build --watch",
    "lint": "eslint .",
    "preview": "vite preview"
  }
}
```

## Dockerfile

```Dockerfile
FROM node:18

WORKDIR /app

COPY . .

RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev"]
```


## index.css

**CLEAR ALL OTHER STYLING**

```css
body{
  width: 100%;
  height: 100%;
}

#root{
  width: 100%;
  height: 100%;
}
```

## main.jsx

```jsx
import { createRoot } from 'react-dom/client'
import { RouterProvider } from 'react-router-dom';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css'


createRoot(document.getElementById('root')).render(
    <RouterProvider router={router}/>
)
```

## router.jsx

```jsx
import { createBrowserRouter } from 'react-router-dom'
import AuthPage from "./pages/AuthPage"
import HomePage from "./pages/HomePage"
import App from "./App"

const router = createBrowserRouter([
    {
        path:"/",
        element: <App/>,
        children:[
            {
                index:true,
                element:<AuthPage/>
            },
            {
                path:"home",
                element: <HomePage />
            }
        ]
    }
])

export default router
```

## App.jsx

```jsx
import { useEffect, useState } from 'react'
import { Outlet } from 'react-router-dom'
import './App.css'

function App() {
  const [user, setUser] = useState(null)

  useEffect(()=>{
    console.log(user)
  }, [user])

  return (
    <>
     <Outlet context={{ user, setUser }}/>
    </>
  )
}

export default App
```

## Pages

### AuthPage.jsx

```jsx
import { useOutletContext } from "react-router-dom";
import AuthForm from "../components/AuthForm";

const AuthPage = () => {
    const {setUser} = useOutletContext()

    return (
        <>
            <h1>Authentication Page</h1>
            <AuthForm setUser={setUser} />
        </>
    )
}

export default AuthPage;
```

### HomePage.jsx

```jsx
import { useState } from "react";
import { useOutletContext } from "react-router-dom";
import Stack from 'react-bootstrap/Stack';
import TaskDisplay from "../components/TaskDisplay";
import TaskForm from "../components/TaskForm";

const HomePage = () => {
    const {user, setUser} = useOutletContext()
    const [tasks, setTasks] = useState([{id:1, title:"Code some more"}])

    const addTask = (task) => {
        setTasks([...tasks, task])
    }

    const rmTask = (rmTask) => {
        setTasks(tasks.filter((task)=>(
            task.id !== rmTask.id
        )))
    }

    const updateTask = (editTask) => {
        setTasks(tasks.map((task)=>(
            task.id === editTask.id ? editTask : task
        )))
    }

    return (
        <>
            <h1>Welcome {user && user}: Here are your Tasks <button onClick={()=>setUser(null)}>Log Out</button></h1>
            
            <Stack gap={3}>
                <TaskForm addTask={addTask}/>

                {tasks.map((task)=>(
                    <TaskDisplay 
                        key={task.id} 
                        task={task}
                        rmTask={rmTask}
                        updateTask={updateTask}
                    />
                ))}

            </Stack>
        </>
    )
}

export default HomePage;
```

## Components

### AuthForm.jsx

```jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom'
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

const AuthForm = ({setUser}) => {
    
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [create, setCreate] = useState(true)
    const navigate = useNavigate()

    const handleSubmit = (e) => {
        e.preventDefault()
        let userDict = {
            email:email,
            password: password
        }
        let method = create ? 'CREATE ACCT' : 'LOGIN ACCT'
        console.log(userDict, method)
        setUser(userDict.email)
        setCreate(true)
        setEmail('')
        setPassword('')
        navigate('/home/')
    }

    return (
        <>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                    <Form.Label>Email address</Form.Label>
                    <Form.Control 
                        type="email" 
                        placeholder="Enter email" 
                        value={email}
                        onChange={(e)=>setEmail(e.target.value)}
                    />
                    <Form.Text className="text-muted">
                    We'll never share your email with anyone else.
                    </Form.Text>
                </Form.Group>

                <Form.Group className="mb-3" controlId="formBasicPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control 
                        type="password" 
                        placeholder="Password" 
                        value={password}
                        onChange={(e)=>setPassword(e.target.value)}
                    />
                </Form.Group>

                <Form.Group className="mb-3" controlId="formBasicCheckbox">
                    <Form.Check 
                        type="checkbox" 
                        label={create ? "CREATE ACCOUNT" : "LOG IN"} 
                        checked={create}
                        onChange={(e)=>setCreate(e.target.checked)}
                    />
                </Form.Group>

                <Button variant="primary" type="submit">
                    {create ? "CREATE ACCOUNT" : "LOG IN"} 
                </Button>
            </Form>
        </>
    )
}

export default AuthForm
```

### TaskDisplay.jsx

```jsx
import Stack from 'react-bootstrap/Stack';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useState } from 'react';

const TaskDisplay = ({task, rmTask, updateTask}) => {
    
    const [edit, setEdit] = useState(false)
    const [editTitle, setEditTitle] = useState(task.title)
    
    const editTaskHandle = () => {
        let editedTask = {
            id:task.id,
            title: editTitle
        }
        updateTask(editedTask)
        setEdit(!edit)
    }

    return (
        <>
            <Stack direction="horizontal" gap={3} style={{border:"solid black 1vmin"}}>
            {edit ?
            <>
                <Form.Control 
                    className="me-auto" 
                    placeholder={task.title}
                    value={editTitle}
                    onChange={(e)=>setEditTitle(e.target.value)}
                />
                <Button variant="outline-primary" onClick={editTaskHandle}>Submit</Button>
                <div className="vr" />
                <Button variant="outline-secondary" onClick={()=>[setEdit(!edit), setEditTitle(task.title)]}>Cancel</Button>
            </>
            :
            <>
                <div className="p-2">{task.title}</div>
                <div className="p-2 ms-auto">
                    <Button variant='warning' onClick={()=>setEdit(!edit)}>
                        Edit
                    </Button>
                </div>
                <div className="vr" />
                <div className="p-2">
                    <Button variant='danger' onClick={()=>rmTask(task)}>
                        Delete
                    </Button>
                </div>
            </>
        }
        </Stack>
        </>
    )
}

export default TaskDisplay
```

### TaskForm.jsx

```jsx
import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/esm/Button';

function TaskForm({addTask}) {
    const [taskTitle, setTaskTitle] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault()
        let newTask = {
            id: crypto.randomUUID(),
            title: taskTitle
        }
        addTask(newTask)
        setTaskTitle('')
    }
        
    return (
        <>
            <Form onSubmit={handleSubmit} style={{width:"100%", display:"flex", justifyContent:"space-around"}}>
                <Form.Control
                    type="text"
                    placeholder='input a new task title here'
                    value={taskTitle}
                    onChange={(e)=>setTaskTitle(e.target.value)}
                />
                <Button type='submit'>
                    Create
                </Button>
            </Form>
        </>
    );
}

export default TaskForm;
```
