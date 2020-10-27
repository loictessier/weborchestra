Provisioning a new site
=======================

## Required packages:

* nginx
* supervisor
* Python 3.8
* virtualenv + pip
* Git
* sentry_sdk

eg, on Ubuntu

    sudo apt update
    sudo apt-get install nginx supervisor git python3.8 python3.8-venv
    sudo apt-get install python3-pip

## Django server settings module 

* see django-settings.template.py (should already be at weborchestra/settings/{settings_name}.py after fab deploy)
* replace email, database and sentry placeholders with server values

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com
* replace USER with server super user

## Supervisor service

* see gunicorn-supervisor.template.conf
* replace SITENAME with, e.g., staging.my-domain.com
* replace USER with server super user
* replace SETTINGS_NAME with, e.g., {settings_name} (depending on how you named the django settings module)

## Folder structure

Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
        ├── database
        ├── source
        ├── static
        └── virtualenv