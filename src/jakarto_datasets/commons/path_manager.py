#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import os.path
import tempfile


def get_jakarto_directory(jakarto_root_directory=None):
    if jakarto_root_directory is None:
        if 'JAKARTO_HOME' in os.environ:
            jakarto_root_directory = os.environ.get('JAKARTO_HOME')
        else:
            jakarto_root_directory = os.path.join(os.path.expanduser('~'), '.jakarto')

            if not os.path.exists(jakarto_root_directory):
                os.makedirs(jakarto_root_directory)

    jakarto_root_directory = os.path.expanduser(jakarto_root_directory)

    if not os.access(jakarto_root_directory, os.W_OK):
        jakarto_root_directory = os.path.join(tempfile.gettempdir(), '.jakarto')

    if not os.path.exists(jakarto_root_directory):
        os.makedirs(jakarto_root_directory)

    return jakarto_root_directory


def get_dataset_directory(root_directory=None, dataset_subdirectory="datasets"):
    jakarto_root_directory = get_jakarto_directory(root_directory)

    dataset_directory = os.path.join(jakarto_root_directory, dataset_subdirectory)
    if not os.path.exists(dataset_directory):
        os.makedirs(dataset_directory)

    return dataset_directory
