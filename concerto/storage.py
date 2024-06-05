import os
from shutil import rmtree

from appdirs import user_data_dir

dir_name = user_data_dir('concerto')

dir_name = os.getenv('CONCERTO_PATH', dir_name)

id_mapping_dir = os.path.join(dir_name, 'id_data')


def create_storage_structure():
    # check or create the main data storage directory
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # check or create the id mapping data storage directory
    if not os.path.exists(id_mapping_dir):
        os.makedirs(id_mapping_dir)


def clear_cached_dbs():
    """Remove old database cached downloads"""
    # check or create the main data storage directory
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    # check or create the network data storage directory
    if os.path.exists(id_mapping_dir):
        rmtree(id_mapping_dir)


create_storage_structure()
