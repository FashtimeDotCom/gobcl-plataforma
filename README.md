# plataforma-gobcl
[![Build Status](https://travis-ci.org/e-gob/plataforma-gobcl.svg?branch=development)](https://travis-ci.org/e-gob/plataforma-gobcl)

A web application hosted on gob.cl, written in Django 1.11 in Python 3

## Dependencies
This project works with:

* Python >= 3.6
* Python libraries defined in requirements.txt 
* Node >= 8.5
* Node libraries defined in package.json 
* Postgress >= 9.6 

## Quickstart
If you are using Ubuntu 16.04 or OSX, the script quickstart.sh installs all 
dependencies of the project. It assumes you have npm installed.

* `./quickstart.sh`

## Start new app
Use the custom app template to create your apps:

    python manage.py startapp --template=project/app_template answers
