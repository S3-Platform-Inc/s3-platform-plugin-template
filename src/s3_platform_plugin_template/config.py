import datetime

from s3p_sdk.plugin.config import (
    PluginConfig,
    CoreConfig,
    TaskConfig,
    trigger,
    MiddlewareConfig,
    modules,
    payload
)
from s3p_sdk.plugin.types import SOURCE
from s3p_sdk.module import (
    WebDriver,
)

config = PluginConfig(
    plugin=CoreConfig(
        reference='my-template-source',
        type=SOURCE,
        files=['template_payload.py', ],
        is_localstorage=False
    ),
    task=TaskConfig(
        trigger=trigger.TriggerConfig(
            type=trigger.SCHEDULE,
            interval=datetime.timedelta(days=1),
        )
    ),
    middleware=MiddlewareConfig(
        modules=[
            modules.TimezoneSafeControlConfig(order=1, is_critical=True),
            modules.CutJunkCharactersFromDocumentTextConfig(order=2, is_critical=True,
                                                            p_fields=['text', 'abstract']),
            modules.FilterOnlyNewDocumentWithDB(order=3, is_critical=True),
            modules.SaveDocument(order=4, is_critical=True),
        ],
        bus=None,
    ),
    payload=payload.PayloadConfig(
        file='template_payload.py',
        classname='MyTemplateParser',
        entry=payload.entry.EntryConfig(
            method='content',
            params=[
                payload.entry.ModuleParamConfig(key='driver', module_name=WebDriver, bus=True),
                payload.entry.ConstParamConfig(key='max_count_documents', value=50),
                payload.entry.ConstParamConfig(key='url',
                                               value='url to the source page'),
            ]
        )
    )
)

__all__ = ['config']
