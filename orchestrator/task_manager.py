import redis
from rq import Queue
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class TaskOrchestrator:
    def __init__(self):
        self.redis = redis.Redis(
            host=config.REDIS_HOST,
            port=6379,
            password=config.REDIS_PASS
        )
        self.queue = Queue('tender_scrapers', connection=self.redis)
        self.process = CrawlerProcess(get_project_settings())

    def schedule_spider(self, spider_name):
        self.queue.enqueue(
            self.run_spider,
            spider_name,
            job_timeout='30m'
        )

    def run_spider(self, spider_name):
        self.process.crawl(spider_name)
        self.process.start()