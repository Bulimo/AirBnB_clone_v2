#!/usr/bin/python3
""" 2-do_deploy_web_static """
from fabric.api import env, local, put, run, runs_once
from datetime import datetime
import os

# setting the web-01 and web-02 ip addresses
env.hosts = ['18.204.6.232', '3.86.13.144']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


@runs_once
def do_pack():
    """
    generates a.tgz archive from the contents of the web_static folder
    """

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
        print("New version deployed!")
        return True
    except Exception:
        return False
