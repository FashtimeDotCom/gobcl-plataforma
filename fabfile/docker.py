# -*- coding: utf-8 -*-

# standard library
import os
from time import gmtime
from time import strftime

# fabric
from fabric.api import cd
from fabric.api import local
from fabric.api import prompt
from fabric.api import run
from fabric.api import sudo
from fabric.api import task
from fabric.colors import green
from fabric.colors import red


def get_os_env(env_var_str):
    """Get an OS environment variable value or exit if unset"""
    env_var = os.getenv(env_var_str)
    if not env_var:
        print(red('{} must be set'.format(env_var_str)))
        exit()
    return env_var


@task
def docker_exec(container_name, cmd):
    """Execute a command on the specified container"""
    return run(
        'docker exec -it "{}" /bin/sh -c "{}"'.format(container_name, cmd)
    )


@task
def get_db_data(setting=''):
    """Return the given setting for the default database"""
    container_name = get_os_env('GOBCL_DOCKER_CONTAINER_NAME')

    return docker_exec(
        container_name,
        'python -Wi manage.py printdatabasedata {}'.format(setting)
    )


@task
def backup_db():
    """Backup database (postgreSQL)."""
    # get database data
    db_name = get_db_data(setting='NAME')
    db_host = get_db_data(setting='HOST')
    db_user = get_db_data(setting='USER')
    db_port = get_db_data(setting='PORT')

    # dumps folder creation
    dumps_folder = 'db_dumps'
    cmd = 'mkdir -p {}'.format(dumps_folder)
    run(cmd)

    # generate backup file name based on current time
    dump_name = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    dump_name = '{}/{}.dump'.format(dumps_folder, dump_name)

    if db_host and db_user:
        cmd = (
            'pg_dump --host {} --username {} -p {} -Fc "{}" -f "{}" '
            '--no-owner --no-privileges'
        ).format(
            db_host, db_user, db_port, db_name, dump_name
        )
    else:
        cmd = (
            'pg_dump -Fc "{}" -f "{}" --no-owner --no-privileges'
        ).format(
            db_name, dump_name
        )

    run(cmd)


@task
def update_docker_image():
    """Update docker image tag"""
    docker_image = get_os_env('GOBCL_DOCKER_IMAGE')

    image_tag = prompt(green('Type in the image tag: '))

    run('docker pull "{}:{}"'.format(docker_image, image_tag))


@task
def update_host():
    """Update host"""
    backup_db()

    host_path = get_os_env('GOBCL_DOCKER_HOST_PATH')
    container_name = get_os_env('GOBCL_DOCKER_CONTAINER_NAME')

    with cd(host_path):
        print(green('Updating host.'))
        run('git pull')

    print(green('installing yarn packages'))
    docker_exec(container_name, 'yarn install')

    print(green('compress files'))
    docker_exec(container_name, 'python manage.py compress --extension=pug')

    print(green('collecting static files'))
    docker_exec(container_name, 'python manage.py collectstatic --noinput')

    print(green('compiling translations'))
    docker_exec(container_name, 'python manage.py compilemessages')


@task
def migrate_db():
    """Migrate database"""
    container_name = get_os_env('GOBCL_DOCKER_CONTAINER_NAME')

    print(green('migrating database'))
    docker_exec(container_name, 'python manage.py migrate')


@task
def restart_container():
    """Restart docker container"""
    container_name = get_os_env('GOBCL_DOCKER_CONTAINER_NAME')

    print(green('Restarting docker container'))
    run('docker container restart "{}"'.format(container_name))


@task
def restart_nginx():
    """Restart nginx on host"""
    print(green('Restarting nginx on host'))
    sudo('service nginx restart')


@task
def restart():
    """Restart docker container and nginx on host"""
    restart_container()
    restart_nginx()


@task
def build_image():
    """Build a docker image specifying a tag"""
    image_tag = prompt(green('Type in the image tag: '))
    local('docker build -t {}'.format(image_tag))


@task
def push_image():
    """Push the docker image"""
    docker_image = get_os_env('GOBCL_DOCKER_IMAGE')
    image_tag = prompt(green('Type in the image tag: '))

    local('docker push "{}:{}"'.format(docker_image, image_tag))
