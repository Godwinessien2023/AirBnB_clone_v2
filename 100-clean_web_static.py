#!/usr/bin/python3
"""Deploy web static package and clean old archives
"""
from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['34.229.161.60', '54.160.83.121']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/godwin_rsa'


def do_pack():
    """Function to compress directory

    Return: path to archive on success; None on fail
    """
    # Get current time
    now = datetime.now()
    now = now.strftime('%Y%m%d%H%M%S')
    archive_path = 'versions/web_static_' + now + '.tgz'

    # Create archive
    local('mkdir -p versions/')
    result = local('tar -cvzf {} web_static/'.format(archive_path))

    # Check if archiving was successful
    if result.succeeded:
        return archive_path
    return None


def do_deploy(archive_path):
    """Deploy web files to server
    """
    try:
        if not path.exists(archive_path):
            return False

        # upload archive
        put(archive_path, '/tmp/')

        # create target dir
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(timestamp))

        # uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C /data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # remove archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # move contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* /data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.format(timestamp))

        # delete pre-existing sym link
        run('sudo rm -rf /data/web_static/current')

        # re-establish symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'.format(timestamp))
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    # return True on success
    return True


def deploy():
    """Deploy web static
    """
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    return False


def do_clean(number=0):
    """Delete out-of-date archives
    number is the number of the archives, including the most recent, to keep.
    If number is 0 or 1, keep only the most recent version of your archive.
    if number is 2, keep the most recent, and second most recent versions of your archive.
    """
    number = int(number)
    if number <= 1:
        number = 1

    # Local clean
    local_archives = sorted(local('ls -1t versions', capture=True).split())
    archives_to_delete = local_archives[number:]
    for archive in archives_to_delete:
        local('rm versions/{}'.format(archive))

    # Remote clean
    with settings(warn_only=True):
        for host in env.hosts:
            with shell_env(ssh_key=env.key_filename):
                with settings(host_string=host):
                    remote_archives = sorted(run('ls -1t /data/web_static/releases').split())
                    remote_archives = [arc for arc in remote_archives if arc.startswith('web_static_')]
                    archives_to_delete = remote_archives[number:]
                    for archive in archives_to_delete:
                        run('sudo rm -rf /data/web_static/releases/{}'.format(archive))
