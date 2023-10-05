#!/usr/bin/python3

"""Module 1-pa """
from fabric.api import *
from datetime import datetime
import os


def do_pack():
    """  generates a .tgz archive from the contents of the web_static folder """
    local('mkdir -p versions')

    date = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = 'versions/web_static_{}.tgz'.format(date)

    result = local('tar -cvzf {} web_static'.format(file_name))

    if result.failed:
        return None
    else:
        print("web_static packed: {} -> {}Bytes".format(file_name,
              os.path.getsize(file_name)))
        return file_name
