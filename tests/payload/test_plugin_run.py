import datetime
import importlib.util
import os
from typing import Type
import sys

import pytest
from pathlib import Path

from s3p_sdk.plugin.payloads.parsers import S3PParserBase
from selenium.webdriver.chrome import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.ie.webdriver import WebDriver

from tests.config.fixtures import fix_plugin_config, project_config
from tests.payload.fixtures import execute_timeout
from s3p_sdk.types import S3PRefer, S3PDocument, S3PPlugin
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
    def fix_payload(self, project_config, fix_plugin_config) -> Type[S3PParserBase]:
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

    def run_payload(self, payload: Type[S3PParserBase], _plugin: S3PPlugin, driver: WebDriver, refer: S3PRefer, max_document: int,
                    timeout: int = 2):
        # !WARNING Требуется изменить путь до актуального парсера плагина
        from src.s3_platform_plugin_template.template_payload import MyTemplateParser
        if isinstance(payload, type(MyTemplateParser)):
            _payload = payload(refer=refer, plugin=_plugin, web_driver=driver, max_count_documents=max_document, last_document=None)

            @execute_timeout(timeout)
            def execute() -> tuple[S3PDocument, ...]:
                return _payload.content()

            return execute()
        else:
            assert False, "Тест проверяет payload плагина"

    def test_run_with_0_docs_restriction(self, chrome_driver, fix_s3pRefer, fix_payload, fix_s3pPlugin):
        # !WARNING Обновить тест для актуального парсера
        max_docs = 10
        docs = self.run_payload(fix_payload, fix_s3pPlugin, chrome_driver, fix_s3pRefer, max_docs)
        assert len(docs) <= max_docs

    def test_return_types(self, chrome_driver, fix_s3pRefer, fix_payload, fix_s3pPlugin):
        # !WARNING Обновить тест для актуального парсера
        max_docs = 10
        docs = self.run_payload(fix_payload, fix_s3pPlugin, chrome_driver, fix_s3pRefer, max_docs)
        assert isinstance(docs, tuple) and all([isinstance(el, S3PDocument) for el in docs])

    def test_returned_parameters_are_sufficient(self, chrome_driver, fix_s3pRefer, fix_payload, fix_s3pPlugin):
        # !WARNING Обновить тест для актуального парсера
        max_docs = 10
        docs = self.run_payload(fix_payload, fix_s3pPlugin, chrome_driver, fix_s3pRefer, max_docs)
        for el in docs:
            assert el.title is not None and isinstance(el.title, str)
            assert el.link is not None and isinstance(el.link, str)
            assert el.published is not None and isinstance(el.published, datetime.datetime)
            assert el.hash
