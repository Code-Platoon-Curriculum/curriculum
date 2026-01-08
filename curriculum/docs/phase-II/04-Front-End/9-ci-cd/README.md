# Continuous Integration and Continuous Deployment

## What are we trying to accomplish?

In this lesson, students will learn how modern development teams **automate testing and deployment** to safely deliver software at scale. Building on prior knowledge of testing, React, and GitHub, this lesson introduces **Continuous Integration (CI)** and **Continuous Deployment (CD)** as structured, automated workflows rather than manual processes.

Students will first understand how React applications become **static assets** and how those assets can be hosted using **GitHub Pages**. From there, they will design and implement **GitHub Actions workflows** that automatically run end-to-end tests with Cypress, enforce quality gates on pull requests, and deploy verified builds to production.

By the end of this lesson, students should be able to explain *why* CI/CD exists, *how* it reduces risk, and *how* to build a complete CI/CD pipeline for a React + Vite application using industry-standard tools.

---

## Lectures & Assignments

### Lectures

- [GitHub Pages for Static Sites](./1-gh-pages.md)
- [GitHub Actions CI/CD](./2-gh-actions.md)

### [Assignments](./assignments.md)

---

## Terminal Learning Objectives (TLO's) executable

- Deploy a React + Vite application as a static site using GitHub Pages.
- Configure a Vite project for production deployment using the correct base path.
- Explain and implement client-side routing strategies compatible with static hosting.
- Create GitHub Actions workflows to automate testing with Cypress.
- Enforce CI rules that block merges when tests fail.
- Configure environment variables for different deployment environments in GitHub Actions.
- Build and deploy production-ready static assets using automated pipelines.
- Securely authenticate and deploy to GitHub Pages from a CI environment.
- Reason about CI/CD pipelines as a sequence of repeatable, deterministic steps.

---

## Enabling Learning Objectives (ELO's) conceptual

- Explain the difference between static sites and server-rendered applications.
- Describe how React applications are transformed at build time.
- Understand why client-side routing requires special handling on static hosts.
- Articulate the purpose and benefits of Continuous Integration.
- Explain how automated test suites act as quality gates.
- Understand how GitHub Actions executes workflows in isolated environments.
- Reason about environment-specific behavior using environment variables.
- Describe how Continuous Deployment reduces risk and improves delivery speed.
- Develop a mental model for modern, production-grade software delivery pipelines.
