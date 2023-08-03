import pytest
import yaml

from src.utils import load_config


def test_load_config(tmp_path):
    # Create a temporary YAML file with test data
    config_path = tmp_path / "test_config.yaml"
    expected_config = {"key1": "value1", "key2": "value2"}
    with open(config_path, "w") as f:
        yaml.dump(expected_config, f)

    # Test loading a valid YAML file
    assert load_config(config_path) == expected_config

    # Test loading an invalid YAML file
    config_path = tmp_path / "test_config_invalid.yaml"
    with open(config_path, "w") as f:
        f.write("invalid_yaml")
    with pytest.raises(TypeError):
        load_config(config_path)
