Test Driven Development
=======================

On the course, we can look some proposed test to check on the development.

Some of these test are

# Models

1) Test to create objects on model and check if exists
2) To check if exists, we can compare `__str__` function with a slug element of the model.

# Admin

1) Check if a user can be created
2) Check if a reverse admin url can get a `HTTP_200_OK` on creating, update and list.

# Commands

Check if a command can be executed (it's recommended to count tries and sustitute some actions with mocks)

# Views

1) Check if a viewset can be shown on public
2) Check if a viewset can be only shown with login (it's recommendated to force login)
    2.1) Test listing of viewset comparing serialized values vs res.data values
    2.2) Check if viewset only returns the elements of an user
    2.3) Check valid creations
    2.4) Check invalid creations (it returns `HTTP_400_BAD_REQUEST`)
    2.5) Check creation with field with many-to-many elements
    2.6) Check updating views
    2.7) Check partial updating views.