from .base_spider import TenderSpider


class NSWSpider(TenderSpider):
    name = "nsw_tenders"
    start_url = "https://buy.nsw.gov.au/opportunity/search?types=Tenders"
    login_url = "https://buy.nsw.gov.au/login"

    def parse_detail(self, response):
        item = super().parse_detail(response)

        # NSW-specific field processing
        item.add_value(
            'category',
            response.css('.classification::text').getall()
        )
        item.add_css(
            'contact',
            'div.contact-details > p::text'
        )

        yield item