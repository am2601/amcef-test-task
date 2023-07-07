# Django Project with Rest API

Project with simple API for list, get, create, change and delete Post.
Implemented with Python Django and Django Rest Framework.
As data storage used PostgreSQL database.

_Version: 0.0.1_

## Overview

Provide an admin and API services for manipulate with Posts.

## Installation

1. Clone the repository:

    ```shell
    git clone git@github.com:am2601/django-test.git
    ```

2. Enter project directory
    ```shell
    cd django-test
    ```

3. Build project
    ```shell
    docker compose build
    ```

4. Run project
    ```shell
    docker compose up
    ```

    Server started at port 8000.

## Getting Started

1. Read the [API docs](http://localhost:8000/api/docs) for usage.
2. Use frontend admin
   1. Exec docker container
      ```shell
      docker compose exec server bash
      ```
   2. Create admin user
      ```shell
      python manage.py createsuperuser
      ```
   3. Log in into [admin](http://localhost:8000/admin)
