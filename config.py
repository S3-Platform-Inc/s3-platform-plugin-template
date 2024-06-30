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
from s3p_sdk.plugin.config.type import SOURCE
from s3p_sdk.module import (
    WEBDRIVER,
)

config = PluginConfig(
    plugin=CoreConfig(
        reference='uniq source name',
        type=SOURCE,
        files=['payload_parser.py', ],
        is_localstorage=False
    ),
    task=TaskConfig(
        trigger=trigger.TriggerConfig(
            type=trigger.SCHEDULE,
            interval=datetime.timedelta(days=7),
        )
    ),
    middleware=MiddlewareConfig(
        modules=[
            modules.TimezoneSafeControlConfig(order=1, is_critical=True),
            modules.CutJunkCharactersFromDocumentTextConfig(order=2, is_critical=True,
                                                            p_fields=['text', 'abstract']),
        ],
        bus=None,
    ),
    payload=payload.PayloadConfig(
        file='payload_parser.py',
        classname='MyParser',
        entry=payload.entry.EntryConfig(
            method='content',
            params=[
                payload.entry.ModuleParamConfig(key='driver', module_name=WEBDRIVER, bus=True),
                payload.entry.ConstParamConfig(key='max_count_documents', value=50),
                payload.entry.ConstParamConfig(key='url',
                                               value='url to the source page'),
            ]
        )
    )
)

__all__ = ['config']
