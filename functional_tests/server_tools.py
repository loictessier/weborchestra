import os

from fabric.api import run
from fabric.context_managers import settings

super_user = os.environ.get('SERVER_SUPER_USER')
django_settings = os.environ.get('SERVER_DJANGO_SETTINGS_MODULE')


def _get_manage_dot_py(host):
    return f"DJANGO_SETTINGS_MODULE='{django_settings}' ~/sites/{host}/virtualenv/bin/python \
        ~/sites/{host}/source/manage.py"


def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'{super_user}@{host}'):
        run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host, email, password):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'{super_user}@{host}'):
        session_key = run(f'{manage_dot_py} create_session {email} {password}')
        return session_key.strip()


def create_activated_account_on_server(host, email, password):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'{super_user}@{host}'):
        user = run(f'{manage_dot_py} create_account {email} {password}')
        return user
