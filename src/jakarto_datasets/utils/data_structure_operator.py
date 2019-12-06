#!/usr/bin/env python3
# -*- coding=utf-8 -*-


def split_list(items, split_threshold=0.5):
    """
    Split a list in two sublists. A threshold is given to compute the index of the pivot.

    >>> split_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], split_threshold=0.7)
    ([1, 2, 3, 4, 5, 6, 7], [8, 9, 10])
    """
    if not 0 <= split_threshold <= 1:
        raise ValueError("split threshold should be between 0 and 1.")

    index_to_keep = int(len(items) * split_threshold)

    return items[:index_to_keep], items[index_to_keep:]
