#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import pathlib

from jakarto_datasets.commons import path_manager
from jakarto_datasets.utils import archive_manager
from jakarto_datasets.utils import data_structure_operator
from jakarto_datasets.utils import downloader
from jakarto_datasets.utils import memory_manager

import numpy as np
import numpy.lib.recfunctions

import imageio
import laspy


class StormDrainsManager(object):
    def __init__(self, files_to_load, maximum_cache_size_in_bytes=2_000_000_000):
        self._files_to_load = files_to_load
        self._maximum_cache_size_in_bytes = maximum_cache_size_in_bytes

        self._cache = {}
        self._memory_cache_in_use = 0

    def __len__(self):
        return len(self._files_to_load)

    def __getitem__(self, index):
        if index in self._cache:
            storm_drain_file = self._cache[index]
        else:
            storm_drain_file = StormDrainFile(self._files_to_load[index])

            memory = memory_manager.get_size(storm_drain_file)
            if (self._memory_cache_in_use + memory) < self._maximum_cache_size_in_bytes:
                self._memory_cache_in_use += memory
                self._cache[index] = storm_drain_file

        return storm_drain_file


class StormDrainFile(object):
    def __init__(self, path):
        self._manage_path(path)
        self._load_data()

    def _manage_path(self, path):
        self._pointcloud_path = path
        self._filename = pathlib.Path(self._pointcloud_path).stem

        self._dataset_root_path = (self._pointcloud_path / '..' / '..' / '..').resolve()
        self._dataset_pointcloud_folder_path = (self._dataset_root_path / 'pointclouds').resolve()
        self._relative_path = self._pointcloud_path.parent.relative_to(self._dataset_pointcloud_folder_path)

        self._mask_path = self._dataset_root_path / 'images' / 'masks' / self._relative_path / (self._filename + '_mask.png')
        self._raster_path = self._dataset_root_path / 'images' / 'rasters' / self._relative_path / (self._filename + '.png')

    def is_storm_drain(self):
        if self._mask_path.exists():
            return True
        return False

    def _load_data(self):
        self._load_raster_data()
        self._load_mask_data()
        self._load_lidar_data()

    def _load_lidar_data(self):
        las_file = laspy.file.File(self._pointcloud_path, mode="r")

        x = np.copy(las_file.x)
        y = np.copy(las_file.y)
        z = np.copy(las_file.z)

        points = las_file.points['point']

        # Extract only scaled coordinates (real coordinates)
        self._coordinates_data = np.rec.fromarrays([x, y, z], dtype=[('x', x.dtype), ('y', y.dtype), ('z', z.dtype)])

        # Extract only the raw integer coordinates stored in las file (integers).
        # See the note in the Reading Data section of https://laspy.readthedocs.io/en/latest/tut_part_1.html
        self._saved_coordinates_data = np.copy(points[['X', 'Y', 'Z']])

        # Extract only intensity and gps_time column
        self._lidar_data = np.copy(points[['intensity', 'gps_time']])

        # Extract only annotation label
        label = np.copy(points['puisard'])
        self._label_lidar_data = np.rec.fromarrays([label], dtype=[('label', label.dtype)])

        # Extract other dimensions
        self._extra_lidar_data = np.copy(points)
        self._extra_lidar_data = numpy.lib.recfunctions.drop_fields(self._extra_lidar_data, ['X', 'Y', 'Z', 'gps_time', 'intensity', 'puisard'])

        las_file.close()

    def _load_mask_data(self):
        if self.is_storm_drain():
            mask = imageio.imread(self._mask_path)
        else:
            mask = np.zeros(self._raster_data.shape)
            mask[:, :, 3] = 1  # Set transparency to 1
        self._mask_data = mask

    def _load_raster_data(self):
        if self._raster_path.exists():
            raster = imageio.imread(self._raster_path)
        else:
            raise FileNotFoundError("This image does not exist : %s" % self._raster_path)
        self._raster_data = raster

    def get_lidar_data(self):
        return self._lidar_data

    def get_coordinates_data(self):
        return self._coordinates_data

    def get_saved_coordinates_data(self):
        return self._saved_coordinates_data

    def get_extra_lidar_data(self):
        return self._extra_lidar_data

    def get_label_lidar_data(self):
        return self._label_lidar_data

    def get_raster(self):
        return self._raster_data

    def get_mask(self):
        return self._mask_data

    def __repr__(self):
        return (self._relative_path / self._filename).as_posix()


_DATASET_URL = "https://storage.googleapis.com/jakarto_opendata/datasets/jakarto_storm_drains_2019.zip"


class StormDrainsDataset(object):
    def __init__(self, root_directory=None, url=_DATASET_URL, split_train_test_threshold=0.6, maximum_cache_size_in_bytes=2_000_000_000):
        self._SPLIT_TRAIN_TEST_THRESHOLD = split_train_test_threshold

        self._url = url
        self._maximum_cache_size_in_bytes = maximum_cache_size_in_bytes

        self._retrieve_dataset(root_directory)
        self._prepare_train_test_set()

    def _retrieve_dataset(self, root_directory=None):
        dataset_directory = path_manager.get_dataset_directory(root_directory)
        destination_download = downloader.download_dataset(self._url, dataset_directory)
        local_dataset_folder = archive_manager.unzip_dataset(destination_download, dataset_directory)

        self._local_dataset_folder = local_dataset_folder

    def _prepare_train_test_set(self):
        pointclouds_which_contain_storm_drains = list((pathlib.Path(self._local_dataset_folder) / 'pointclouds').glob('positive_storm_drains/*.las'))
        pointclouds_which_do_not_contain_storm_drains = list((pathlib.Path(self._local_dataset_folder) / 'pointclouds').glob('negative_storm_drains/*.las'))

        pointclouds_which_contain_storm_drains_for_training, pointclouds_which_contain_storm_drains_for_testing = data_structure_operator.split_list(pointclouds_which_contain_storm_drains, split_threshold=self._SPLIT_TRAIN_TEST_THRESHOLD)
        pointclouds_which_do_not_contain_storm_drains_for_training, pointclouds_which_do_not_contain_storm_drains_for_testing = data_structure_operator.split_list(pointclouds_which_do_not_contain_storm_drains, split_threshold=self._SPLIT_TRAIN_TEST_THRESHOLD)

        training_set = pointclouds_which_contain_storm_drains_for_training + pointclouds_which_do_not_contain_storm_drains_for_training
        testing_set = pointclouds_which_contain_storm_drains_for_testing + pointclouds_which_do_not_contain_storm_drains_for_testing

        self.training_set = StormDrainsManager(training_set, maximum_cache_size_in_bytes=self._maximum_cache_size_in_bytes)
        self.testing_set = StormDrainsManager(testing_set, maximum_cache_size_in_bytes=self._maximum_cache_size_in_bytes)
