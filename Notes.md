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

## Postgresql 

If we want to add a Postgresql service, we can create with the following info

```
  db:                                           # Service database
    image: postgres-10-alpine                   # Imagen postgres light (alphone)
    environment:                                # The following has the database connection information
      - POSTGRES_DB=app
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=supersecretpassword
```

We need to add the database information connection to our app service

```
version: '3'
services:
 app: 
   ...
   environment:
    - DB_HOST=db                                 # Database host is our dababase instance
    - DB_NAME=app
    - DB_USER=postgres
    - DB_PASS=supersecretpassword
  depends_on:                                    # Database must begin first and persist to work with app
    - db 
```

Our project must read the environment variants using `settings.py`

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}
```

Also, add the installation on `requirements.py`

```
psycopg2>=2.7.5,<2.8.0
```

And also, django dockerfile will need to install the postgresql client to consult database. Also, it will require to install other dependencies.

```
# Install dependencies
COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps
```

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

## Test Case

Into our test class we can find the following

 - setUp function: This function starts before all our test. In this function, we can generate the initial values for our testings.

 - Testing functions: The test function must begin with `test_`. We execute the required code and finally, we will check the comparisons to define than the test is passed or failed. These are the available comparisons.
   - `self.assertEqual(A, B)`. A is equals to B
   - `self.assertTrue(A)`: A equals true
   - `self.assertRaises(Error)`: It must be on a with statement. If the code generates an `Error`, passed
   - `self.assertContains(A, B)`: B is contained on A. Also, A must have a 200 OK status.

## TDD methodology

When you code with this methodology, you need to create the testing functions firsts. When the test failed, you need to code the minimal to pass the test.

 1) Code testing
 2) Run test and check with testing failed
 3) Code to solve failed test
 4) Check again steps 2 and 3 until there isn't failed test

 ## Fine tunning

 Every app than we create, we will delete "test.py" file than generate.

 We will create a folder named "test" and it will have a file called "__init__.py". The objective is to create tests in direrent files.

 ## Mocking

Mocking is when you override the behavior of your dependencies of the code than tou are testing. We use mocking to avoid any unintended side effects and also to isolate the specific piece of code that we want to test.

We don't have to depende our test from external resources. An example is to tests a send email function. We won't be sending real emails on testings. We only need to check than the function receives the correct paramenters.

To implement mock, we need to import `patch` from `unittest.mock`.

 # Miscelaneous

 ## Reverse

Importing reverse from django.urls, we can manage urls direcly on our code using names instead of direct URL's.

> from django.urls import reverse

We can get a url inserting the name on url as reverse paramenter.

> url = reverse('APP:PAGE')

The name of the admin pages we can find it on the [documentation](https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#reversing-admin-urls).

If we want to check an url with parameters, we need to use the `args` parameter.

> url = reverse('admin:core_user_change', args=[self.user.id])

 ## Client

Importing `Client` from `django.test`, we can generate a virtual client who will be executing actions on our pages.

> from django.test import Client

We can create a client lisk this

> self.client = Client()

Then, force to login it 

> self.client.force_login(USER)

Also, client can accsend a GET request to an url (reverse)

> res = self.client.get(url)

We can check if the request has an status code with the `status_code` value.

> self.assertEqual(res.status_code, 200)

## APIClient

This client is imported from `rest_framework.test` 

> from rest_framework.test import APIClient

Similar to client from `django.test` you can execute http request

> res = self.client.post(URL, payload)

## Status

To compare request status, we need to use `status` object from `rest_framework`.

These are some status to work. You can find all on [this link](https://www.django-rest-framework.org/api-guide/status-codes/).

 - status.HTTP_200_OK
 - status.HTTP_400_BAD_REQUEST
 - status.HTTP_201_CREATED


## Modify admin view

On `admin.py` we usually add the following line to add a model on the admin site

> admin.site.register(models.User)

But the admin will show a default view. So, if we want to assign a different view, we need to difine it as a second parameter.

> admin.site.register(models.User, UserAdmin)

To create the new view, we need to create it importing `UserAdmin` from `django.contrib.auth.admin`. Into the class, we can define some parameters like
 - `ordering` of the registers
 - `list_displays` on the general display
 - `fieldsets`: The fields containing on a tuple. It's a set of subsets, every subset ha a section name and a dictionary with the fields required.
 - `add_fields`: The fields required to add an user. It requires as `fieldsets` a set of sebsets. The subsets must have a name and a dictionary with the fields and classes to visualizing (we usually assign `wide` class as default)

```
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            )}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
            }),
            )
    
```

It's a best practice thant titles passed on a translation importing `gettext` from `django.utils.translation`. We can declare it calling as `_`

> from django.utils.translation import gettext as _

## Commands

On the backend, we need to execute some process to manage our projects. These process must be on a `management` folder on our applications. Also, it will have a `__init__.py` file. Then, into the `management` folder, we will create another folder called `commands`. This folder will also have the `__init__.py` file.

The commands than we create, we can execute with `python manage.py NEW_COMMAND` 

Coding the new command, it must be a class inherit from `BaseCommand` (from django.core.management.base import BaseCommand). The body of the command will be into a `handle` function (def handle(self, *args, **options)).

## Generics

We can create a APIView than give us all the http´methods, or we can only define a segmented APIView for one action.

This is using `generics` from `rest_framework`.

We can create a APIView only inherit the class with the action required (we can check the generics classes available [here](https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes)).

 - generics.CreateAPIView for only creation
 - generics.ListAPIView for only listing

## URL's

On main project, we need to point the app's url.

```
urlpatterns = [
    ....
    path('api_project/app_url/', include('app.urls'))
]

```

On app url, se specify whe name of app for the reverse funcction,. Also the name of every class view on the urlpatterns.

```
app_name = 'api_name'

urlpatterns = [
    path('function/', views.Function.as_view(), name='function_name'), #reverse name will be "api_name.function_name"
]
```

## Viewset and Mixins

In case tahn we want to create a viewsets than manage two or more HTTP methods, instead to creeate one by one, we can create a class inherit from `viewsets.GenericViewSet` and also inherit from `, mixins.x`, where x is the required method (you can check the [here](https://www.django-rest-framework.org/api-guide/generic-views/#mixins), also, you can check an example [here](https://www.django-rest-framework.org/api-guide/viewsets/#custom-viewset-base-classes)).

```
from rest_framework import viewsets, mixins


class MyViewSet(
  viewsets.GenericViewSet,
  mixins.ListModelMixin,
  CreateModelMixin):
  """Viewset to only list and create"""
  pass

```

## URL's for mixings

To generate url's for mixings, it's neccesary to create a router on url's file.

```
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views

app_name = 'my_app'

router = DefaultRouter()
router.register('my_view', views.TagView)

urlpatterns = [
    path('', include(router.urls))
]
```

For this case, you will have the url's with the following reverse syntax:

> my_app:my_view:my_methods

The methods allowed are the same on the inherited mixins. You can check the reverse methods [here](https://www.django-rest-framework.org/api-guide/routers/#simplerouter).

## Many to many serializers

In case to display serializers with many to many attributes, we can try two ways.

1) `PrimaryKeyRelatedField`. Imported from serializers, this kind of gield will only return the id's of every element on the serializer.

2) `Serializer(many=True, read_only=True)`: A filed will be called as a previously serializer created. The element will show the fields on the previous serializer.

## Self.action

If we want to change any parameter depending of action (get, post, etc), we can select it with the ``self.action` operator.

```
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        return self.serializer_class
```

The existing actions can be found [here](https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions).