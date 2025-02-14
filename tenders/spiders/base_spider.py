import scrapy
from scrapy_zyte_smartproxy import ZyteSmartProxyRequest
from itemloaders import ItemLoader
from tenders.items import TenderItem
from tenders.middlewares.auth_middleware import GovAuthMiddleware


class TenderSpider(scrapy.Spider):
    name = "base_tender"
    custom_settings = {
        'ZYTE_SMARTPROXY_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'tenders.middlewares.auth_middleware.GovAuthMiddleware': 543,
            'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 725,
        },
        'ITEM_PIPELINES': {
            'tenders.pipelines.mongodb_pipeline.MongoDBPipeline': 300,
            'tenders.pipelines.storage_pipeline.DigitalOceanPipeline': 400,
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selector_config = self.load_selectors()
        self.login_creds = self.load_credentials()

    def load_selectors(self):
        # Load from config/selectors.yaml
        with open('config/selectors.yaml') as f:
            return yaml.safe_load(f)[self.name]

    def start_requests(self):
        yield ZyteSmartProxyRequest(
            self.start_url,
            callback=self.parse_list,
            meta={'zyte_smartproxy': True}
        )

    def parse_list(self, response):
        # Pagination handling with common CSS selector
        for tender in response.css(self.selector_config['list_item']):
            detail_url = tender.css(
                self.selector_config['detail_link']
            ).get()
            yield response.follow(
                detail_url,
                self.parse_detail,
                meta={'login_required': True}
            )

        next_page = response.css(
            self.selector_config['next_page']
        ).get()
        if next_page:
            yield response.follow(next_page, self.parse_list)

    def parse_detail(self, response):
        loader = ItemLoader(item=TenderItem(), response=response)
        for field, selector in self.selector_config['detail_fields'].items():
            loader.add_css(field, selector)

        # Handle file attachments
        files = response.css(
            self.selector_config['file_selector']
        ).getall()
        loader.add_value('file_urls', files)

        yield loader.load_item()