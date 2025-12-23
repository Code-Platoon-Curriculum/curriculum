
# Full-Stack, AI, and Cloud Engineering Curriculum

![Fullstack Development](./curriculum/docs/page-resources/full-stack-diamond.jpeg)

This project will be utilized to manage all content presented during Code Platoons Full Stack Software Engineering Program for Self-Paced, Evening and Weekends, and Immersive.

## Run Locally

Running locally is extremely simple thanks to MkDocs.

Clone the project

```bash
  git clone https://github.com/CodePlatoon/se-curriculum
```

Go to the project directory

```bash
  cd se-curriculum
```

There are some `Python` dependencies within this project for `Material MkDocs` that must be installed prior to interacting with this project.

Create a Python virtual environment:

```bash
python -m venv <.venv>
```

Activate virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies within `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Run the server:

```bash
  mkdocs serve
```


## Deployment

Ideally this project will be Deployed on an AWS ec2 instance.

