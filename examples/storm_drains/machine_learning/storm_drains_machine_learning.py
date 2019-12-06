#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""
This example shows how to train a random forest classifier to detect storm drains.
This example requires 17.5 Go of RAM to train the model on all training set.
"""

import pathlib
import pickle

from jakarto_datasets.datasets.storm_drains import StormDrainsDataset
from jakarto_datasets.commons.path_manager import get_jakarto_directory

from numpy.lib import recfunctions as rfn
import pptk
import sklearn.ensemble


def select_features_and_labels(pointcloud):
    lidar_data = pointcloud.get_lidar_data()
    extra_lidar_data = pointcloud.get_extra_lidar_data()

    # Merge intensity and geometric features
    features = rfn.merge_arrays((lidar_data, extra_lidar_data), flatten=True)

    labels = pointcloud.get_label_lidar_data()

    return features, labels


def stack_pointclouds(pointcloud_list):
    features_stack = None
    labels_stack = None

    for index, data in enumerate(pointcloud_list):
        print("%d / %d" % (index + 1, len(pointcloud_list)), data)

        features, labels = select_features_and_labels(data)

        if features_stack is None:
            features_stack = features
            labels_stack = labels
        else:
            features_stack = rfn.stack_arrays((features_stack, features))
            labels_stack = rfn.stack_arrays((labels_stack, labels))

    return features_stack, labels_stack


if __name__ == "__main__":
    SAVE_MODEL_FILE = pathlib.Path(get_jakarto_directory()) / 'model_random_forest.save'

    # Load dataset
    storm_drains_2019 = StormDrainsDataset(maximum_cache_size_in_bytes=10_000_000_000)

    # TRAINING PART
    training_set = list(storm_drains_2019.training_set)

    # Select features to learn
    training_features_stack, training_labels_stack = stack_pointclouds(training_set)

    # Train a balanced random forest model
    model = sklearn.ensemble.RandomForestClassifier(n_estimators=100, n_jobs=-1, class_weight="balanced")
    model.fit(rfn.structured_to_unstructured(training_features_stack),
              rfn.structured_to_unstructured(training_labels_stack).ravel())

    # Save the model
    with open(SAVE_MODEL_FILE, mode='wb') as f:
        pickle.dump(model, f)

    # TESTING PART
    testing_set = list(storm_drains_2019.testing_set)

    # Evaluate the model
    testing_features_stack, testing_labels_stack = stack_pointclouds(testing_set)
    score = model.score(rfn.structured_to_unstructured(testing_features_stack),
                        rfn.structured_to_unstructured(testing_labels_stack).ravel())
    print("Score on testing set : %f" % score)

    # Visualize prediction
    for index, data in enumerate(testing_set):
        saved_coordinates = data.get_saved_coordinates_data()

        features, labels = select_features_and_labels(data)

        predictions = model.predict(rfn.structured_to_unstructured(features))

        # Init 3d viewers
        v = pptk.viewer([0, 0, 0])

        # Update 3d viewer
        v.attributes()
        v.load(rfn.structured_to_unstructured(saved_coordinates))  # pptk viewer failed with real coordinates
        v.attributes(labels, predictions, data.get_lidar_data()['intensity'])

        input('(%d / %d) press Enter to continue' % (index + 1, len(testing_set)))
        v.close()
