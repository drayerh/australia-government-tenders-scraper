import os

BOT_NAME = 'australian_tenders'

SPIDER_MODULES = ['tenders.spiders']
NEWSPIDER_MODULE = 'tenders.spiders'

# Zyte Smart Proxy
ZYTE_SMARTPROXY_ENABLED = True
ZYTE_SMARTPROXY_APIKEY = os.getenv('ZYTE_API_KEY')

# MongoDB Atlas
MONGO_URI = os.getenv('MONGO_URI')
MONGO_DATABASE = "tenders"

# DigitalOcean Spaces
DO_ENDPOINT = "nyc3.digitaloceanspaces.com"
DO_BUCKET = "tender-documents"
DO_KEY = os.getenv('DO_ACCESS_KEY')
DO_SECRET = os.getenv('DO_SECRET_KEY')

# AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 2