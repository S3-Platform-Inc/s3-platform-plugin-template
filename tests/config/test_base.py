import os
from pathlib import Path

import pytest

from tests.config.fixtures import Project, project_config


@pytest.mark.pre_set
class TestBaseConfig:

    def test_version(self, project_config: Project):
        assert project_config.version.startswith("3.")

    def test_plugin_structure(self, project_config: Project):
        # Тест проверяет структуру проекта плагина версии 3
        if str(project_config.version).startswith("3.0"):
            assert os.path.exists(
                Path(project_config.root) / 'src'), "проект должен иметь каталог `src` в корне проекта"
            assert os.path.exists(Path(
                project_config.root) / 'src' / project_config.name), f"проект должен иметь каталог `{project_config.name}` в каталоге `src`"
            assert os.path.exists(Path(
                project_config.root) / 'src' / project_config.name / 'config.py'), f"проект должен иметь файл `config.py` в каталоге `{project_config.name}`"
        else:
            assert False, f"Плагины версии {project_config.version} пока не тестируются"
