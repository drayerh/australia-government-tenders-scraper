from prometheus_client import Counter, Histogram

SCRAPED_ITEMS = Counter(
    'scraped_items_total',
    'Total items scraped',
    ['spider', 'status']
)

REQUEST_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency distribution',
    ['spider', 'method']
)

class MetricsExtension:
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.stats)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        return ext

    def item_scraped(self, item, spider):
        SCRAPED_ITEMS.labels(
            spider=spider.name,
            status='success'
        ).inc()