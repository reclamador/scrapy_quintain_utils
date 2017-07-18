from datetime import datetime
import logging

from scrapy.exceptions import DropItem
import pymongo

class MongoPipeline(object):


    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = self.get_collection_name()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        saved_item = self.collection.find_one({"_id": item['id']})
        mongo_item = self.process_for_mongo(item)
        if saved_item:
            if saved_item == mongo_item:
                reason = "content already in mongo"
                logging.warning("Dropped %s.  Reason: %s" % (item, reason))
                raise DropItem
            else:
                self.collection.replace_one({"_id": mongo_item['_id']}, mongo_item, True)
        else:
            self.collection.insert_one(mongo_item)
        return item


    def transform_date(self, day, time):
        """
        Helper function
        :param day:
        :param time:
        :return:
        """
        return datetime.strptime(day + ' ' + time, '%d/%m/%y %H:%M')

    def process_for_mongo(self, item):
        """
        From item return Mongo element
        :param item:
        :return:
        """
        raise NotImplementedError

    def get_collection_name(self):
        """
        Return mongo collection name
        :return:
        """
        raise NotImplementedError
