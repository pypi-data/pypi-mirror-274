import os
import pathlib
from glob import glob
from typing import Any

from yaml import YAMLError

from content_manager.fs import (load_object_from_yaml, load_sample_from_csv,
                                save_object_as_yaml, validate_jinja_filename,
                                validate_yaml_filename)

USER_HOME_DIR = pathlib.Path.home().absolute()
CONTENT_BASE_DIR = os.path.join(USER_HOME_DIR, '.eventum', 'content')

TIME_PATTERNS_DIR = os.path.join(CONTENT_BASE_DIR, 'time_patterns')
CSV_SAMPLES_DIR = os.path.join(CONTENT_BASE_DIR, 'samples')
EVENT_TEMPLATES_DIR = os.path.join(CONTENT_BASE_DIR, 'templates')
APPLICATION_CONFIGS_DIR = os.path.join(CONTENT_BASE_DIR, 'configs')


# For read functions we should initialize structure.
# Creation of subdirectories in save functions is handled on their own.
for dir in [
    TIME_PATTERNS_DIR, CSV_SAMPLES_DIR,
    EVENT_TEMPLATES_DIR, APPLICATION_CONFIGS_DIR
]:
    os.makedirs(dir, exist_ok=True)


class ContentManagementError(Exception):
    """Base exception for all content manipulation errors."""


def get_time_pattern_filenames() -> list[str]:
    """Get all relative paths of currently existing time patterns in
    content directory. Paths are relative to time patterns directory.
    """
    return glob(
        pathname='**/*.y*ml',
        root_dir=TIME_PATTERNS_DIR,
        recursive=True
    )


def get_template_filenames() -> list[str]:
    """Get all relative paths of currently existing templates in
    content directory. Paths are relative to templates directory.
    """
    return glob(
        pathname='**/*.jinja',
        root_dir=EVENT_TEMPLATES_DIR,
        recursive=True
    )


def get_csv_sample_filenames() -> list[str]:
    """Get all relative paths of currently existing samples in
    content directory. Paths are relative to templates directory.
    """
    return glob(
        pathname='**/*.csv',
        root_dir=CSV_SAMPLES_DIR,
        recursive=True
    )


def save_time_pattern(
    pattern_config: dict,
    path: str,
    overwrite: bool = False
) -> None:
    """Save time pattern in specified path. If path is relative then it
    is saved in content directory.
    """
    if not os.path.isabs(path):
        path = os.path.join(TIME_PATTERNS_DIR, path)

    base_path, filename = os.path.split(path)

    try:
        validate_yaml_filename(filename)
    except ValueError as e:
        raise ContentManagementError(str(e)) from e

    if overwrite is False and os.path.exists(path):
        raise ContentManagementError(
            'Time pattern already exists in specified location'
        )

    os.makedirs(base_path, exist_ok=True)

    try:
        save_object_as_yaml(
            data=pattern_config,
            filepath=path
        )
    except (OSError, YAMLError) as e:
        raise ContentManagementError(str(e)) from e


def save_template(
    content: str,
    path: str,
    overwrite: bool = False
) -> None:
    """Save template in specified path. If path is relative then it
    is saved in content directory.
    """
    if not os.path.isabs(path):
        path = os.path.join(EVENT_TEMPLATES_DIR, path)

    base_path, filename = os.path.split(path)

    try:
        validate_jinja_filename(filename)
    except ValueError as e:
        raise ContentManagementError(str(e)) from e

    if overwrite is False and os.path.exists(path):
        raise ContentManagementError(
            'Template already exists in specified location'
        )

    os.makedirs(base_path, exist_ok=True)

    try:
        with open(path, 'w') as f:
            f.write(content)
    except OSError as e:
        raise ContentManagementError(str(e)) from e


def load_time_pattern(path: str) -> Any:
    """Load specified time pattern. If path is relative then it is
    loaded from content directory.
    """
    if not os.path.isabs(path):
        path = os.path.join(TIME_PATTERNS_DIR, path)

    try:
        return load_object_from_yaml(path)
    except (OSError, YAMLError) as e:
        raise ContentManagementError(str(e)) from e


def load_template(path: str) -> str:
    """Load specified template. If path is relative then it is
    loaded from content directory.
    """
    if not os.path.isabs(path):
        path = os.path.join(EVENT_TEMPLATES_DIR, path)

    try:
        with open(path) as f:
            return f.read()
    except OSError as e:
        raise ContentManagementError(str(e)) from e


def load_csv_sample(path: str, delimiter: str = ',') -> list[tuple[str, ...]]:
    """Load specified csv sample and return it as list of tuples. If
    path is relative then it is loaded from content directory.
    """
    if not os.path.isabs(path):
        path = os.path.join(CSV_SAMPLES_DIR, path)

    try:
        return load_sample_from_csv(
            filepath=path,
            delimiter=delimiter
        )
    except OSError as e:
        raise ContentManagementError(str(e)) from e


def load_app_config(path: str) -> Any:
    """Load specified application config. If path is relative then it
    is loaded from content directory.
    """
    if not os.path.isabs(path):
        path = os.path.join(APPLICATION_CONFIGS_DIR, path)

    try:
        return load_object_from_yaml(path)
    except (OSError, YAMLError) as e:
        raise ContentManagementError(str(e)) from e
