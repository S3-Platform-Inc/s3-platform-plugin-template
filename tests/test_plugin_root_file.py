import os
import re

import xml.etree.ElementTree as ET
from tests.fixtures.plugin_manifest import fix_plugin_root_config_path, XML_FILENAME, ROOT_TAG, PROJECT_NAME_TAG, \
    PROJECT_VERSION_TAG

import pytest


@pytest.mark.pre_set
class TestPluginRootFile:

    def test_check_plugin_xml_file(self, fix_plugin_root_config_path):
        """Наличие главного файла плагина"""
        assert os.path.exists(str(fix_plugin_root_config_path)), f"S3P plugin должен содержать файл `{XML_FILENAME}` в корне репозитория"

    def test_check_plugin_xml_structure(self, fix_plugin_root_config_path):
        """Проверяет структуру плагина"""
        tree = ET.parse(str(fix_plugin_root_config_path))
        assert tree.getroot().tag == ROOT_TAG,\
            f"Не найден тег `{ROOT_TAG}` в корне `{XML_FILENAME}`"
        assert tree.getroot().attrib.get(PROJECT_NAME_TAG), \
            f"Не найдено поле `{PROJECT_NAME_TAG}` в теги `{ROOT_TAG}`"
        assert tree.getroot().find(PROJECT_VERSION_TAG).tag == PROJECT_VERSION_TAG,\
            f"Не найден тег `{PROJECT_VERSION_TAG}` в теги `{ROOT_TAG}`"

    def test_format_version_check(self, fix_plugin_root_config_path):
        """Проверяет формат версии плагина"""
        pattern = r'^(0*[1-9]\d*|0*\d+\.\d+)$'

        tree = ET.parse(str(fix_plugin_root_config_path))
        _version = tree.getroot().find(PROJECT_VERSION_TAG).text
        assert re.match(pattern, _version), \
            f"{_version} не соответствует шаблону версий. см. в документации"
