import datetime
import time

from s3p_sdk.plugin.payloads.parsers import S3PParserBase
from s3p_sdk.types import S3PRefer, S3PDocument, S3PPlugin
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class MyTemplateParser(S3PParserBase):
    """
    A Parser payload that uses S3P Parser base class.
    """

    def __init__(self, refer: S3PRefer, plugin: S3PPlugin, web_driver: WebDriver, max_count_documents: int = None,
                 last_document: S3PDocument = None):
        super().__init__(refer, plugin, max_count_documents, last_document)

        # Тут должны быть инициализированы свойства, характерные для этого парсера. Например: WebDriver
        self._driver = web_driver
        self._wait = WebDriverWait(self._driver, timeout=20)

    def _parse(self) -> None:
        for article in self._test_data():
            self._find(article)

    def _test_data(self) -> list[S3PDocument]:
        out = [
            S3PDocument(None, "title-test-1", None, None, 'web-link-test-1', None, None, datetime.datetime.now(), None),
            S3PDocument(None, "title-test-2", None, None, 'web-link-test-2', None, None, datetime.datetime.now(), None),
            S3PDocument(None, "title-test-3", None, None, 'web-link-test-3', None, None, datetime.datetime.now(), None),
            S3PDocument(None, "title-test-4", None, None, 'web-link-test-4', None, None, datetime.datetime.now(), None)
        ]
        return out

    def _example_parse_page(self, url: str) -> S3PDocument:
        doc = self._example_page_init(url)
        return doc

    def _example_page_init(self, url: str) -> S3PDocument:
        self._example_initial_access_source(url)
        return S3PDocument(None, None, None, None, None, None, None, None, None)

    def _example_encounter_pages(self) -> str:
        """
        Формирование ссылки для обхода всех страниц
        """
        _base = 'self.URL'
        _param = f'&page='
        page = 0
        while True:
            url = str(_base) + _param + str(page)
            page += 1
            yield url

    def _example_collect_doc_links(self, _url: str) -> list[str]:
        """
        Формирование списка ссылок на материалы страницы
        """
        try:
            self._example_initial_access_source(_url)
            self._wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, '<class контейнера>')))
        except Exception as e:
            raise NoSuchElementException() from e
        links = []

        try:
            articles = self._driver.find_elements(By.CLASS_NAME, '<class контейнера>')
        except Exception as e:
            raise NoSuchElementException('list is empty') from e
        else:
            for article in articles:
                try:
                    doc_link = article.find_element(By.TAG_NAME, 'a').get_attribute('href')
                except Exception as e:
                    raise NoSuchElementException(
                        'Страница не открывается или ошибка получения обязательных полей') from e
                else:
                    links.append(doc_link)
        return links

    def _example_initial_access_source(self, url: str, delay: int = 2):
        self._driver.get(url)
        self.logger.debug('Entered on web page ' + url)
        time.sleep(delay)
