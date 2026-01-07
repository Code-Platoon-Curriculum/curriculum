# React Components

## What are we trying to accomplish?

In this lesson, students move from thinking about React as a single large application to understanding it as a **composition of smaller, reusable components**. The goal is to help students reason about how UI can be broken down into logical pieces, how data flows between those pieces, and how responsibility is divided between parent and child components.

By the end of this lesson, students should understand *why* components exist, what problems they solve in large applications, and how props and component-level state enable predictable, maintainable UI behavior. This lesson emphasizes architectural thinking: deciding where logic should live, how components communicate, and how to avoid tightly coupled designs.

---

## Lectures and Assignments

### Lectures

- [Components and Props](./1-component-props.md)
- [Component Level State](./2-component-lvl-state.md)

### [Assignments](./assignments.md)

---

## Terminal Learning Objectives (TLO's)

- Create reusable React components using functional component syntax.
- Pass data from parent components to child components using props.
- Render dynamic data inside components using JSX expressions.
- Deconstruct props for cleaner and more readable component code.
- Refactor inline JSX into dedicated child components.
- Implement component-level state using the `useState` hook.
- Manage independent UI behavior at the child component level.
- Lift state to a parent component when multiple children depend on shared data.
- Structure React projects using common folder and file conventions.

---

## Enabling Learning Objectives (ELO's)

- Understand what a component represents in a React application.
- Explain what problems components solve compared to monolithic UI files.
- Describe the one-way data flow model in React (parent → child).
- Understand the difference between props and state.
- Reason about when data should be passed as props versus stored as state.
- Understand the trade-offs of parent-owned state versus child-owned state.
- Develop intuition for component responsibility and separation of concerns.
- Build a mental model for how UI composition scales in real-world React applications.
