# S3 Platform Plugin Template

[![Test Plugin](https://github.com/S3-Platform-Inc/s3-platform-plugin-template/actions/workflows/plugin_test.yml/badge.svg)](https://github.com/S3-Platform-Inc/s3-platform-plugin-template/actions/workflows/plugin_test.yml)
[![Release plugin](https://github.com/S3-Platform-Inc/s3-platform-plugin-template/actions/workflows/build-release.yml/badge.svg)](https://github.com/S3-Platform-Inc/s3-platform-plugin-template/actions/workflows/build-release.yml)
[![Sync plugin to S3](https://github.com/S3-Platform-Inc/s3-platform-plugin-template/actions/workflows/sync-release.yml/badge.svg)](https://github.com/S3-Platform-Inc/s3-platform-plugin-template/actions/workflows/sync-release.yml)

> [!WARNING]
> В документации к плагину используются GitHub Badges - это динамические шильдики, которые в этом кейсе показывают статус работы Github Actions.
> Необходимо обновить ссылки в шильдиках. Заменить `s3-platform-plugin-template` на `название репозитория плагина`.
> _Удалить это напоминание из readme.md 


> [!NOTE]
> Нажми на <kbd>Use this template</kbd> кнопку и клонируй его в IDE.

S3 Platform Plugin Template - это репозиторий предоставляет чистый шаблон для простого и быстрого создания проекта плагина (Посмотри статью [Creating a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)).

Основная цель этого шаблона - ускорить этап установки плагина как для новичков, так и для опытных разработчиков, предварительно настроив CI проекта, указав ссылки на нужные страницы документации и сохранив все в порядке.

[//]: # (Если вы все еще не совсем понимаете, о чем идет речь, прочитайте наше введение: Что такое S3 Platform?)

# Содержание
- [Быстрый старт](#быстрый-старт)
- [Обновление зависимостей](#обновления-зависимостей)
- [Требования](#требования-к-разработке-плагина)
  - [Структура](#обязательная-структура)
  - [CI](#github-actions)
  - [Тесты](#тесты)
    - [Как запустить тесты](#запуск-тестов)
- [Правила написания парсера](#правила-написания-парсеров)

## Быстрый старт

1. На GitHub:
   1. В GitHub выбрать `Use this template` для создания плагина.
   2. Назвать новый плагин в соответствии с [требованиями](#название-репозитория).
   3. **ПРОПУСТИТЬ ШАГ, ЕСЛИ РЕПОЗИТОРИЙ СОЗДАЕТСЯ В РАМКАХ [ОРГАНИЗАЦИИ](https://github.com/S3-Platform-Inc)**. Добавить секреты в репозиторий (см. [тут](#секреты)).
   4. Открыть новые issue (пример названия: `New plugin: xxx` или `add payload xxx`)
   5. Создать новую ветку в проекте, наследуемую от `main` (пример названия: `feature/{issue id}-new-plugin`).
2. В IDE:
   1. Скачаем новый репозиторий `git clone [repo name]`.
   2. Переключаемся в новую ветку `git checkout feature/{issue id}-new-plugin`.
   3. Прочитать [требования](#требования-к-разработке-плагина).
   4. Обновить Github Badges в начале файла `readme.md` (`s3-platform-plugin-template` на `название репозитория плагина`).
   5. Придумать название плагина в соответствии с [требованиями](#название-плагина). 
   6. Обновить [GitHub Actions](#обновление-cicd-).
   7. Обновить [декларацию плагина](#pluginxml).
   8. Обновить документация (`readme.md`): Заголовок, описание, характерные особенности парсера и логика работы, эксклюзивные начальные параметры парсера. 
   9. Написать логику плагина (см. [тут](#правила-написания-парсеров)). 
   10. Обновить конфигурацию плагина (см. [тут](https://github.com/S3-Platform-Inc/s3p-sdk/blob/main/docs/config.md)).
   11. Обновить тесты и дописать новые при необходимости (см. [тут](#тесты)).
   12. Запустить тесты (см. [тут](#запуск-тестов)).
   13. Если все тесты пройдены, сохраняем изменениями (`git commit ...` и `git pull`).
3. На GitHub:
   1. Создать pull request для ветки `feature/{issue id}-new-plugin`.
   2. Дождаться завершения `Checks` для PR.
   3. **ШАГ ОБЯЗАТЕЛЕН В РАМКАХ [ОРГАНИЗАЦИИ](https://github.com/S3-Platform-Inc)**. Указать в PR админа: `Assignees` -> `CuberHuber`
   4. **ПРОПУСТИТЬ ШАГ, ЕСЛИ РЕПОЗИТОРИЙ СОЗДАЕТСЯ В РАМКАХ [ОРГАНИЗАЦИИ](https://github.com/S3-Platform-Inc)**. Слить изменения и закрыть PR.

------------

## Обновления зависимостей
При работе над плагином важно поддерживать его версию в актуальном состоянии. Шаблон плагинов и версия SDK часто обновляются, из-за начальной стадии продукта.
Чтобы синхронизироваться с шаблоном можно выполнить следующие действия.

> [!NOTE]
> Рекомендуется выполнять синхронизацию мануально. Таким образом вы сможете исправить потенциальные конфликты при слиянии.

1. Нужно добавить шаблон в git
```shell
git remote add template https://github.com/S3-Platform-Inc/s3-platform-plugin-template.git
git fetch --all
```

2. Влить `main` ветку шаблона в `main` ветку репозитория плагина
> [!NOTE]
> Убедитесь, что важные изменения вашего проекта не будут удалены
```shell
git merge template/main --allow-unrelated-histories
```
3. При возникновении конфликтов, нужно принять все изменения из template, а затем подстраивать свой код.
> [!NOTE]
> После синхронизации с шаблоном, нужно обновить зависимости.
```shell
poetry install
# или, при ошибке установки можно обновить записимость вручную.
poetry add s3p-sdk@[relevant version]
```
4. Обновить код плагина и тестов при необходимости.


## Требования к разработке плагина

### Правила наименований

#### Название репозитория
Общий шаблон названия репозитория
```
s3p-plugin-[type]-[uniq_name]
```
Шаблон названия репозитория парсера
```
s3p-plugin-parser-[uniq_name]
```
Пример названия репозитория парсера
```
s3p-plugin-parser-emvco
```

#### Название плагина
Шаблон названия плагина схож с названием репозитория.
```
s3p_plugin_[type]_[uniq_name]
```
Пример названия репозитория парсера
```
s3p_plugin_parser_emvco
```

### Обязательная структура
Репозиторий плагина состоит из основных компонентов:

```markdown
my-plugin/                      # Репозиторий
│
├── .github/                    #
│   └── workflows/              # GitHub Actions 
│
├── src/                        # Основная директория разработки
│   └── <uniq plugin name>/     # Каталог с файлами плагина.
│       ├── config.py           # Конфигурация плагина
│       └── <some files>.*      # Файлы плагина (его payload)
│ 
├── tests/                      # Тесты для плагина
│
└── plugin.xml                  # Основной декларативный файл плагина
```

#### Plugin.xml
Стандартный вид `plugin.xml`:
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<project name="[ uniq plugin name ]">
    <version>[ version ]</version>
</project>
```
- уникальное имя плагина [`uniq plugin name`] см. [тут](#название-плагина). Используется как имя каталога с файлами плагина и в тестах.
- версия плагина [`version`]. Имеет формат `[N > 0].[N >= 0]`. Последняя стабильная версия по умолчанию - `3.0`.

#### src
В каталоге `src` должен обязательно находиться каталог, названный [`uniq plugin name`] (Такое же название, как и в [plugin.xml](#pluginxml)). 

##### uniq plugin name
- Каталог плагина должен обязательно содержать файл `repo/src/[uniq plugin name]/config.py`.
- Все дополнительные файлы плагина (парсер, вспомогательные файлы) должны быть расположены в этом разделе `repo/src/[uniq plugin name]/`.

##### config.py
Файл config.py - это обязательный файл плагина. 

> [!WARNING]
> Нужно просмотреть файл `config.py` и поля, связанные с уникальными названиями и файлами.

> [!TIP]
> Читайте комментарии в файле `config.py`


### GitHub Actions
В репозитории настроен CI/CD на GitHub Actions.
Для его полноценной работы необходимо добавить секреты в репозиторий на стороне GitHub (см. [раздел](https://github.com/S3-Platform-Inc/s3-platform-plugin-template/settings/secrets/actions)).

Если репозиторий с плагином создан в аккаунте организации [S3 Platform](https://github.com/S3-Platform-Inc), то можно воспользоваться секретами организации. В противном случае нужно создавать секреты репозитория.

#### Секреты

**CI/СD:**
- `PLUGIN_RELEASE_TOKEN`: создается в GitHub для работы с релизами репозиториев (см. [здесь](https://github.com/settings/personal-access-tokens)).

S3 Platform использует Amazon S3 в качестве [объектного хранилища](https://ru.wikipedia.org/wiki/Amazon_S3).
Следующие секреты требуются для подключения к нему (_Все 5 значений можно получить в панели администратора хранилища_):
- `S3_ACCESS_KEY_ID`
- `S3_SECRET_ACCESS_KEY`
- `S3_BACKET_NAME`
- `S3_REGION`
- `S3_SERVICE_URL`

#### Обновление CI/CD 

> [!IMPORTANT]
> После написание плагина от разработчика потребуется обновить некоторые поля в github actions yml файлах.

#### [Файл сборка](.github/workflows/build-release.yml)
Требуется обновить переменную `PATH_TO_CONFIG` в `env` на `src.[uniq plugin name].config`.


### Тесты

> [!WARNING]
> Требуется дополнить некоторые тесты, которые помечены отметкой `!WARNING`

В [тестах нагрузки](tests/payload/test_plugin_run.py) в функции `run_payload()` нужно обновить сигнатуру вызова (соответствие главному классу парсера).

> [!TIP]
> Последующие тесты с отметкой нужно просмотреть и обновить при необходимости. 

> [!TIP]
> Рекомендуется дополнять тесты для парсеров с необычной логикой.

#### Запуск тестов
```shell
poetry run pytest -v
```
or
```shell
pytest -v
```

## Правила написания парсеров

Ниже приведен пример парсера с подробным описанием.
```python
from s3p_sdk.plugin.payloads.parsers import S3PParserBase
from s3p_sdk.types import S3PRefer, S3PPlugin, S3PPluginRestrictions
from s3p_sdk.exceptions.parser import S3PPluginParserOutOfRestrictionException, S3PPluginParserFinish 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

class MyTemplateParser(S3PParserBase):
    """
    Parser plugin that uses `S3PParserBase`
    """

    def __init__(self, refer: S3PRefer, plugin: S3PPlugin, restrictions: S3PPluginRestrictions, web_driver: WebDriver):
        """
        Constructor for the parser plugin.
        
        Required parameters (passed by the platform):
        :param refer: S3PRefer - the source processed by the plugin.
        :param plugin: S3PPlugin - plugin metadata.
        :param restrictions: S3PPluginRestrictions - restrictions for parsing (maximum_materials, to_last_material, from_date, to_date).
        
        Other parameters can be added at the discretion of the parser developer.
        (These parameters should be specified in src/<uniq plugin name>/config.py).
        However, it's worth considering the rule "everything that can be parameterized should be parameterized".
        """
        super().__init__(refer, plugin, restrictions)

        # Тут должны быть инициализированы свойства, характерные для этого парсера. Например: WebDriver
        self._driver = web_driver
        self._wait = WebDriverWait(self._driver, timeout=20)

    def _parse(self) -> None:
        """
        The main method of the parser class, overriding the method of the `S3PParserBase` class.
        
        This method will be called by the platform when the parser is launched.
        This obliges the developer to parse the source in this method 
        (of course, the developer can create additional methods within this class).
        """
        for article in self.test_data():
            try:
                # The self._find(:S3PDocument) method is called during parsing to give the found document to the platform.
                # The developer must use only this method when parsing.
                # The developer doesn't need to think about what happens next. 
                # The platform itself will stop the parser's work when certain conditions are met: 
                # the required number of documents has been collected, date restrictions are met, or the last document is found.
                self._find(article)
            except S3PPluginParserFinish as e:
                # Parsing is finished due to restrictions
                raise e
            except S3PPluginParserOutOfRestrictionException:
                # Document is out of date range, continue to next material.
                # You can also use a restriction exception to skip irrelevant materials later on.
                continue

```

