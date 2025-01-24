import re
from pathlib import Path

from tests.fixtures.plugin_manifest import fix_plugin_manifest, fix_plugin_root_config_path
import pytest


@pytest.mark.pre_set
class TestPluginREADME:

    def test_badges_name(self, fix_plugin_manifest):
        """Проверка соответствие имен репозитория в ссылках на шильдики GitHub"""

        print(fix_plugin_manifest.plugin_name)
        badge_pattern = rf'\[\!\[.*?\]\(https://github\.com/S3-Platform-Inc/{fix_plugin_manifest.plugin_name.replace("_", "-")}/actions/workflows/.*?\.yml/badge\.svg\)\]'

        with open(Path(__file__).parent.parent / 'readme.md', 'r') as file:
            readme_content = file.read()

        found_lines = re.findall(badge_pattern, readme_content, re.MULTILINE)
        assert len(found_lines) == 3, "Обновите readme.md файл. Укажите валидный url для GitHub Badges"
