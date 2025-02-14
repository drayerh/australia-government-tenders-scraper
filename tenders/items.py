import scrapy

class TenderItem(scrapy.Item):
    tender_id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    publish_date = scrapy.Field()
    closing_date = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
# Compare this snippet from australian-government-tenders-scraper/tenders/spiders/finance_tender.py:

