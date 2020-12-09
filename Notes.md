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
