# omnihr-assignment

OmniHR Assignment

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users


- To create a **superuser account**, use this command:

      $ make createsuperuser


### Running unit test

To run the tests:

    $ make test



### Start development 
To run the development:

    $ make dev

To run the development and rebuild image:
    
    $ make dev.build

To make migrations:

    $ make migrations

To apply migrate:

    $ make migrate

To load initial data:
    
    $ make loaddata
