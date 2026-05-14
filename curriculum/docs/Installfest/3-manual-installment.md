# **Manual Installment**

---

## Introduction

Before we start building full-stack applications, it’s important to have a consistent development environment. This ensures that all the tools we use (Python, Node, PostgreSQL, Git) work correctly and predictably across different machines.

In this lecture, we will install and configure:

* **Package Managers** – Will handle the maintenance of and versioning of our dependencies
* **Python 3** – our main programming language
* **Node.js & npm** – for front-end tooling, Live Server, Vite
* **PostgreSQL** – our relational database
* **Git & GitHub** – for version control
* **Zsh & Aliases** – to streamline terminal commands

> **Note:** Windows users should follow the **WSL/Ubuntu instructions**. Everything in WSL behaves like Linux, which keeps our setup consistent.

---

## Package Management

A package manager, such as `apt-get` on Debian-based Linux systems or `Homebrew` on macOS, is a tool that automates the process of installing, updating, configuring, and removing software on a computer. Rather than manually downloading software from websites, resolving dependencies, and placing files in the correct directories, a package manager provides a centralized system to handle all of this efficiently. When you install a package, the package manager ensures that any other software libraries or tools required for it to run are also installed, preventing conflicts and broken programs. Additionally, package managers maintain a database of installed software and their versions, which makes updating or uninstalling applications straightforward and reliable. They are crucial because they save time, reduce errors, enhance system stability, and make software management consistent across different machines, which is especially important in professional or development environments where reliability and reproducibility are key.


### WSL Ubuntu

The `update` command in apt will fetch a list of packages from an external source that are available for download. This list changes frequently so it's important to run the update command before installing anything to ensure you will be fetching the latest package and not an outdated one.

```bash
# update the list of external packages that are available for install
sudo apt-get update
# you will be prompted for your password at this point
```

### MacOS

[Homebrew](https://brew.sh/) is a package manager for MacOS. You can install it by running the following command (more easily copy/pasted from their website):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

> It isn't important to understand the details but `bash` is a specific shell (the default on older macs) and `curl` is a program that allows us to install a file from a url.

> It is not necessary that you read the output but Homebrew will be installing Command Line Tools for XCode first if you do not already have it. This might take a fair bit of time (up to 15 minutes), but it's a welcome improvement from the previous solution of downloading all of XCode (Apple's one stop shop for doing development on a Mac) which is far larger (up to 3 hours).

Let's check if we've installed homebrew correctly. You may need to close and reopen your terminal first.

```bash
brew
```

If you see a list of further options it is working. If you are getting a message that the command is not found something went wrong.

Homebrew is going to do a lot of work for us in that it manages our software versions, so always ensure that it's up-to-date and that it's healthy. First run:

```bash
# grabs a list of all the current packages you can install
brew update
```

then:

```bash
brew doctor
```

`brew doctor` may tell you a lot of stuff and if it's complex you will want to reach out to one of us. We're ideally shooting for a message like this:

```bash
brew doctor
# Your system is ready to brew.
```

Warnings are good to read but are not mandatory to fix, so continue on for now and reach out if you hit a snag down the line.

---

## Python

Python is a high-level, interpreted programming language known for its simplicity, readability, and versatility, making it one of the most popular languages in the world. It was created by Guido van Rossum and first released in 1991 with a philosophy that emphasizes code readability and developer productivity. Python uses a clear and concise syntax that closely resembles natural language, which makes it accessible for beginners while still powerful for advanced users. It is a general-purpose language, meaning it can be used for a wide variety of applications, including web development, data analysis, artificial intelligence and machine learning, automation, scientific computing, and software prototyping. Python comes with a rich standard library that provides pre-built modules for common tasks, and it has a vast ecosystem of third-party packages available via package managers like `pip`. Its combination of simplicity, flexibility, and a strong supportive community has made Python a cornerstone in both education and professional software development.


Python is included in both MacOS and Ubuntu by default, but the system version may be old or not fully manageable. We will install a version we control.


### **MacOS**

1. Check if Python3 exists:

```bash
python3 --version
```

You should see something like:

```bash
Python 3.8.10
```

We can also check where this current version of `Python` is located vy utilizing pip.

```bash
which python3
```

`which` is a command that tells us where a given command is located in the filesystem. The result should be `/usr/bin/python3`.

2. Install Python via Homebrew:

```bash
brew install python
```

5. Verify the installation:

```bash
which python3
```

The result should be `/usr/local/bin/python3`. If it's not, speak to an instructor or TA because your Homebrew installations are not being correctly picked up.

This install should also include python's package manager, `pip`. To test this enter the command:

```bash
python3 -m ensurepip
```

---

### **WSL / Ubuntu**



1. Install Python 3, pip, and setuptools. This will allow us to utilize Python to its full potential through out the program:

```bash
sudo apt install -y python3 python3-pip python3-venv python-is-python3
```

2. Verify the installations were successful with the following commands:

```bash
python3 --version
pip3 --version
```

---

### **Error Handling (Python)**

* **Python command not found:** Make sure `/usr/local/bin` (MacOS) or `/usr/bin` (WSL) is on your PATH
* **Old version:** Remove the old version or explicitly use the installed path
* **pip not recognized:** Run `python3 -m ensurepip`

---

## **Python Virtual Environments**

A **virtual environment (venv)** is a self-contained folder where Python packages are installed for a single project. This prevents package conflicts between projects. We will dive further into this once through out the program

---

### **Creating a default virtual environment**

1. Open terminal and navigate to your home directory:

```bash
cd ~
```

2. Use the following command to create your first Python Virtual Environment (venv):

```bash
python3 -m venv .default
```

This command will create a directory named `.default` and will only be visible if you run the command `ls -a` to include privatized files and directories.

3. Activate the venv:

```bash
source ~/.default/bin/activate
```

After running the above you should see the name of the venv ('.default') represented somewhere in your command line. Keep in mind, a venv is only activated while the terminal that executed the above command is alive and all new terminals must manually activate the venv in order to access it's dependencies. Because it is easy to forget to do this we will make it happen on startup by adding it to our `.zshrc` file later.

4. Deactivate the Virtual Environment by typing:

```bash
deactivate
```

You'll notice that `.default` is no longer present at the left of your user within your terminal.

---

## **Installing Node.js & npm**

Node (commonly referred to as **Node.js**) is a JavaScript runtime built on Google’s V8 engine that allows developers to run JavaScript code outside of the browser, typically on a server. It provides an event-driven, non-blocking I/O model, which makes it lightweight and efficient for handling concurrent operations like network requests, file system access, and APIs. With Node, developers can build scalable backend services such as web servers, real-time applications, and APIs, all using JavaScript—the same language used on the client side. It also comes with **npm (Node Package Manager)**, the world’s largest ecosystem of open-source libraries, which makes it easier to integrate external tools and frameworks into applications.


---

### **MacOS (via Homebrew)**

In this section, we'll use Homebrew to install `npm`, the default package manager for node. We'll then use `npm` to install `n`, which is a tool to help manage different versions of `node`. Lastly, we'll use `n` to install the latest stable version of `node`.

```bash
# use apt to install npm
brew install npm
# use npm to install n (-g means globally, as opposed to in a specific project/folder)
sudo npm install -g n
# use n to install the latest stable version of node
sudo n stable
```

Verify installments with the following commands:

```bash
node -v
npm -v
```

---

### **WSL / Ubuntu**

In this section, we'll use `apt` to install `npm`, the default package manager for node. We'll then use `npm` to install `n`, which is a tool to help manage different versions of `node`. Lastly, we'll use `n` to install the latest stable version of `node`.

```bash
# use apt to install npm
sudo apt-get install npm
# use npm to install n (-g means globally, as opposed to in a specific project/folder)
sudo npm install -g n
# use n to install the latest stable version of node
sudo n stable
```

Verify node and npm were installed successfully with the following:

```bash
node -v
npm -v
```

Close and reopen your terminal if necessary and test that both the commands `node` and `npm` are recognized.

---

### **Error Handling (Node.js)**

* **Wrong version:** Use `sudo n stable` to reinstall the latest stable version
* **Command not found:** Close and reopen terminal or check PATH

---

## **Git & GitHub**

**Git** is a distributed version control system that lets developers track changes in their codebase, collaborate with others, and manage different versions of a project efficiently. It allows you to create branches, merge code, and roll back to previous states, making teamwork and experimentation safe and organized. **GitHub**, on the other hand, is a cloud-based platform built around Git that provides hosting for repositories along with collaboration tools like pull requests, issues, and project boards. While Git is the tool that manages version control locally and on servers, GitHub acts as a service that makes sharing, reviewing, and managing code with others much easier.


---

### **Installing Git**

**MacOS:**

```bash
brew install git
```

**WSL / Ubuntu:**

```bash
sudo apt-get install -y git
```

---

### **Configure Git**

The following configurations will allow us to easily interact with both git and github moving forward so ensure you utilize your github username as your name, your email associated with your github account for your user.email.

```bash
# run each command separately
git config --global user.name "<YOUR_NAME>"
git config --global user.email "<YOUR_EMAIL>"
git config --global core.editor "code --wait"
git config --global -l
```

You should see from the last command in the above code block:

```
user.name=<YOUR_NAME>
user.email=<YOUR_EMAIL>
core.editor=code --wait
```

---

### **GitHub CLI (`gh`)**

Github's preferred way you interact with it now is a command line tool called `gh`. First, you will need a github account to continue, then, in your terminal type:


#### **Install:**

* MacOS: `brew install gh`
* WSL: `sudo apt-get install -y gh`

#### **Authenticate:**

Once the `gh` command line interface is installed, we can Authenticate with our github accounts allowing us to easily communicate with Github itself from our local machine terminal.

```bash
gh auth login
```

and follow the wizard steps to complete the authentication process (the default choices are what you want). When done you should be able to clone a repo like so:

```bash
gh repo clone lodash/lodash
```

This will install that repo in your current directory. Assuming this is successful if you want to delete it afterwards type:

```bash
rm -rf lodash
```

---

## **Aliases**

### **What are aliases?**

Machine aliases (often just called **aliases**) are custom shortcuts you can define in your shell (like Bash or Zsh) to replace longer or more complex commands with a shorter, easier-to-remember keyword. For example, instead of typing `git status` repeatedly, you could create an alias like `alias gs="git status"`. They are useful because they save time, reduce typing errors, and allow you to customize your development environment to fit your workflow. Aliases are especially important for tasks you run frequently or commands that are long and error-prone, making your overall work on the machine faster and more efficient.

---

### **Starter `.zshrc`**

A **.zshrc file** is a configuration file that runs automatically whenever a new **Zsh (Z shell)** terminal session starts, allowing users to customize their shell environment. Inside this file, you can define aliases, environment variables, custom functions, themes, and plugins that modify how your terminal behaves and looks. For example, you might set your default text editor, adjust your PATH, or enable tools like Oh My Zsh. Each time you open a new Zsh terminal, the `.zshrc` file is read and executed line by line, applying all your customizations so that your shell is tailored to your workflow.

Travel back to the root user directory and lets ensure this file exist:

```bash
cd ~
ls -a
```

**If** the file does not exist, lets go ahead and create one:

```bash
touch .zshrc
```

Finally, lets open the `.zshrc` file:

```bash
code .zshrc
``` 

and add the following `path` for our environment:

```bash
# * MacOS ONLY * Points to version-less executables for python and pip
export PATH="$(brew --prefix python)/libexec/bin:$PATH"

# Activate default Python venv
source $HOME/default/bin/activate
```

Reload your zsh terminal to utilize the `.zshrc` file by running the following command:

```bash
source ~/.zshrc
```
Moving forward every new zsh terminal will load this file first prior to becoming available.

---

## **Installing PostgreSQL**

**PostgreSQL** (often called **Postgres**) is an open-source, powerful, and highly reliable relational database management system (RDBMS) that uses SQL (Structured Query Language) to store, manage, and retrieve data. Known for its strong standards compliance and advanced features, PostgreSQL supports complex queries, transactions, indexing, JSON storage, and even custom data types, making it suitable for both traditional and modern applications. It is designed for scalability and data integrity, handling everything from small projects to large, enterprise-level systems. Because it’s open-source, actively maintained, and extensible, PostgreSQL is widely used in web applications, analytics, and data-driven software where stability and performance are critical.


---

### **MacOS**

We will now install PostgreSQL by running the following command:

```bash
brew install postgresql@14
```

Start a PostgreSQL instance (in the background) like so:

```bash
brew services restart postgresql@14
```

To enter PostgreSQL we will switch our shell user to one named `postgres`, and then we can enter the running PostgreSQL instance.

```bash
# connect to the running PostgreSQL instance as the user 'postgres'
psql postgres
```

If your terminal now looks like it does below, you have successfully installed PostgreSQL:

```sql
postgres=#
```

To exit out of this environment type `\q`

```
postgres=# \q
```

### **WSL / Ubuntu**

We will now install PostgreSQL by running the following command:

```bash
sudo apt-get install postgresql@14 postgresql-contrib
```

Start a PostgreSQL instance (in the background) like so:

```bash
sudo service postgresql@14 restart
```

To enter PostgreSQL we will switch our shell user to one named `postgres`, and then we can enter the running PostgreSQL instance.

```bash
# switch to the user `postgres`
sudo -i -u postgres

# connect to the running PostgreSQL instance
psql
```

If your terminal now looks like it does below, you have succesfully installed PostgreSQL:

```psql
postgres=#
```

To exit out of this environment type `\q`

```psql
postgres=# \q
```

Then finally to return to ubuntu type in:

```bash
exit
```

---

### **Error Handling (PostgreSQL)**

* Service not starting → `journalctl -u postgresql`
* `psql` not found → reinstall or check PATH
* Permission issues → always use `sudo -i -u postgres`

---

## Conclusion

Congratulation, now you have a working environment for our tech stack within your local machine!
