# gobcl-plataforma

[![Build Status](https://travis-ci.org/e-gob/gobcl-plataforma.svg?branch=master)](https://travis-ci.org/e-gob/gobcl-plataforma)
[![Build Status](https://travis-ci.org/e-gob/gobcl-plataforma.svg?branch=staging)](https://travis-ci.org/e-gob/gobcl-plataforma)
[![Build Status](https://travis-ci.org/e-gob/gobcl-plataforma.svg?branch=testing)](https://travis-ci.org/e-gob/gobcl-plataforma)
[![Build Status](https://travis-ci.org/e-gob/gobcl-plataforma.svg?branch=development)](https://travis-ci.org/e-gob/gobcl-plataforma)

A web application hosted on gob.cl, written in Django 1.11 in Python 3

## Dependencies
This project works with:

* Python >= 3.6
* Python libraries defined in requirements.txt 
* Node >= 8.5
* Node libraries defined in package.json 
* Postgress >= 9.6 
* yarn >= 1.3.2

## Quickstart
If you are using Ubuntu 16.04 or OSX, the script quickstart.sh installs all 
dependencies of the project. It assumes you have yarn installed.

* `./quickstart.sh`

## Start new app
Use the custom app template to create your apps:

    python manage.py startapp --template=project/app_template answers
