from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
from scrapy.exceptions import IgnoreRequest
from requests.auth import AuthBase


class GovAuthMiddleware(RedirectMiddleware):
    def __init__(self, crawler):
        super().__init__(crawler.settings)
        self.credentials = self.load_credentials()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        if request.meta.get('login_required'):
            return self.handle_login(request, spider)

    def handle_login(self, request, spider):
        # Get CSRF token first
        csrf_request = scrapy.Request(
            spider.login_url,
            callback=self.extract_csrf,
            meta={'original_request': request}
        )
        return csrf_request

    def extract_csrf(self, response):
        original_request = response.meta['original_request']
        csrf_token = response.css(
            'input[name="csrf_token"]::attr(value)'
        ).get()

        return scrapy.FormRequest(
            spider.login_url,
            formdata={
                'username': self.credentials[spider.name]['user'],
                'password': self.credentials[spider.name]['pass'],
                'csrf_token': csrf_token
            },
            callback=self.after_login,
            meta={'original_request': original_request}
        )

    def after_login(self, response):
        if "Login Failed" in response.text:
            raise IgnoreRequest("Authentication failed")

        original_request = response.meta['original_request']
        return original_request.replace(
            cookies=response.headers.getlist('Set-Cookie')
        )