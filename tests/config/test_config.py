import os
from pathlib import Path

import pytest
from s3p_sdk.plugin.config.payload import EntryConfig
from s3p_sdk.plugin.config.payload.entry import AbcParamConfig
from s3p_sdk.plugin.types import PIPELINE, SOURCE, ML

from tests.config.fixtures import fix_plugin_config, project_config
from s3p_sdk.plugin.config import (
    PluginConfig, CoreConfig, TaskConfig, MiddlewareConfig, PayloadConfig, RestrictionsConfig
)
import s3p_sdk.module as s3p_module


class PluginStructure:
    PLUGIN: str = 'plugin'
    TASK: str = 'task'
    MIDDLEWARE: str = 'middleware'
    PAYLOAD: str = 'payload'


@pytest.mark.pre_set
class TestBaseConfig:

    def test_config_exists(self, fix_plugin_config):
        """Проверка на то, что файл существует"""
        assert isinstance(fix_plugin_config,
                          PluginConfig), "`config.py` файл должен содержать переменную `config` с типом `PluginConfig`"

    def test_config_structure(self, fix_plugin_config):
        """Проверка базовой структуры плагина"""
        assert isinstance(fix_plugin_config.__dict__.get(PluginStructure.PLUGIN),
                          CoreConfig), "`PluginConfig` должен содержать переменную `plugin` с типом `CorePlugin`"
        assert isinstance(fix_plugin_config.__dict__.get(PluginStructure.TASK),
                          TaskConfig), "`PluginConfig` должен содержать переменную `talk` с типом `TaskConfig`"
        assert isinstance(fix_plugin_config.__dict__.get(PluginStructure.MIDDLEWARE),
                          MiddlewareConfig), "`PluginConfig` должен содержать переменную `middleware` с типом `MiddlewareConfig`"
        assert isinstance(fix_plugin_config.__dict__.get(PluginStructure.PAYLOAD),
                          PayloadConfig), "`PluginConfig` должен содержать переменную `payload` с типом `PayloadConfig`"


@pytest.mark.pre_set
class TestConfigPlugin:

    def test_config_plugin_structure(self, fix_plugin_config):
        _cplugin = fix_plugin_config.__dict__.get(PluginStructure.PLUGIN)

        assert isinstance(_cplugin.__dict__.get('reference'), str)
        assert isinstance(_cplugin.__dict__.get('type'), str) and str(_cplugin.__dict__.get('type')) in (
        SOURCE, ML, PIPELINE)
        assert isinstance(_cplugin.__dict__.get('files'), list) and all(
            [isinstance(it, str) for it in _cplugin.__dict__.get('files')])
        assert isinstance(_cplugin.__dict__.get('is_localstorage'), bool)
        assert isinstance(_cplugin.__dict__.get('restrictions'), RestrictionsConfig)

    def test_config_plugin_files(self, fix_plugin_config, project_config):
        """Проверка наличия файлов плагина"""
        _cplugin = fix_plugin_config.__dict__.get(PluginStructure.PLUGIN)
        _files = _cplugin.__dict__.get('files')

        for _file in _files:
            file_path = Path(project_config.root) / 'src' / project_config.name / _file
            assert os.path.exists(file_path)


@pytest.mark.pre_set
class TestConfigPayload:

    def test_config_payload_structure(self, fix_plugin_config, project_config):
        """Провека структуры PayliadConfig"""
        _cpayload = fix_plugin_config.__dict__.get(PluginStructure.PAYLOAD)

        assert isinstance(_cpayload.__dict__.get('file'), str)
        assert isinstance(_cpayload.__dict__.get('classname'), str)
        assert isinstance(_cpayload.__dict__.get('entry'), EntryConfig)

    def test_config_payload_entry_structure(self, fix_plugin_config, project_config):
        """Провека структуры PayliadConfig"""
        _pentry = fix_plugin_config.__dict__.get(PluginStructure.PAYLOAD).__dict__.get('entry')

        assert isinstance(_pentry.__dict__.get('method'), str)
        assert _pentry.__dict__.get(
            'method') == 'content', f"Метод запуска плагина {_pentry.__dict__.get('method')} не соответствуе значению по умолчанию `content`"
        assert isinstance(_pentry.__dict__.get('params'), list) and all(
            [isinstance(it, AbcParamConfig) for it in _pentry.__dict__.get('params')])

    def test_config_plugin_files(self, fix_plugin_config, project_config):
        """Проверка наличия файлов плагина"""
        _cplugin = fix_plugin_config.__dict__.get(PluginStructure.PLUGIN)
        _files = _cplugin.__dict__.get('files')

        for _file in _files:
            file_path = Path(project_config.root) / 'src' / project_config.name / _file
            assert os.path.exists(file_path)

    def test_exists_entry_file(self, fix_plugin_config, project_config):
        """Проверяет наличие файла-точки входа в плагин"""
        _cpayload = fix_plugin_config.__dict__.get(PluginStructure.PAYLOAD)
        _cpayload.__dict__.get('file')

        entry_path = Path(project_config.root) / 'src' / project_config.name / _cpayload.__dict__.get('file')
        assert os.path.exists(entry_path)

    def test_right_extensions_file(self, fix_plugin_config, project_config):
        """Расширение файла-точки входа в плагин должен быть `.py`"""
        _cpayload = fix_plugin_config.__dict__.get(PluginStructure.PAYLOAD)
        _cpayload.__dict__.get('file')

        entry_path = Path(project_config.root) / 'src' / project_config.name / _cpayload.__dict__.get('file')
        assert os.path.exists(entry_path)
        assert entry_path.suffix == '.py'

    def test_compare_entry_file_and_plugin_files(self, fix_plugin_config):
        """Файл в параметре `payload.file` должен быть описан в `plugin.files`"""
        _cpayload = fix_plugin_config.__dict__.get(PluginStructure.PAYLOAD)
        _cplugin = fix_plugin_config.__dict__.get(PluginStructure.PLUGIN)

        assert _cpayload.__dict__.get('file') in _cplugin.__dict__.get('files')


@pytest.mark.pre_set
class TestConfigMiddleware:

    def test_modules_order(self, fix_plugin_config):
        for i, module in enumerate(fix_plugin_config.middleware.modules):
            assert module.order == i + 1, f"Module {module.name} should have order {i + 1}"

    def test_modules_key_params(self, fix_plugin_config):
        for i, module in enumerate(fix_plugin_config.middleware.modules):
            assert isinstance(module.order, int)
            assert isinstance(module.name, str)
            assert isinstance(module.is_critical, bool)
