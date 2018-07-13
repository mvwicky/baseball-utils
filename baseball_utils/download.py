"""Download retrosheet/gameday files"""
import os
from typing import Text, Optional, List
from zipfile import ZipFile

import requests

from .const import Retrosheet
from .types import Path


def retrosheet_event_zip(
    year: int, out_dir: Path, force: bool = False, verbose: bool = False
) -> Optional[Path]:
    """Download a yearly event zip file
    Assumes the output directory exists
    """
    url = Retrosheet.event_url(year)
    out_file = os.path.join(out_dir, '{0}eve.zip'.format(year))
    if os.path.isfile(out_file) and os.path.getsize(out_file) and not force:
        if verbose:
            print('{0} already exists, skipping'.format(out_file))
        return out_file

    print(url)
    res = requests.get(url, stream=True)
    if res.status_code != requests.codes.ok:
        if verbose:
            print('Failed on {0} with code {1}'.format(url, res.status_code))
        return None

    with open(out_file, 'wb') as f:
        for chunk in res.iter_content():
            f.write(chunk)

    return out_file


def retrosheet_unzip(
    in_file: Path, out_dir: Path, force: bool = False, verbose: bool = False
) -> Optional[Path]:
    year = os.path.split(os.path.splitext(in_file)[0])[1]
    out_path = os.path.join(out_dir, year)
    if os.path.isdir(out_path) and os.listdir(out_path) and not force:
        if verbose:
            print('{0} already exists, skipping'.format(out_path))
        return out_path

    if not os.path.isdir(out_path):
        os.makedirs(out_path)
    with ZipFile(in_file) as z:
        z.extractall(out_path)
    return out_path


def retrosheet_seasons(
    retro_dir: Text,
    zip_dir: Text,
    data_dir: Text,
    force: bool = False,
    verbose: bool = False,
) -> List[Path]:
    # retro_dir = os.path.join('f:\\local_scratch', 'retrosheet')
    if not os.path.isdir(retro_dir):
        os.makedirs(retro_dir)

    # zip_dir = os.path.join(retro_dir, 'events', 'raw')
    if not os.path.isdir(zip_dir):
        os.makedirs(zip_dir)

    eve_zips = []
    for year in Retrosheet.years:
        p = retrosheet_event_zip(year, zip_dir)
        if p is not None:
            if verbose:
                print('{0} ({1:,})'.format(p, os.path.getsize(p)))
            eve_zips.append(p)

    # data_dir = os.path.join(retro_dir, 'events', 'data')
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    eve_dirs = []
    for file in eve_zips:
        o = retrosheet_unzip(file, data_dir)
        if o is not None:
            if verbose:
                print('{0} ({1} files)'.format(o, len(os.listdir(o))))
            eve_dirs.append(o)
    return eve_dirs


if __name__ == '__main__':
    pass
