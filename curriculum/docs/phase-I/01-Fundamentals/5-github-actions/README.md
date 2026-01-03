# GitHub Actions

## What are we trying to accomplish?

In this lesson, we introduce **GitHub Actions** as a core tool for modern software automation and Continuous Integration (CI). The goal is to move students from **manually running commands** to **trusting automated systems** that validate code every time it changes.

Students will learn how workflows act as programmable rules that define **when** automated checks run, **where** they run, and **what** they execute. By the end of this lesson, students will understand how GitHub Actions fits into professional development pipelines and how it works alongside tools like **Jest**, **Docker**, and **GitHub pull requests** to ensure code quality.

---

## Lectures & Assignments

### Lectures

- [Intro to Workflows](./1-intro-to-workflows.md)  
- [Managing Workflows](./2-managing-workflows.md)

### [Assignments](./assignments.md)

---

## Enabling Learning Objectives (ELO's)

- What GitHub Actions workflows are and how they support Continuous Integration
- The relationship between **events, workflows, jobs, and steps**
- Why automated testing is an industry standard in professional software development
- How CI workflows reduce human error and increase confidence when merging code
- The role of the **Actions tab** as a feedback and observability tool
- The conceptual difference between **workflows** (automation orchestration) and **Docker** (environment consistency)
- When and why workflows should run (pushes, pull requests, manual triggers, schedules)

## Tangible Learning Objectives (TLO's)

- Create GitHub Actions workflows using YAML
- Configure workflows to run on specific branches and pull requests
- Execute workflows manually using `workflow_dispatch`
- Run a JavaScript test suite automatically within a GitHub Actions pipeline
- Identify passing and failing workflows using GitHub’s Actions UI
- Debug failed workflows by inspecting logs and step output
- Update workflows using proper version control and review practices
- Execute test suites both natively and via Docker inside a workflow

