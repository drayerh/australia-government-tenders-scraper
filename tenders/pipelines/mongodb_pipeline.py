import motor.motor_asyncio
from itemadapter import ItemAdapter

class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    async def open_spider(self, spider):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        await self.db.tenders.create_index("tender_id", unique=True)

    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        try:
            await self.db.tenders.update_one(
                {'tender_id': adapter['tender_id']},
                {'$setOnInsert': adapter.asdict()},
                upsert=True
            )
        except Exception as e:
            spider.logger.error(f"MongoDB Error: {e}")
        return item