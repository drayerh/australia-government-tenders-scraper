import boto3
from botocore.client import Config
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse

class DigitalOceanPipeline(FilesPipeline):
    AWS_ENDPOINT_URL = "https://nyc3.digitaloceanspaces.com"
    AWS_REGION = "nyc3"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s3 = boto3.client('s3',
            endpoint_url=self.AWS_ENDPOINT_URL,
            region_name=self.AWS_REGION,
            aws_access_key_id=config.DO_KEY,
            aws_secret_access_key=config.DO_SECRET,
            config=Config(s3={'addressing_style': 'virtual'}))

    def file_path(self, request, response=None, info=None, *, item=None):
        # Custom path: {spider_name}/{tender_id}/{filename}
        tender_id = item['tender_id']
        original_path = super().file_path(request)
        filename = original_path.split('/')[-1]
        return f"{info.spider.name}/{tender_id}/{filename}"

    def media_to_download(self, request, info):
        # Check if file already exists
        key = self.file_path(request, info=info)
        try:
            self.s3.head_object(Bucket=config.DO_BUCKET, Key=key)
            return None  # Skip download if exists
        except:
            return super().media_to_download(request, info)

    def media_downloaded(self, response, request, info):
        # Upload to DO Spaces after download
        key = self.file_path(request, info=info)
        self.s3.upload_fileobj(
            response.body,
            config.DO_BUCKET,
            key,
            ExtraArgs={'ACL': 'public-read'}
        )
        return key