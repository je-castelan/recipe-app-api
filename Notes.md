Notes
=====

# Creating project

## Github

Although you can create the project locally and push to github, other way is the following:

 - Create project in github
 - On creating, you can assign the .gitignore (Python based) and license file (MIT based) on the beggining
 - Finally, get the git url to execute `git clone` (remember to have associated your SSH key to your github account)

## Docker

Create a `Dockerfile` file with the following information

 - `FROM python:3.7-alpine` : Based on a Linux light image called alpine with Pyhton 3.7 (remember to check [docker hub](https://hub.docker.com) to check all the image available).
 - `MAINTAINER John Doe.`: Optional value which mentions the company or developer who checks this project. New versions masks this as deprecated, so you can try `LABEL AUTHOR John Doe`
 - `ENV PYTHONUNBUFFERED 1`: Environment variable which masks tahan Python doen't work with buffer. So, outputs are being printed.
 - `COPY ./requirements.txt /requirements.txt`: You must have this file created on the same folder. It copies the file to the new container.
 - `RUN pip install -r /requirements.txt`: RUN executes the command described. In this case, it executes the pip install
 - `RUN mkdir /app`: RUN creates a work directory
 - `WORKDIR /app`: WORKDIR defines the described directory as working directoy
 - `COPY ./app/ /app`: COPY copy the files to the destination marked
 - `RUN adduser -D user`: RUN linux command to create new user who only executes applications (security).
 - `USER user`: Container will switch to the new user.

Finally, we create our container

> docker build .

## Docker Compose

It allows to manage easier all the components existing on our project.

It must be created in a YAML file (extension .yml).

```
version: '3'                                           # Version of docker compose to use
services:                                              # Services sections
 app:                                                  # Service name
   build: 
     context: .                                        # Context is find on the same path
   ports:
     - "8000:8000"                                     # Port 8000 host matched to 8000 on the image
   volumes:
     - ./app:/app                                      # Gets the app files to app folder container
   command: >
     sh -c "python manage.py runserver 0.0.0.0:8000"   # Run django project (not show command)
```

Finally, we create the components with the following command

> docker-compose build

## Django project

On app folder, we create our project.

In this case, we can create it directly or create it on our docker-compose

> docker-compose run app sh -c "django-admin.py startproject app ."

## Travis-CI

In this [page](https://travis-ci.org/) we can login with our Github account to sync our push with the testing. Then, click on `+` simbol near to `My Repositories` to add the required projects switching on.

Then, we create a file called `.travis.yml` with the following contain

```
language: python                                                         # Language
python:
  - "3.6"                                                                # Version

services:
  - docker                                                               # Services to use

before_script: pip install docker-compose                                # Use docker compose before to test

script:
  - docker-compose run --rm app sh -c "python manage.py test && flake8"  # Script to test
```

On the case of `flake8`, remember to declare it on `requirements.txt`. Also, we can create a `.flake8` file to define which files we need to ignore with the following syntax. It must be into the app folder

```
[flake8]
exclude =
  migrations,
  __pycache__,
  manage.py,
  settings.py
```

# Test Driven Development

## Testing

Django framework can use testing  when you create a file named `test.py` in any part of the project. It will be runned when you executed `python manage.py test`
On `test.py` you create an object inherit from `TestCase` on `django.test`. On the new class you can create your test functions. The functions must begin with "test"

## TDD methodology

When you code with this methodology, you need to create the testing functions firsts. When the test failed, you need to code the minimal to pass the test.

 1) Code testing
 2) Run test and check with testing failed
 3) Code to solve failed test
 4) Check again steps 2 and 3 until there isn't failed test

 ## Fine tunning

 Every app than we create, we will delete "test.py" file than generate.

 We will create a folder named "test" and it will have a file called "__init__.py". The objective is to create tests in direrent files.