#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import pathlib
import zipfile

import tqdm


def unzip_dataset(dataset_path, destination_folder, force_unzip=False):
    dataset_name = pathlib.Path(dataset_path).name
    unzipped_path = pathlib.Path(destination_folder) / pathlib.Path(dataset_path).stem

    if (not unzipped_path.exists()) or force_unzip:
        with zipfile.ZipFile(dataset_path, 'r') as dataset_zip:
            for member in tqdm.tqdm(dataset_zip.infolist(), unit_scale=True, miniters=1, desc='Extracting %s' % dataset_name):
                dataset_zip.extract(member, destination_folder)

    return unzipped_path.as_posix()
