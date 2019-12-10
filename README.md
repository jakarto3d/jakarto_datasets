# Jakarto datasets for 3d detection challenge of urban assets

[![Build Status](https://travis-ci.org/jakarto3d/jakarto_datasets.svg?branch=master)](https://travis-ci.org/jakarto3d/jakarto_datasets) [![Code coverage](https://codecov.io/gh/jakarto3d/jakarto_datasets/branch/master/graph/badge.svg)](https://codecov.io/gh/jakarto3d/jakarto_datasets) [![License](https://img.shields.io/github/license/jakarto3d/jakarto_datasets)](https://github.com/jakarto3d/jakarto_datasets/blob/master/LICENSE.txt) 
[![PyPI version](https://badge.fury.io/py/jakarto-datasets.svg)](https://badge.fury.io/py/jakarto-datasets) [![GitHub stars](https://img.shields.io/github/stars/jakarto3d/jakarto_datasets.svg?style=flat&label=github&nbsp;stars&nbsp;&starf;)](https://GitHub.com/jakarto3d/jakarto_datasets/stargazers/)


We built that python API to share some real-world 3d lidar datasets of urban assets. We hope to help some of you to develop and test algorithms about 3d lidar processing.


![jakarto car detection](https://raw.githubusercontent.com/jakarto3d/jakarto_datasets/master/doc/images/jakarto_car_detection.png)
![jakarto urban object detection](https://raw.githubusercontent.com/jakarto3d/jakarto_datasets/master/doc/images/jakarto_urban_object_detection.png)

Those datasets have been gathered with the [Jakarto](https://www.jakarto.com) truck.
![jakarto truck](https://raw.githubusercontent.com/jakarto3d/jakarto_datasets/master/doc/images/camion_jakarto.jpg)


## Installation
This API requires `python 3.6+`.

```sh
pip install jakarto-datasets
```

## Usage
```python
from jakarto_datasets.datasets.storm_drains import StormDrainsDataset

# Load dataset
storm_drains_2019 = StormDrainsDataset()

for data in storm_drains_2019.training_set:
    coordinates = data.get_coordinates_data()
    lidar_data = data.get_lidar_data()
    
    label = data.get_label_lidar_data()
    
    print(data)
    print(coordinates.shape)
    print(lidar_data.shape)
    print(label.shape)
    
    print(lidar_data['intensity'])
```


## Datasets

| datasets | year | 3d lidar | label | raster | mask | `len(training_set)` | `len(testing_set)` | examples | description |
| --- | --- | --- | --- | --- | --- | --- | --- | ---| --- |
| storm drains | 2019 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:  | :heavy_check_mark: | 223 | 150 | [see examples](examples/storm_drains/README.md) | [see details](examples/storm_drains/README.md) |


## Benchmarks

We will be more than happy to share your experiments.

| datasets | title | authors | links | description |
| -- | -- | --  | -- | -- |
| storm drains 2019 | balanced random forest | Jakarto team  | [link](examples/storm_drains/machine_learning/storm_drains_machine_learning.py) | Use a deadly simple balanced random forest to classify each point from lidar data. Although it doesn't use spatial information, it allowed Jakarto to detect ~25% of storm drains. Those storm drains will be added to the Jakarto storm drains 2020 dataset. |
|...                | ...                    | ...           | ...                                                                     |             |


## Citation

If you find this work useful and wish to refer to, please consider the following BibTeX entry:

    @MISC{jakarto_datasets,
        author = {Loic Messal and Cedric Pelletier},
        title = {Jakarto datasets},
        year = {2019},
        howpublished={\url{https://github.com/jakarto3d/jakarto_datasets}}
    }

A github star may also help.

## Contact
If you want to email us, please send an email to contact@jakarto.com.

## License
This project is licensed under the terms of the MIT license. (see LICENSE.txt file for details).
