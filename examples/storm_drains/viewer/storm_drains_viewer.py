import numpy as np
from numpy.lib import recfunctions as rfn

from jakarto_datasets.datasets.storm_drains import StormDrainsDataset

import matplotlib.pyplot as plt
import pptk

fake_image_to_init_plt = np.array([[0, 0, 0], [2, 2, 2], [3, 3, 3]])

# Load dataset
storm_drains_2019 = StormDrainsDataset()

# Access data sets
print("#items in training set : %d" % len(storm_drains_2019.training_set))
print("#items in testing set : %d" % len(storm_drains_2019.testing_set))


for index, data in enumerate(storm_drains_2019.testing_set):
    print("loading (%d/%d) : %s" % (index + 1, len(storm_drains_2019.training_set), data))

    # Get data
    real_coordinates = data.get_coordinates_data()
    saved_coordinates = data.get_saved_coordinates_data()

    lidar_data = data.get_lidar_data()
    extra_lidar_data = data.get_extra_lidar_data()
    label = data.get_label_lidar_data()

    raster = data.get_raster()
    mask = data.get_mask()

    # Init 3d viewers
    v = pptk.viewer([0, 0, 0])

    # Update 3d viewer
    v.attributes()
    v.load(rfn.structured_to_unstructured(saved_coordinates))  # pptk viewer failed with real coordinates
    v.attributes(label, lidar_data['intensity'], *[extra_lidar_data[item] for item in extra_lidar_data.dtype.names if item.startswith('omnivariance')])

    # Prepare 2d viewer
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(5, 3))
    raster_axis = axes[0, 0]
    raster_axis.set_title('Raster')
    raster_layout = raster_axis.imshow(fake_image_to_init_plt)
    mask_axis = axes[0, 1]
    mask_axis.set_title('Mask')
    mask_layout = mask_axis.imshow(fake_image_to_init_plt)
    intensity_axis = axes[1, 0]
    intensity_axis.set_title('Histogram of intensity')
    omnivariance_axis = axes[1, 1]
    omnivariance_axis.set_title('Histogram of omnivariance computed for 10cm sphere')

    # Update 2d viewer
    raster_layout.set_data(raster)
    mask_layout.set_data(mask)
    intensity_axis.hist(lidar_data['intensity'])
    omnivariance_axis.hist(extra_lidar_data['omnivariance__0_1'])
    plt.tight_layout()
    plt.draw()

    print('press q to continue')
    plt.show()
    v.close()
