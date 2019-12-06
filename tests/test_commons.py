#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import os.path
import pathlib
import shutil
import tempfile

import pytest

from jakarto_datasets.commons.path_manager import get_jakarto_directory


def test_jakarto_directory_with_env_var(tmpdir, monkeypatch):
    tmpdir_path = pathlib.Path(tmpdir).as_posix()
    monkeypatch.setenv("JAKARTO_HOME", tmpdir_path)

    assert pathlib.Path(get_jakarto_directory()).as_posix() == tmpdir_path


def test_jakarto_directory_with_user_var(tmpdir, monkeypatch):
    tmpdir_path = pathlib.Path(tmpdir).as_posix()

    def mockreturn(path):
        return tmpdir_path

    monkeypatch.setattr(os.path, 'expanduser', mockreturn)
    assert pathlib.Path(get_jakarto_directory()).as_posix() == tmpdir_path


def test_jakarto_directory_with_no_write_access(tmpdir, monkeypatch):
    tmpdir_path = pathlib.Path(tmpdir).as_posix()

    def mockreturn(path):
        return tmpdir_path

    monkeypatch.setattr(os.path, 'expanduser', mockreturn)

    def mockreturn_access(*args, **kwargs):
        return False

    monkeypatch.setattr(os, 'access', mockreturn_access)

    assert pathlib.Path(get_jakarto_directory()).as_posix() != tmpdir_path


def test_jakarto_directory_with_temp_file(tmpdir, monkeypatch):
    tmpdir_path = pathlib.Path(tmpdir).as_posix()

    # Force recreation of .jakarto folder
    jakarto_path = pathlib.Path(tmpdir_path) / '.jakarto'
    if jakarto_path.exists():
        shutil.rmtree(jakarto_path)

    def mockreturn_access(*args, **kwargs):
        return False
    monkeypatch.setattr(os, 'access', mockreturn_access)

    def mockreturn_gettempdir():
        return tmpdir_path
    monkeypatch.setattr(tempfile, 'gettempdir', mockreturn_gettempdir)

    assert pathlib.Path(get_jakarto_directory()).as_posix() == jakarto_path.as_posix()
