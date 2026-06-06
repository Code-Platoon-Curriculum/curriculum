# UI Fundamentals

## <a href="https://docs.google.com/presentation/d/1WLlJ8Br3V1LryvG2JqwOJ0P-ySHRWC2TXBsj3HihaP8/edit?usp=sharing" target="_"> LECTURE SLIDE DECK </a>
## Introduction

Today, we are going to look at the absolute starting point of any great application: the User Interface (UI).

When building with agentic tools like Claude Code, your biggest superpower isn't your ability to write syntax—it’s your ability to communicate intent. Claude Code can build almost anything, but it cannot read your mind. If you give an AI a vague prompt like "make a workout app," you will get a generic, frustrating result.

Today, you will learn how to use visual sketching tools and structured user journeys to create a bulletproof blueprint that Claude Code can transform into a production-ready front-end application on the first try.

---

## Lesson

### What is the User Interface?

A User Interface (UI) is the part of a computer program, website, mobile app, or device that allows people to interact with it. It includes everything a user can see, touch, click, type into, or receive feedback from. Buttons, menus, icons, forms, images, text fields, sliders, and navigation menus are all examples of user interface elements.

Think of a User Interface as the bridge between humans and technology. Computers process information using code, logic, and data, but most people do not communicate directly with computer code. Instead, the UI translates complex computer functions into simple visual and interactive elements that people can understand and use. For example, when you click the "Send" button in an email application, you are not writing the networking code required to deliver the message. The User Interface provides a simple button that triggers all of those complex processes behind the scenes.

A useful real-life comparison is a car dashboard. When you drive a car, you interact with the steering wheel, pedals, speedometer, fuel gauge, buttons, and touchscreens. These controls allow you to operate a very complex machine without needing to understand the engineering details of the engine, transmission, or braking system. The dashboard and controls are the car's user interface. Similarly, the UI of a software application allows users to perform tasks without understanding the underlying programming.

---

### Why is a Good Interface so Important?

A good User Interface is critically important in a full stack application because it is the primary point of interaction between the user and all of the functionality built throughout the application. No matter how powerful your backend is, how well-designed your database is, or how efficient your APIs are, users judge the application based on what they can see and interact with. If the interface is confusing, difficult to navigate, or visually overwhelming, users may never realize how much work and functionality exists behind the scenes.

To understand this better, let's review the layers of a full stack application:

- Frontend (User Interface): What users see and interact with.
- Backend (Server Logic): Processes requests and business logic.
- Database: Stores and retrieves data.

Think of a restaurant. The kitchen may have world-class chefs, expensive equipment, and incredible recipes (backend and database), but if customers receive a confusing menu, poor service, and unclear ordering instructions (UI), they will likely leave dissatisfied. The quality of the kitchen becomes irrelevant because the customer never experiences it properly.

The UI Creates the First Impression

When users open an application, the User Interface is the first thing they encounter. Humans naturally make judgments very quickly. If an application looks outdated, cluttered, or confusing, users may assume the entire system is unreliable.

---

### Identifying your Application

#### What is your App?

Before you touch a canvas, you must define the core identity of your application in one or two sentences.

> Example: Our Reference App: A lightweight, mobile-first Workout Tracker that allows users to quickly log exercises, sets, reps, and weights during a workout, and view their history over time.

---

#### What Problem Are We Solving?

Before discussing buttons, menus, or screens, answer:

* What problem does this application solve?
* Why would someone use it?
* What pain point exists today?
* What is frustrating about the current process?
* How are users solving this problem right now?

In our example, we are building a workout application but these questions apply to all applications you may be thinking about.

Problem:

> When logging my workouts, it's on spreadsheets and notebooks, this is messy and I can't really track my progress very well.


---

#### Who Are the Users?

Different users need different interfaces.

* Who will use the application?
* Are there multiple user types?
* What are their responsibilities?
* What information does each user need?

---

### Clarify your Features

This is actually one of the most important steps in software development. Many new developers jump straight into wireframing screens, choosing colors, or building React components before they truly understand **what problem the application solves** and **what users need to accomplish**.

#### What Are the User Goals?

Users don't care about your code. They care about completing tasks.

* What are users trying to accomplish?
* What are the top 3 reasons they log in?
* What tasks do they perform most frequently?
* What actions create value?

---

#### What Information Must Users See?

Now identify data requirements.

* What information should users view?
* What information should users create?
* What information should users update?
* What information should users delete?
* What information should users never see?

---

#### What Actions Can Users Perform?

Every major action usually becomes a feature. Can users:

* Create something?
* Read something?
* Update something?
* Delete something?
* Search?
* Filter?
* Sort?
* Export?
* Share?

---

### How to Write your users Journey

What Does the User Journey Look Like? Think about the user's step-by-step experience. What happens when:

* A user first visits?
* A user signs up?
* A user logs in?
* A user completes their primary task?
* A user makes a mistake?

---

### Draw out your App utilizing <a href="https://tldraw.com" target="_">TLDraw</a>

You are now aware of what your user should be doing and have the capabilities to do. With that said, we can now start identifying screens and their individual content matching our user journey and the features we have for said journey.

Examples:

* Home
* Dashboard
* Profile
* Settings
* Search Results
* Details Page
* Reports
* Admin Panel

---

#### What Should Be On Each Page?

Now focus on layout. For each page:

* What information appears?
* What actions are available?
* What buttons exist?
* What forms exist?
* What navigation exists?

---

#### What Should Happen When Something Goes Wrong?

This is a commonly missed step by new developers and definitely a step that is vital to the integrity of any application. What if:

* Login fails?
* Internet disconnects?
* Form validation fails?
* Payment fails?
* User enters invalid data?

---

### Practical Template

When planning your next full stack application, answer these eight questions first:

1. What problem does the application solve?
2. Who are the users?
3. What are their primary goals?
4. What information do they need?
5. What actions can they perform?
6. What pages are required?
7. What data must be collected?
8. What permissions exist?

In fact, for many full-stack projects, 80% of the UI can be sketched simply by answering these questions before writing a single line of code.

## Conclusion

As modern builders, your relationship with coding has fundamentally changed. You no longer need to spend weeks mastering complex UI framework syntax just to get a button to render correctly on a screen. Agentic tools like Claude Code can handle that heavy lifting in seconds. 

But remember the core lesson of today: **AI accelerates execution, but it does not replace architecture.**

If you feed an AI a weak, unstructured prompt, it will spend hours generating code for an application you didn't actually want. By taking the time to answer these architectural questions, define your user journeys, and sketch your boundaries in TLDraw, you are doing the real work of a Software Engineer. You are designing the intent.

Your TLDraw sketches and written user journeys are the exact "context packages" that Claude Code thrives on. When you hand a precise visual and structural blueprint to an AI agent, you unlock its true potential, transforming it from a simple code assistant into a powerhouse development partner.

For your homework, pick your application idea, open TLDraw, and answer the 8-question Practical Template. Next time, we will take those exact blueprints and watch Claude Code turn them into a running application right before our eyes.
