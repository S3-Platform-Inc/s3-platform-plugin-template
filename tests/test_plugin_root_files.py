import importlib.util
import os
import re
from pathlib import Path

import xml.etree.ElementTree as ET

import pytest


@pytest.mark.pre_set
class TestPluginRootFiles:
    ROOT_TAG: str = "project"
    PROJECT_NAME_TAG: str = "name"
    PROJECT_VERSION_TAG: str = "version"
    XML_FILENAME: str = "plugin.xml"

    @pytest.fixture(autouse=True)
    def plugin_root_config(self) -> Path:
        return Path(__file__).parent.parent / self.XML_FILENAME

    def test_check_plugin_xml_file(self, plugin_root_config):
        """Наличие главного файла плагина"""
        assert os.path.exists(str(plugin_root_config)), f"S3P plugin должен содержать файл `{self.XML_FILENAME}` в корне репозитория"

    def test_check_plugin_xml_structure(self, plugin_root_config):
        """Проверяет структуру плагина"""
        tree = ET.parse(str(plugin_root_config))
        assert tree.getroot().tag == self.ROOT_TAG,\
            f"Не найден тег `{self.ROOT_TAG}` в корне `{self.XML_FILENAME}`"
        assert tree.getroot().attrib.get(self.PROJECT_NAME_TAG), \
            f"Не найдено поле `{self.PROJECT_NAME_TAG}` в теги `{self.ROOT_TAG}`"
        assert tree.getroot().find(self.PROJECT_VERSION_TAG).tag == self.PROJECT_VERSION_TAG,\
            f"Не найден тег `{self.PROJECT_VERSION_TAG}` в теги `{self.ROOT_TAG}`"

    def test_format_version_check(self, plugin_root_config):
        """Проверяет формат версии плагина"""
        pattern = r'^(0*[1-9]\d*|0*\d+\.\d+)$'

        tree = ET.parse(str(plugin_root_config))
        _version = tree.getroot().find(self.PROJECT_VERSION_TAG).text
        assert re.match(pattern, _version), \
            f"{_version} не соответствует шаблону версий. см. в документации"
