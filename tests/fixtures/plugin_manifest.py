from pathlib import Path

import xml.etree.ElementTree as ET
from s3p_sdk.types.manifest import Manifest

import pytest


ROOT_TAG: str = "project"
PROJECT_NAME_TAG: str = "name"
PROJECT_VERSION_TAG: str = "version"
XML_FILENAME: str = "plugin.xml"


@pytest.fixture(scope="session", autouse=True)
def fix_plugin_root_config_path() -> Path:
    return Path(__file__).parent.parent.parent / XML_FILENAME


@pytest.fixture(scope="session", autouse=True)
def fix_plugin_manifest(fix_plugin_root_config_path) -> Manifest:
    tree = ET.parse(str(fix_plugin_root_config_path))
    _version = tree.getroot().find(PROJECT_VERSION_TAG).text
    _name = tree.getroot().attrib.get(PROJECT_NAME_TAG)
    return Manifest(
        version=_version,
        plugin_name=_name,
    )
