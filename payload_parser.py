import time

from s3p_sdk.plugin.payloads.parsers import S3PParserBase
from s3p_sdk.types import S3PRefer, S3PDocument
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class MyParser(S3PParserBase):
    """
    Парсер, использующий базовый класс парсера S3P
    """

    def __init__(self, refer: S3PRefer, web_driver: WebDriver, url: str, max_count_documents: int = None,
                 last_document: S3PDocument = None):
        super().__init__(refer, max_count_documents, last_document)

        # Тут должны быть инициализированы свойства, характерные для этого парсера. Например: WebDriver
        self.URL = url
        self._driver = web_driver
        self._wait = WebDriverWait(self._driver, timeout=20)

    def _parse(self) -> None:
        # HOST - это главная ссылка на источник, по которому будет "бегать" парсер
        self.logger.debug(F"Parser enter to {self._refer.to_logging}")

        for page_link in self._encounter_pages():
            # получение URL новой страницы
            for link in self._collect_doc_links(page_link):
                # парсинг материала
                doc = self._parse_page(link)
                self._find(doc)

    def _parse_page(self, url: str) -> S3PDocument:
        doc = self._page_init(url)
        return doc

    def _page_init(self, url: str) -> S3PDocument:
        self._initial_access_source(url)
        return S3PDocument()

    def _encounter_pages(self) -> str:
        """
        Формирование ссылки для обхода всех страниц
        """
        _base = self.URL
        _param = f'&page='
        page = 0
        while True:
            url = str(_base) + _param + str(page)
            page += 1
            yield url

    def _collect_doc_links(self, _url: str) -> list[str]:
        """
        Формирование списка ссылок на материалы страницы
        """
        try:
            self._initial_access_source(_url)
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

    def _initial_access_source(self, url: str, delay: int = 2):
        self._driver.get(url)
        self.logger.debug('Entered on web page ' + url)
        time.sleep(delay)
