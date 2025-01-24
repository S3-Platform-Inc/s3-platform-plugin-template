import re
from pathlib import Path

from tests.fixtures.plugin_manifest import fix_plugin_manifest, fix_plugin_root_config_path
import pytest


@pytest.mark.pre_set
class TestPluginREADME:

    @pytest.fixture(scope="class", autouse=True)
    def readme_content(self) -> str:
        with open(Path(__file__).parent.parent / 'readme.md', 'r') as file:
            readme_content = file.read()
        return readme_content

    def test_badges_name(self, fix_plugin_manifest, readme_content):
        """Проверка соответствие имен репозитория в ссылках на шильдики GitHub"""

        print(fix_plugin_manifest.plugin_name)
        badge_pattern = rf'\[\!\[.*?\]\(https://github\.com/S3-Platform-Inc/{fix_plugin_manifest.plugin_name.replace("_", "-")}/actions/workflows/.*?\.yml/badge\.svg\)\]'

        found_lines = re.findall(badge_pattern, readme_content, re.MULTILINE)
        assert len(found_lines) == 3, "Обновите readme.md файл. Укажите валидный url для GitHub Badges"

    def test_title(self, fix_plugin_manifest, readme_content):
        title_pattern = r'^# S3 Platform Plugin Template'

        matched = re.match(title_pattern, readme_content)

        if fix_plugin_manifest.plugin_name == "s3_platform_plugin_template":
            assert matched
        else:
            assert not matched, "Измените название плагина в readme.md файле"
