# Storm drains dataset

## pointclouds
This dataset contains 373 HD 3d lidar pointclouds. Each pointcloud is a 2mx2m tile.

Among those pointclouds, 182 contains at least one storm drain and 191 none.

![3d lidar](/doc/images/storm_drains/storm_drains_lidar.png)

Those pointclouds are split into a training set (223 pointclouds) and a testing set (150 pointclouds).

### features and labels
Each point has the following properties:
- `x, y, z` 3d coordinates in EPSG:2950
- `intensity` of the signal from the lidar sensor
- `label` which has the value `1` if that point belongs to a storm drain (`0` otherwise).
- some computed geometric features given its neighborhood:
  The neighborhood is computed as a sphere of ray `r` which can be 3cm, 5cm, 10cm or 20cm. The geometric feature will be prefixed with `__0_03` for the sphere of 3cm, `__0_05` for the sphere of 5cm, etc...
  - `nb_neighbors`
  - `pca1`
  - `pca2`
  - `anisotropy`
  - `eigen_entropy`
  - `eigenvalue_sum`
  - `linearity`
  - `nx`
  - `ny`
  - `nz`
  - `omnivariance`
  - `planarity`
  - `sphericity`
  - `surface_variation`
  - `verticality`

  Those geometric features are described in the following references :
    - Brodu, N., & Lague, D. (2012). 3D terrestrial lidar data classification of complex natural scenes using a multi-scale dimensionality criterion: Applications in geomorphology. ISPRS Journal of Photogrammetry and Remote Sensing, 68, 121-134. [pdf](https://arxiv.org/pdf/1107.0550.pdf)
    - Weinmann, M., Jutzi, B., & Mallet, C. (2017). Geometric features and their relevance for 3d point cloud classification. ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences, 4, 157. [pdf](https://www.isprs-ann-photogramm-remote-sens-spatial-inf-sci.net/IV-1-W1/157/2017/isprs-annals-IV-1-W1-157-2017.pdf)


```python
from jakarto_datasets.datasets.storm_drains import StormDrainsDataset

# Load dataset
storm_drains_2019 = StormDrainsDataset()

for data in storm_drains_2019.training_set:
    coordinates = data.get_coordinates_data()  # x, y, z in EPSG:2950
    lidar_data = data.get_lidar_data()  # intensity, gps_time
    extra_lidar_data = data.get_extra_lidar_data()  # geometric features

    label = data.get_label_lidar_data()  # labels

    print(data)
    print(coordinates.shape)
    print(lidar_data.shape)
    print(extra_lidar_data.shape)
    print(label.shape)
```

## rasters and masks
We also rasterized the lidar pointclouds to benefit of Computer Vision algorithms.
![rasters](/doc/images/storm_drains/raster.png)
![masks](/doc/images/storm_drains/masks.png)


```python
from jakarto_datasets.datasets.storm_drains import StormDrainsDataset

# Load dataset
storm_drains_2019 = StormDrainsDataset()

for data in storm_drains_2019.training_set:
    raster = data.get_raster()
    mask = data.get_mask()

    print(data)
    print(raster.shape)
    print(mask.shape)
```


# Examples
Please refer to the following examples :
- [A simple viewer](viewer/) to loop over the dataset. It allows to visualize the pointcloud, the raster and the mask at the same time.
- [train a machine learning model](machine_learning/) given only intensity and computed geometric features, try to predict the label for each point of pointclouds.
