# userService



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.allence.cloud/clients-acp/codereview/userservice.git
git branch -M main
git push -uf origin main
```
# Chalice Project UserService

This Markdown file provides a structured guide for setting up your Chalice project efficiently.

## Prerequisites

- Python 3.x installed (https://www.python.org/downloads/)

## Steps

### 1. Create Environment Variables

1. Create a file named `.env` in your project's root directory. This file stores sensitive information like your MongoDB connection URI.
2. Add the following line to your `.env` file, replacing `MONGO_URI =<your_mongo_link_here>` with your actual MongoDB connection string:

### 2. Set Up a Virtual Environment (Recommended)

A virtual environment helps isolate project dependencies and prevent conflicts with other Python environments. Here's how to create and activate one:

1. Open a terminal window.
2. Navigate to your project's root directory.
3. Run the following command to create a virtual environment named `myenv`:

bash
python3 -m venv myenv

#### 3. Activate the virtual environment using the appropriate command for your operating system:

bash
source myenv/bin/activate

##### 4. Run the following command to install dependencies:

bash
pip install -r requirements.txt

###### 5.Run Your Chalice Application Locally

bash
chalice local

## Nomoclature
nom des fichiers du repos: **snake_case**

nom des classes : **CamelCase**

nom des attributs/méthodes : **snake_case**

nom des attributs des models/mongo : **CamelCase**

nom des constantes : **SNAKE_CASE tout en majuscule**

