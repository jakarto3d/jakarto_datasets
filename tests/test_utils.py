#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import pytest

import urllib.request
import os

from jakarto_datasets.utils.data_structure_operator import split_list
from jakarto_datasets.utils.memory_manager import humansize
from jakarto_datasets.utils.downloader import download_dataset, get_filename_from_url


def test_split_list():
    train_list, test_list = split_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], split_threshold=0.7)
    assert train_list == [1, 2, 3, 4, 5, 6, 7]
    assert test_list == [8, 9, 10]


def test_split_threshold():
    with pytest.raises(ValueError):
        _ = split_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], split_threshold=2)


def test_humanize():
    assert humansize(2_000_000_000) == '1.86 GB'


def test_downloader_exception(tmpdir, monkeypatch):
    def mockreturn_access(url, filename=None, reporthook=None, data=None):
        with open(filename, 'w') as f:
            f.write('test')

        assert os.listdir(tmpdir) == ['mini_jakarto_storm_drains_2019.zip']
        raise Exception()

    monkeypatch.setattr(urllib.request, 'urlretrieve', mockreturn_access)

    with pytest.raises(Exception):
        download_dataset(url="https://storage.googleapis.com/jakarto_opendata/datasets/mini_jakarto_storm_drains_2019.zip", destination_directory=tmpdir)

    assert os.listdir(tmpdir) == []
