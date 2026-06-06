# Building and Deploying Your SPA

## Introduction

In our previous lesson, we focused on the most important part of software development: understanding the problem, identifying our users, defining features, and creating wireframes that describe the user experience. Today, we take those blueprints and turn them into a real application.

Historically, building applications required developers to spend months learning programming languages, frameworks, build systems, deployment pipelines, and hosting providers before they could create something useful. Modern agentic tools have changed that reality.

As builders, our goal is no longer to memorize syntax. Our goal is to clearly communicate our vision and leverage AI to execute it.

---

## Lesson

### What is a Single Page Application?

A Single Page Application (SPA) is a web application that loads a single HTML page and dynamically updates the content as users interact with it. Unlike traditional websites, an SPA does not continuously request entirely new pages from a server every time a user clicks a link. Instead, the application loads once and then updates portions of the screen as needed. When you navigate around these applications, the entire page doesn't reload. Instead, the content changes instantly while maintaining a smooth user experience. That is the power of a Single Page Application.

---

### Understanding our Tech Stack

Technology stacks are collections of tools and technologies that work together to build an application. Lets break down everything we will be using!

---

#### What is and Why React?

React is a JavaScript library used to build user interfaces. React allows developers to create reusable building blocks called components. Instead of creating entire pages repeatedly, React encourages us to build small pieces and assemble them together. Think of React like LEGO bricks. Each component is a LEGO piece. Pages are combinations of those pieces. Applications are combinations of pages.

---

##### Why React?

React provides:

* Reusable Components
* Faster Development
* Easier Maintenance
* Excellent Performance
* Massive Industry Adoption

More importantly for builders, Claude Code is exceptionally good at generating React applications. Because React is so widely used, Claude has enormous amounts of training data to draw from. When we ask Claude Code to build interfaces, React is often the best choice.

---

##### What is and Why React Router DOM?

A single page application is meant to render one time and one time only and then change the content of said page dynamically through JavaScript. This allows single page applications to deliver the User Interface to the user quick and efficiently but if it's only rendering once than how am I supposed to render different pages and handle something like page routing???

That's where React-Router-DOM comes into play. React Router DOM could be thought of as an extension to the React Library giving it the ability to control Routing with the browser and without having to re-render the page each time.

---

#### What is and Why Vite?

Vite is a modern development tool used to create React applications. Historically, frontend projects required complicated setup processes. Developers spent hours configuring:

* Build systems
* Bundlers
* Development servers
* Project structures

Vite solves that problem by bringing in a batteries included mindset where all of these issues are standardized and easily executed by developers and/or builders.

---

##### Why Vite?

Vite provides:

* Instant project creation
* Extremely fast development servers
* Automatic hot reloading
* Optimized production builds

For builders, Vite allows us to focus on creating applications rather than configuring tooling.

---

#### What is and Why Vercel?

Vercel is a deployment platform. Deployment simply means making your application available on the internet.

When you're developing locally, only your computer can access the application. After deployment, anyone with a URL can access it.

> Deployment == Publish

---

##### Registering with Vercel

Visit <a href="https://vercel.com" target="_">Vercels Website</a> and create an account using your Github since it already is part of your development workflow. Once registered, you will be able to deploy applications directly from your repositories by executing very few terminal commands.

---
### Building Your Application

#### Start your Project

Now we are ready to start our project. We have already covered installfest so we have everything we need to get started. Lets go ahead and start our new Vite + React Project. In a safe location, execute the following:

```bash
npm create vite
```

You'll then be promted to specify a name for your project. >> This will then be traced by packageName, you can press enter with the default value >> You'll then be asked to choose a Front-End library. In this case you should choose `React` >> Once you've selected `React` you'll be asked to choose a variant which is basically a few different standardized versions of React Apps. In this case we will choose `JavaScript` >> finally you'll be asked if you'd like to install and start your app now. Go ahead and submit `Yes` by pressing enter.

Once this action is completed you will see a folder with the dictated directory name, you can open it up and see the files and directories created by `Vite`, we won't do a deep dive into this technology because that is not the purpose of this course any changes we make will be explicitly stated to get your app running.

You can now open your own browser (we recommend Google Chrome) and visit <a href="http://localhost:5173/" target="_">http://localhost:5173/</a> and View the React Application you've just created.

Finally we can end our set up by installing `react-router-dom` onto our project with the following command:

```bash
npm install react-router-dom
```

#### Formatting your WireFrames as a Project

Here's what we have up to this point:

- WireFrame images for both pages and components
- User Stories for pages and components 
- User Story for the User Journey in this Application

But this isn't an App yet so far we've done all of the planning but haven't seen the fruits of our labor. Let's get started by bringing them in, first lets create a new directory within the React Project we created and name it `app_outline`, within this application we will break everything down into the following file and directory structure:

```bash
app_outline
| - app.png
| - user_journey.md
| - style_guide.md
| - pages
|    | - homepage
|    |      | - user_story.md
|    |      | - hompage.png
|    |
|    | - contact_page
|    |      | - user_story.md
|    |      | - contact_page.png
```

This will allow Claude Code to easily isolate each page, feature, and components it needs to create in order to bring our application to live. We can do two things, limit context and isolate the scope of the task claude code is attempting to execute at a time.

#### Prepping Claude Code

Now we can hand things off to Claude code and give it a nice prompt for it to leverage all of our hard work and bring it to life. Lets first bring claude code into our project and writing out the `CLAUDE.md` by executing `/init` within our project.

Once that's done, we should ensure that claude code is capable of observing and checking it's own work. This means we need to give it a feedback loop so it can check it's own work and ensure the work it's doing matches our demands. We can do this by ensuring the `playwright` mcp server is installed and accessible to claude code by running `/mcp list`.

Now lets think about the complexity of our task, the tokens that may be utilized while executing this task of creating an entire application. In this case lets stick with Sonnet but lets ensure its effort level is at minimum a medium. You can try it in low and see the outcome but this is a pretty massive operation that may require some more thinking and effort before executing. 

Additionally, this is a massive task that will interact with a variety of file types, coding languages, and browser feedback so (without using superpowers) lets ensure Claude thinks through each tasks and maps it properly by putting it in `planning` mode.

In summary:

- CLAUDE.md created with accurate context
- Playwright MCP Server connected to Claude Code
- Medium Effort on the Sonnet Model (you can experiment here but this is our recommendation)
- Planning mode set for Claude Code.

> be adviced using a model like Opus may consume too many tokens and leave your project incomplete.

#### Leveraging Claude Code

Now we are ready to have Claude Code bring our application to life. If you followed our recommendations than here is an example prompt you can utilize:

```text
I would like you to build a Front-End Single Page Application from the wire frames and user stories I have mapped out. 

The tech-stack for this applicatoin will be as follows:
- React.js + Vite
- React Router DOM with Browser Router

There will be no API interactions and all data should be retained only at the browser level, meaning if I refresh/rerender my site all of the data should reset.

I have created a series of documents and images as a reference for what I would like this application to look like and isolated everything by pages. Take a look at this folder @./app_outline and read the `user_journey.md` file to get context for the users journey through the application. Then look at the `app.png` to visualize the entire application. Finally under pages, you'll find a wire-frame corresponding to each page along with a detailed user story for how a user would interact with this page. Additionally, when it comes to design style, you can read the `style_guide.md` and apply its guidelines as you see fit.

Ensure to utilize the `playwright` MCP server to supervise the development of this Application. After each page is built, use Playwright to screenshot it and compare against the wireframe before moving on and ensuring it's output matches the desired outcome from the wireframes and user stories.

Finally the execution of this app should happen in phases, phases should correspond roughly to pages or major feature areas. I'll leave it to you to declare the number of phases and what their independent passing conditions are, but these conditions should be approved by me and allow me to provide you feedback before moving on into the next phase.

Before writing any code, please confirm your understanding of the application by summarizing the user journey and listing the pages you plan to build.
```

This prompt is **NOT** the ONLY way to formulate your prompt and approach this problem, there may be additional context you'd like to share with Claude pending on the requirements of your app. Ensure you use and leverage all the fundamentals you learned regarding prompt engineering.

#### Version Control

Now that our application is created, let's ensure it gets up on Github, create a repository, initialize a git repo and push your code up to Github. This will allow you to share your code with others and yourself to regulate the changes of your code base.

### Deploying with Vercel

Once your application is working locally, it's time to deploy. 

---

#### Continuous Deployment

One of the best parts about modern deployment workflows is continuous deployment, this means that anytime changes happen to our application and get committed to Github they also get pushed to Published version of the website. This should look as such:

```text
Make Changes
 ↓
Commit Changes
 ↓
Push to GitHub
 ↓
Vercel Deploys Automatically
```

---

#### Connect Vercel

Travel to the Vercel Platform and execute the following:

* Click Add New Project
* Import Git Repository
* Select your repository

Vercel will automatically detect this is a React + Vite project. Now we should be able to simply deploy.

---

## Conclusion

By the end of this lesson, you have moved from the planning phase of application development into the execution and deployment phase. You learned what a Single Page Application (SPA) is and why modern frontend applications rely on technologies such as React, React Router DOM, Vite, and Vercel to create fast, responsive user experiences. More importantly, you explored how modern AI-assisted development workflows allow builders to focus less on memorizing syntax and more on communicating product requirements, user experiences, and design intent. Through wireframes, user stories, application outlines, and structured prompting, you now have a repeatable process for transforming an idea into a functioning application. You also learned how to leverage Claude Code as a development partner, using planning, context organization, and browser-based validation to ensure generated applications align with user expectations. Finally, you saw how version control and deployment platforms like GitHub and Vercel allow your work to move from your local machine to a publicly accessible website. As AI development tools continue to evolve, the most valuable skill is not simply writing code—it is clearly defining problems, communicating solutions, and orchestrating the tools available to bring those solutions to life.

