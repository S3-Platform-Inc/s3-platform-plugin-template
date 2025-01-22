from typing import Type

import pytest

# TODO: Указать путь до класса плагина
from s3_platform_plugin_template.template_payload import MyTemplateParser as imported_payload_class


@pytest.fixture(scope="module")
def fix_plugin_class() -> Type[imported_payload_class]:
    return imported_payload_class
