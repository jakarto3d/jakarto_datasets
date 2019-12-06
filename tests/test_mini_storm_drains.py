#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import pathlib

import pytest


@pytest.fixture
def download_dataset(tmpdir):
    from jakarto_datasets.datasets.storm_drains import StormDrainsDataset

    dataset = StormDrainsDataset(
        root_directory=tmpdir,
        url="https://storage.googleapis.com/jakarto_opendata/datasets/mini_jakarto_storm_drains_2019.zip",
        split_train_test_threshold=1.0
    )
    return dataset


def test_storm_drains_dataset(download_dataset):
    dataset = download_dataset
    assert len(dataset.training_set) == 2
    assert dataset.training_set[0].get_mask().shape == (164, 164)


def test_is_storm_drain(download_dataset):
    dataset = download_dataset
    assert dataset.training_set[0].is_storm_drain() == True
    assert dataset.training_set[1].is_storm_drain() == False

def test_use_of_cache(download_dataset):
    dataset = download_dataset

    def get_memory_in_use_for_training_set(dataset):
        return dataset.training_set._memory_cache_in_use

    initial_memory_in_use = get_memory_in_use_for_training_set(dataset)

    # load first data once
    dataset.training_set[0]
    memory_in_use_after_loading_first_item_once = get_memory_in_use_for_training_set(dataset)

    assert initial_memory_in_use <= memory_in_use_after_loading_first_item_once

    # load first data twice
    dataset.training_set[0]
    memory_in_use_after_loading_first_item_twice = get_memory_in_use_for_training_set(dataset)

    assert memory_in_use_after_loading_first_item_once == memory_in_use_after_loading_first_item_twice


def test_public_interfaces(download_dataset):
    dataset = download_dataset

    data = dataset.training_set[0]

    assert str(data) == 'positive_storm_drains/5068030'

    assert data.is_storm_drain() == True

    assert data.get_lidar_data().shape == (21590,)
    assert data.get_lidar_data().dtype.names == ('intensity', 'gps_time')

    assert data.get_coordinates_data().shape == (21590,)
    assert data.get_coordinates_data().dtype.names == ('x', 'y', 'z')

    assert data.get_saved_coordinates_data().shape == (21590,)

    assert data.get_extra_lidar_data().shape == (21590,)

    assert data.get_label_lidar_data().shape == (21590,)
    assert data.get_label_lidar_data().dtype.names == ('label',)

    assert data.get_raster().shape == (164, 164, 4)
    assert data.get_mask().shape == (164, 164)

def test_file_not_found(tmpdir):
    # create fake file tree
    path = tmpdir.mkdir("pointclouds").mkdir("positive_storm_drains").join("fake.las")


    from jakarto_datasets.datasets.storm_drains.storm_drains import StormDrainFile

    with pytest.raises(FileNotFoundError):
        _ = StormDrainFile(pathlib.Path(path))
