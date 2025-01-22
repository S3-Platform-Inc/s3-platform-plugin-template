import importlib.util
import os
from pathlib import Path

import xml.etree.ElementTree as ET

import pytest
from s3p_sdk.plugin.config import PluginConfig


class Project:
    name: str
    version: str
    root: str
    plugin_path: str

    def __init__(self, dir: str):
        try:
            tree = ET.parse(Path(dir) / 'plugin.xml')
            root = tree.getroot()
            project_name = root.attrib.get('name')
            assert project_name is not None
            self.name = project_name
            version = root.find('version').text
            assert version is not None
            self.version = version
            self.root = dir
            self.plugin_path = str(Path(dir) / 'src' / self.name)
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            raise Exception(f"Error parsing XML") from e
        except FileNotFoundError:
            print(f"File not found: {Path(dir) / 'plugin.xml'}")
            raise FileNotFoundError(f"File not found {Path(dir) / 'plugin.xml'}")


@pytest.fixture(scope="session")
def project_config() -> Project:
    return Project(str(Path(__file__).parent.parent.parent))


@pytest.fixture(scope="session")
def fix_plugin_config(project_config) -> PluginConfig:
    """Загружает конфигурацию из config.py файла по динамическому пути на основании конфигурации"""
    config_path = Path(project_config.root) / 'src' / project_config.name / 'config.py'
    assert os.path.exists(config_path)
    spec = importlib.util.spec_from_file_location('s3p_plugin_config', config_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.config


@pytest.fixture(scope="session")
def fix_necessary_payload_entry_params() -> tuple[str, ...]:
    return 'refer', 'plugin', 'restrictions', 'self'
