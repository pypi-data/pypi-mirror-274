import pytest

from eventum_content_manager.validators import (validate_csv_filename,
                                                validate_jinja_filename,
                                                validate_yaml_filename)


def test_validate_jinja_filename():
    validate_jinja_filename('template.jinja')
    validate_jinja_filename('template.json.jinja')

    with pytest.raises(ValueError):
        validate_jinja_filename('template.json')

    with pytest.raises(ValueError):
        validate_jinja_filename('template')

    with pytest.raises(ValueError):
        validate_jinja_filename('')


def test_validate_yaml_filename():
    validate_yaml_filename('config.yaml')
    validate_yaml_filename('config.yml')

    with pytest.raises(ValueError):
        validate_yaml_filename('config.toml')

    with pytest.raises(ValueError):
        validate_yaml_filename('config')

    with pytest.raises(ValueError):
        validate_yaml_filename('')


def test_validate_csv_filename():
    validate_csv_filename('sample.csv')

    with pytest.raises(ValueError):
        validate_csv_filename('sample.xls')

    with pytest.raises(ValueError):
        validate_csv_filename('sample')

    with pytest.raises(ValueError):
        validate_csv_filename('')
