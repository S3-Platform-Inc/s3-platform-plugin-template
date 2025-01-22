import inspect

import pytest

from tests.fixtures.payload_class import fix_plugin_class
from tests.config.fixtures import fix_plugin_config, project_config, fix_necessary_payload_entry_params


@pytest.mark.pre_set
class TestPluginConfigCompliance:

    def test_payload_entry_params_equaled_payload_init_params(self, fix_plugin_config, fix_plugin_class,
                                                              fix_necessary_payload_entry_params):
        """
        Тест проверяет соответствие начальных параметров в конфигурации и аргументов
        """
        full_arg_spec = inspect.getfullargspec(fix_plugin_class.__init__)
        entry_params = list(full_arg_spec.args)

        for necessary_param in fix_necessary_payload_entry_params:
            assert necessary_param in entry_params
            entry_params.remove(necessary_param)

        for param in fix_plugin_config.payload.entry.params:
            assert param.key not in fix_necessary_payload_entry_params, f"Custom param should not overload necessary params"
            assert param.key in full_arg_spec.args, f'Param `{param.key}` must be processed in the payload class constructor'

        assert set(full_arg_spec.args) == set([param.key for param in fix_plugin_config.payload.entry.params]).union(set(fix_necessary_payload_entry_params))

    def test_payload_entry_param_key_unique(self, fix_plugin_config):

        param_keys = []
        for param in fix_plugin_config.payload.entry.params:
            param_keys.append(param.key)

        assert len(param_keys) == len(set(param_keys))