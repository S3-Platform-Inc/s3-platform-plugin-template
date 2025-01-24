import datetime
import importlib.util
import os
from typing import Callable, Union

import pytest
from pathlib import Path

from s3p_sdk.plugin.payloads.parsers import S3PParserBase
from selenium.webdriver.chrome import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.ie.webdriver import WebDriver

from tests.config.fixtures import fix_plugin_config, project_config
from s3p_sdk.types import S3PRefer, S3PDocument, S3PPlugin, S3PPluginRestrictions
from s3p_sdk.plugin.types import SOURCE


@pytest.mark.payload_set
class TestPayloadRun:

    @pytest.fixture(scope="class", autouse=True)
    def chrome_driver(self) -> WebDriver:
        options = webdriver.Options()

        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        driver = Chrome(options=options)
        yield driver
        driver.quit()

    @pytest.fixture(scope="class")
    def fix_s3pRefer(self) -> S3PRefer:
        return S3PRefer(1, 'test-refer', SOURCE, None)

    @pytest.fixture(scope="class")
    def fix_s3pPlugin(self) -> S3PPlugin:
        return S3PPlugin(1, 'unittests/repo/1', True, None, None, SOURCE, "3.0")

    @pytest.fixture(scope="module", autouse=True)
    def fix_payload(self, project_config, fix_plugin_config) -> S3PParserBase:
        MODULE_NAME: str = 's3p_test_plugin_payload'
        """Загружает конфигурацию из config.py файла по динамическому пути на основании конфигурации"""
        payload_path = Path(project_config.root) / 'src' / project_config.name / fix_plugin_config.payload.file
        assert os.path.exists(payload_path)
        spec = importlib.util.spec_from_file_location(MODULE_NAME, payload_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Get the class from the module
        class_name = fix_plugin_config.payload.classname
        assert class_name in module.__dict__, f"Class {class_name} not found in module."

        # Create an instance of the class
        parser_class = module.__dict__[class_name]
        assert issubclass(parser_class, S3PParserBase), f"{class_name} is not a subclass of S3PParserBase."
        return parser_class

    def run_payload(self, payload: Union[S3PParserBase, Callable], refer: S3PRefer, _plugin: S3PPlugin, restrictions: S3PPluginRestrictions, driver: WebDriver):

        _payload = payload(
            refer=refer,
            plugin=_plugin,
            restrictions=restrictions,
            web_driver=driver
        )
        return _payload.content()

    # !WARNING: Изменить максимальное время работы плагина из логических соображений
    @pytest.mark.timeout(30)
    def test_all_cases_with_once_executing_parser(self, chrome_driver, fix_s3pRefer, fix_payload, fix_s3pPlugin):
        """
        Test Case

        Этот тест выполняет однократный запуск парсера, а затем проверяет ответ по нескольким параметрам.

        Требования:
            1. Количество материалов должно быть не меньше параметра максимального числа материалов.
            2. Тип возвращаемых документов должен соответствовать S3PDocument
            3. Каждый полученный документ должен обязательно содержать 3 ключевых поля (title, link, published)

        """
        max_docs = 4
        docs = self.run_payload(fix_payload, fix_s3pRefer, fix_s3pPlugin, S3PPluginRestrictions(max_docs, None, None, None), chrome_driver)

        # 1. Количество материалов должно быть не меньше параметра максимального числа материалов.
        assert len(docs) == max_docs, f"Payload вернул {len(docs)} материалов. А должен был {max_docs}"

        # 2. Тип возвращаемых документов должен соответствовать S3PDocument
        assert isinstance(docs, tuple) and all([isinstance(el, S3PDocument) for el in docs]), f"Тип возвращаемых документов должен соответствовать S3PDocument"

        # 3. Каждый полученный документ должен обязательно содержать 3 ключевых поля (title, link, published)
        for el in docs:
            assert el.title is not None and isinstance(el.title, str), f"Документ {el} должен обязательно содержать ключевое поле title"
            assert el.link is not None and isinstance(el.link, str), f"Документ {el} должен обязательно содержать ключевое поле link"
            assert el.published is not None and isinstance(el.published, datetime.datetime), f"Документ {el} должен обязательно содержать ключевое поле published"
            assert el.hash

    @pytest.mark.timeout(20)
    def test_date_restrictions(self, chrome_driver, fix_s3pRefer, fix_payload, fix_s3pPlugin):
        _boundary_date = datetime.datetime.now() - datetime.timedelta(days=2)
        docs = self.run_payload(fix_payload, fix_s3pRefer, fix_s3pPlugin, S3PPluginRestrictions(None, None, _boundary_date, None), chrome_driver)

        for doc in docs:
            assert doc.published >= _boundary_date, f"The {doc.to_logging} must meet the restriction (older than {_boundary_date})"
