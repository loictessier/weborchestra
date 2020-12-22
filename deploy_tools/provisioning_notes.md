Provisioning a new site
=======================

## Required packages:

* nginx
* supervisor
* Python 3.8
* virtualenv + pip
* Git

eg, on Ubuntu

    sudo apt update
    sudo apt-get install nginx supervisor git python3.8 python3.8-venv
    sudo apt-get install python3-pip

## .env file

* see .env.template
* copy the file to the root of the project and rename it to .env
* complete all the value with environment secret values

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com
* replace USER with server super user

## Supervisor service

* see gunicorn-supervisor.template.conf
* replace SITENAME with, e.g., staging.my-domain.com
* replace USER with server super user

## Folder structure

Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
        ├── database
        ├── source
        ├── static
        └── virtualenv