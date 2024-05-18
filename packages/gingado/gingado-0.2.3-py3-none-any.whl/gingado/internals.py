"""Functions intended for library internal use."""
from __future__ import annotations  # Allows forward annotations in Python < 3.10

import io
import os
from pathlib import Path
import re
import time
from zipfile import ZipFile

import pandas as pd
import requests


def get_latest_timestamped_file_path(file_path: str) -> str:
    """Get the latest version of a file, based on the unix timestamp in its name.

    Args:
        file_path: The file path of which to search for a timestamped version of the file

    Raises:
        FileNotFoundError: Raised if no timestamped version of the file can be found.

    Returns:
        The path of an existing timestamped version of the provided path.
    """
    file_no_extension, extension = os.path.splitext(file_path)

    # Regular expression for matching timestamped files in the format:
    # <filename>_<timestamp><extension> e.g. '/foo/bar_12345.baz'
    file_regex = rf'{re.escape(file_no_extension)}_(?P<unix_timestamp>\d+){re.escape(extension)}'

    # Get all files in directory of given file
    files_in_dir = [str(f) for f in Path(file_path).parent.glob('*') if f.is_file()]

    # Find version of requested file with latest timestamp
    latest_file_path = None
    latest_unix_timestamp = -1
    for file_name in files_in_dir:
        match = re.match(file_regex, file_name)

        # No match -> file is not a timestamped version of file_path
        if match is None:
            continue

        unix_timestamp = int(match.group('unix_timestamp'))

        # Unix timestamp is higher -> file is newer
        if unix_timestamp > latest_unix_timestamp:
            latest_file_path = file_name
            latest_unix_timestamp = unix_timestamp

    # Raise error if no timestamped file exists
    if latest_file_path is None:
        raise FileNotFoundError(f"No timestamped file for {file_path}")

    return latest_file_path


def generate_timestamped_file_path(file_path: str, exists_ok: bool = True) -> str:
    """Add a unix timestamp at the end of the filename but before the file extension.
    This function only generates the path name, it does not actually create or modify any files.

    Args:
        file_path: The path to which to add a unix timestamp
        exists_ok: Whether to raise an error if a file already exists at the generated path. Defaults to True.

    Raises:
        FileExistsError: Raised if `exists_ok` is `False` and a file at the path generated by this
            function already exists.

    Returns:
        A path with an added unix timestamp.
    """
    file_no_extension, extension = os.path.splitext(file_path)

    # Get unix timestamp, rounded down to seconds
    unix_timestamp = int(time.time())

    # Add timestamp to file path
    timestamped_file_path = f'{file_no_extension}_{unix_timestamp}{extension}'

    # Raise an exception if the file already exists
    if not exists_ok and os.path.exists(timestamped_file_path):
        raise FileExistsError(f'Timestamped file {timestamped_file_path} already exists')

    return timestamped_file_path


def try_read_cached_csv(filename: str, **kwargs) -> pd.DataFrame | None:
    """Try to read a CSV from cache.

    Args:
        filename: The name of the file (NOT the name of the cache file!).

    Returns:
        The contents of the CSV as a dataframe or None if the file is not found in cache.
    """
    try:
        timestamped_file_path = get_latest_timestamped_file_path(filename)
        df = pd.read_csv(timestamped_file_path, **kwargs)
    except FileNotFoundError:
        # File is not in cache
        df = None

    return df


def download_csv(
    url: str,
    cache_filename: str | None = None,
    zipped_filename: str | None = None,
    timeout: int = 120, **kwargs
) -> pd.DataFrame:
    """Download a CSV and load it into a dataframe.

    Args:
        url: The full HTTP(S) URL of the CSV file.
        cache_filename: The name of the file the downloaded CSV should be cached to. \
            If None, no caching is performed. Defaults to None.
        zipped_filename: If the given file is a zip, this should be set to the file \
            path of the desired CSV in the zip. Defaults to None.
        timeout: The timeout (in seconds) for the HTTP request. Defaults to 120.

    Returns:
        The CSV data as a pandas DataFrame.
    """
    # Get CSV file from URL
    with requests.get(url, timeout=timeout) as response:
        if zipped_filename is not None:
            # CSV file is in a zip, get zip file and extract CSV file in memory
            zip_file_content = response.content
            speeches_zip = ZipFile(io.BytesIO(zip_file_content))
            csv_io = speeches_zip.open(zipped_filename, 'r')
        else:
            # Read CSV file
            # WORKAROUND: File may contain characters not compatible with utf8 encoding. "Fix" them
            # by ignoring them during decode.
            csv_io = io.StringIO(response.content.decode("utf8", errors="ignore"))

        # Read CSV into dataframe
        with csv_io as csv_file:
            df = pd.read_csv(csv_file, **kwargs)

    # Write file to cache
    if cache_filename is not None:
        timestamped_file_path = generate_timestamped_file_path(cache_filename)
        Path(timestamped_file_path).parent.mkdir(exist_ok=True)  # Ensure parent dir exists
        df.to_csv(timestamped_file_path, index=False)

    return df


def verify_cached_csv(file_path: str) -> None:
    """Verify that a given file exists in the cache and can be read as CSV.

    Args:
        file_path: The name of the file (NOT the name of the cache file!)

    Raises:
        RuntimeError: Raised if verification fails.
    """
    try:
        timestamped_file_path = get_latest_timestamped_file_path(file_path)
        verify_df = pd.read_csv(timestamped_file_path)
        assert len(verify_df) > 0, (
            f'Cached CSV at {timestamped_file_path} is empty. '
            'Manually remove the file or replace with correct dataset.'
        )
    except Exception as ex:
        raise RuntimeError('Verification error. See previous exception.') from ex
