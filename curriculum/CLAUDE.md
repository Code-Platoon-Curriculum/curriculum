# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-phase software engineering curriculum delivered as a static MkDocs site. Content lives in `docs/` as Markdown files, configured via `mkdocs.yml`, and deployed to AWS EC2 via GitHub Actions on push to `main`.

## Local Development

```bash
# From the curriculum/ directory
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Serve locally at http://localhost:8000
mkdocs serve

# Build static site (outputs to site/)
mkdocs build --clean
```

## Navigation Structure

All curriculum navigation is defined in `mkdocs.yml`. When adding new lessons or modules, register them in the `nav:` section of `mkdocs.yml` — MkDocs will not include unlisted files in the built site.

## Curriculum Architecture

Content is organized into sequential phases under `docs/`:

- **Phase I** — Fundamentals: Docker, Git, Python/JS, OOP, DSA
- **Phase II** — Full-Stack: React, Django, PostgreSQL, Docker Compose
- **Phase III** — AI & ChatBots: Regex bots, NLP/text preprocessing, deep learning, retrieval-based bots, generative AI
- **Phase IV** — Cloud: AWS, deployment, NGINX
- **Phase V** — Capstone projects

Each module typically follows this structure:
```
module-name/
├── README.md         # Overview and learning objectives (TLOs/ELOs)
├── 1-lecture.md      # Numbered lesson files
├── 2-lecture.md
├── assignments.md
└── resources/
```

## Content Conventions

- **TLOs** (Terminal Learning Objectives) — final mastery targets listed in READMEs
- **ELOs** (Enabling Learning Objectives) — intermediate milestones
- Phases are designed to be taken in order; later modules assume prior knowledge
- `old/` subdirectories in each phase contain archived/deprecated lesson versions — do not modify them
- `docs/page-resources/` holds media assets (~72 MB); avoid adding large binaries

## Deployment

CI/CD is configured in `.github/workflows/deployment.yml`. Merging to `main` triggers:
1. MkDocs build
2. rsync to AWS EC2 (IP stored in `EC2_PUBLIC_IP` secret)
3. NGINX reload on the EC2 instance

Do not push directly to `main` during active curriculum development — use feature branches (e.g., `phase-III`) and PR into `main` when a phase is complete.
