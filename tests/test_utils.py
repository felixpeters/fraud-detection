import yaml

from src.utils import add, load_config


def test_add():
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0


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
    assert load_config(config_path) is None
