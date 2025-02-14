import requests
from prometheus_client import Gauge

HEALTH = Gauge(
    'scraper_health',
    'Scraper health status',
    ['spider']
)


class HealthMonitor:
    def __init__(self, spiders):
        self.spiders = spiders

    def check_endpoints(self):
        for spider in self.spiders:
            try:
                response = requests.get(
                    spider.start_url,
                    timeout=10
                )
                HEALTH.labels(spider=spider.name).set(
                    1 if response.ok else 0
                )
            except:
                HEALTH.labels(spider=spider.name).set(0)