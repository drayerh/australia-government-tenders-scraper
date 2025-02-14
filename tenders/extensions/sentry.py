import sentry_sdk
from sentry_sdk.integrations.scrapy import ScrapyIntegration

class SentryLogger:
    @classmethod
    def from_crawler(cls, crawler):
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
            integrations=[ScrapyIntegration()],
            traces_sample_rate=0.2
        )
        return cls()