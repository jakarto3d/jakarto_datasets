# Jakarto datasets for 3d detection challenge of urban assets

We built that python API to share some real-world 3d lidar datasets of urban assets. We hope to help some of you to develop and test algorithms about 3d lidar processing.


![jakarto car detection](https://raw.githubusercontent.com/jakarto3d/jakarto_datasets/master/doc/images/jakarto_car_detection.png)

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
        author = {Loic Messal and Cedric Pelletier and {Jakarto Cartographie 3d team}},
        title = {Jakarto datasets},
        year = {2019},
        howpublished={\url{https://github.com/jakarto3d/jakarto_datasets}}
    }

A github star may also help.

## Contact
If you want to email us, please send an email to contact@jakarto.com.

## License
This project is licensed under the terms of the MIT license. (see LICENSE.txt file for details).
