#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os.path
import urllib.parse
import urllib.request

from tqdm import tqdm


class TqdmUpTo(tqdm):
    # from tqdm documentation
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""
    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize


def get_filename_from_url(url):
    urlsplit_result = urllib.parse.urlsplit(url)
    filename = urlsplit_result.path.split('/')[-1]
    return filename


def download_dataset(url, destination_directory):
    filename = get_filename_from_url(url)
    destination_download = os.path.join(destination_directory, filename)

    if not os.path.exists(destination_download):
        try:
            with TqdmUpTo(unit='B', unit_scale=True, miniters=1, desc="Downloading %s" % filename) as t:
                urllib.request.urlretrieve(url, destination_download, reporthook=t.update_to)
        except (Exception, KeyboardInterrupt):
            if os.path.exists(destination_download):
                os.remove(destination_download)
            raise

    return destination_download
