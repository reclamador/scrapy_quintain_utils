from datetime import datetime
import logging

from scrapy.exceptions import DropItem
import pyrebase

class FirebasePipeline(object):

    def __init__(self, fb_apikey, fb_authDomain, fb_databaseUrl, fb_storageBucket, fb_user, fb_password):
        self.fb_apikey = fb_apikey
        self.fb_authDomain = fb_authDomain
        self.fb_databaseUrl = fb_databaseUrl
        self.fb_storageBucket = fb_storageBucket
        self.fb_user = fb_user
        self.fb_password = fb_password
        self.collection_name = self.get_collection_name()


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            fb_apikey=crawler.spider.fb_apikey,
            fb_authDomain=crawler.spider.fb_authDomain,
            fb_databaseUrl=crawler.spider.fb_databaseUrl,
            fb_storageBucket=crawler.spider.fb_storageBucket,
            fb_user=crawler.spider.fb_user,
            fb_password=crawler.spider.fb_password
        )

    def open_spider(self, spider):
        config = {
            "apiKey": self.fb_apikey,
            "authDomain": self.fb_authDomain,
            "databaseURL": self.fb_databaseUrl,
            "storageBucket": self.fb_storageBucket
        }

        # Init firebase
        self.firebase = pyrebase.initialize_app(config)

        # Get a reference to the auth service
        auth = self.firebase.auth()

        # Log the user in
        self.user = auth.sign_in_with_email_and_password(self.fb_user, self.fb_password)

        # Get a reference to the database service
        self.db = self.firebase.database()


    def process_item(self, item, spider):
        # Does the item already exist?
        item_by_id = self.db.child(item["id"]).get(token=self.user['idToken'])
        saved_item = item_by_id.val()
        firebase_item = self.process_for_firebase(saved_item)

        if saved_item:
            if saved_item == firebase_item:
                # Drop duplicated item
                reason = "content already in firebase"
                logging.warning("Dropped %s.  Reason: %s" % (item, reason))
                raise DropItem
            else:
                # Update
                self.db.child(item["id"]).update(dict(firebase_item), token=self.user["idToken"])

        # Just add new one
        else:
            self.db.child(item["id"]).set(dict(firebase_item), token=self.user["idToken"])

        return item



    def transform_date(self, day, time):
        """
        Helper function
        :param day:
        :param time:
        :return:
        """
        return datetime.strptime(day + ' ' + time, '%d/%m/%y %H:%M')

    def process_for_firebase(self, item):
        """
        From item return Firebase element
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
