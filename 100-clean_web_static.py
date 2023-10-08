#!/usr/bin/python3
"""Module 3-deploy_web_static"""
from fabric.api import env, local, put, run, cd, lcd, sudo
from datetime import datetime
import os

# setting the web-01 and web-02 ip addresses
env.hosts = ['18.204.6.232', '3.86.13.144']
env.user = 'ubuntu'
env.key_filename = 'my_ssh_private_key'

# Flag to track if do_pack has been executed
do_pack_executed = False


def do_pack():
    """
    generates a.tgz archive from the contents of the web_static folder
    """
    global do_pack_executed  # Use the global flag

    # Check if do_pack has already been executed
    if do_pack_executed:
        print("New version already deployed.")
        return None

    # Set the flag to indicate that do_pack is being executed
    do_pack_executed = True

    try:
        local('mkdir -p versions')

        date = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = 'versions/web_static_{}.tgz'.format(date)

        local('tar -cvzf {} web_static'.format(file_name))
        print("web_static packed: {} -> {}Bytes".format(file_name,
              os.path.getsize(file_name)))
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """
    distributes an archive to your web servers, using the function do_deploy
    """
    # returns false if archive_path does not exitst
    if os.path.isfile(archive_path) is False:
        return False

    try:
        # extract filename from a full path
        filename = archive_path.split('/')[-1]
        file_no_ext = filename.split('.')[0]

        # create a path
        path_name = "/data/web_static/releases/{}/".format(file_no_ext)

        # upload the archive to /tmp/directory in web server
        put(archive_path, '/tmp/')

        # place the extracted content in desired folder
        run('mkdir -p {}'.format(path_name))

        # using tar command to extract the uploaded contents
        run('tar -xzf /tmp/{} -C {}'.format(filename, path_name))

        # Delete archive from web server
        run('rm /tmp/{}'.format(filename))

        # safely copy the running files
        run("mv {}web_static/* {}".format(path_name, path_name))
        run('rm -rf {}/web_static'.format(path_name))
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {} /data/web_static/current'
            .format(path_name))
        return True
    except Exception:
        return False


def deploy():
    """Fabric script that creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False

    # Call do_deploy with the new archive path on both servers
    for host in env.hosts:
        env.host_string = host
        if not do_deploy(archive_path):
            return False
    return True


def do_clean(number=0):
    """
    Deletes out-of-date archives and unnecessary folders
    """
    num = int(number)

    if num == 0:
        num = 1
    num += 1

    # delete in local machine
    with lcd('./versions/'):
        local("ls -t | tail -n +{} | xargs rm -rf".format(num))
    # local("cd versions && ls -t | tail -n +{} | xargs rm -rf".
    # format(number))

    # delete in remote server
    with cd('/data/web_static/releases/'):
        sudo("ls -t | tail -n +{} | xargs rm -rf".format(num))
    # path = "/data/web_static/releases"
    # run("cd {} ; ls -t | tail -n +{} | xargs rm -fr".format(path, number))
