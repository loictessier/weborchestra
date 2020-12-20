from fabric.contrib.files import append, exists
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/loictessier/weborchestra.git'


def deploy_production():
    _deploy(settings_name='production')


def deploy_staging():
    _deploy(settings_name='staging')


def _deploy(settings_name='default'):
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host, settings_name)
    _update_virtualenv(source_folder, settings_name)
    _update_static_files(source_folder)
    _update_database(source_folder, settings_name)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder):
    secret_key_file = source_folder + '/weborchestra/settings/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')


def _update_virtualenv(source_folder, settings_name):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.8 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements/{settings_name}.txt')


def _update_static_files(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )


def _update_database(source_folder, settings_name):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )
    run(
        f"cd {source_folder}"
        f" && DJANGO_SETTINGS_MODULE='weborchestra.settings.{settings_name}'"
        " ../virtualenv/bin/python manage.py migrate --noinput"
    )
