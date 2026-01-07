# React Hooks

## What are we trying to accomplish?

In this lesson, students will transition from manually manipulating the DOM to using React’s state-driven and lifecycle-aware programming model. The goal is to help students understand how React manages data over time, how changes in state trigger re-renders, and how side effects such as data fetching and subscriptions fit into the React rendering lifecycle. By the end of this lesson, students should be able to reason about *why* hooks exist, not just *how* to use them, and begin thinking in terms of declarative UI rather than imperative DOM updates.

---

## Lectures and Assignments

### Lectures

- [The useState Hook](./1-useState-hook.md)
- [The useEffect Hook](./2-useEffect-hook.md)

### [Assignments](./assignments.md)

---

## Terminal Learning Objectives (TLO's)

- Implement the `useState` hook to manage and update component state.
- Replace manual DOM manipulation with state-driven rendering using JSX.
- Dynamically render lists of data using `.map()` and React keys.
- Add and remove data from state using immutable patterns such as spread and filter.
- Implement the `useEffect` hook to perform side effects such as API requests.
- Correctly configure dependency arrays to control when effects run.
- Implement cleanup logic in `useEffect` to handle component unmounting and effect re-runs.
- Integrate asynchronous logic with React’s render cycle.

---

## Enabling Learning Objectives (ELO's)

- Understand the difference between the Virtual DOM and the real DOM.
- Explain how state changes trigger re-renders in React.
- Describe why React requires immutable state updates.
- Explain why hooks must be called at the top level of a component.
- Understand component lifecycle phases: mounting, re-rendering, and unmounting.
- Explain how `useEffect` maps to lifecycle behavior in functional components.
- Understand the purpose and importance of the dependency array.
- Reason about how asynchronous side effects interact with rendering.
- Develop a mental model for declarative UI updates in React.
