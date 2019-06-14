from w3lib.http import basic_auth_header
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from scrapy.pipelines.files import S3FilesStore
from scrapy_splash import SplashRequest


class ScreenshotPipeline(object):
    """
    Download screenshot by splash
    """
    DEFAULT_SPLASH_ARGS = {'html': 1,
                           'png': 1,
                           'width': 600,
                           'render_all': 1,
                           'wait': 1.5}

    DEFAULT_S3_HEADERS = {}



    def __init__(self, store_uri, s3store, api_key_splash, splash_args, s3_headers, settings):
        self.settings = settings
        self.store = s3store(store_uri)
        self.api_key_splash = api_key_splash
        self.splash_args = splash_args
        self.s3_headers = s3_headers

    @classmethod
    def from_settings(cls, settings):
        s3store = S3FilesStore
        s3store.AWS_ACCESS_KEY_ID = settings['AWS_ACCESS_KEY_ID']
        s3store.AWS_SECRET_ACCESS_KEY = settings['AWS_SECRET_ACCESS_KEY']
        s3store.POLICY = settings['IMAGES_STORE_S3_ACL']
        api_key_splash = settings['API_KEY']
        store_uri = settings['IMAGES_STORE']
        splash_args = settings.get('SCREENSHOT_PIPELINE_SPLASH_ARGS', cls.DEFAULT_SPLASH_ARGS)
        s3_headers = settings.get('SCREENSHOT_PIPELINE_S3_HEADERS', cls.DEFAULT_S3_HEADERS)
        return cls(store_uri, s3store, api_key_splash, splash_args, s3_headers, settings=settings)

    def process_item(self, item, spider):
        self.spider = spider

        request = SplashRequest(
                        self.get_url(item),
                        endpoint='render.json',
                        args=self.splash_args,
                        splash_headers={
                            'Authorization': basic_auth_header(self.api_key_splash, ''),
                        },
                    )
        dfd = spider.crawler.engine.download(request, spider)
        dfd.addBoth(self.return_item, item)
        return dfd

    def return_item(self, response, item):
        import base64
        if response.status != 200:
            # Error happened, return item.
            return item
        png_bytes = base64.b64decode(response.data['png'])
        name = self.get_file_name(item)

        self.store.persist_file(name, BytesIO(png_bytes), info=None, headers=self.s3_headers)
        # Store filename in item.
        item = self.update_item_with_s3_key(name, item)
        self.inc_stats(self.spider, 'uptodate')
        return item

    def inc_stats(self, spider, status):
        spider.crawler.stats.inc_value('screenshot_count', spider=spider)
        spider.crawler.stats.inc_value('screenshot_status_count/%s' % status, spider=spider)

    def get_url(self, item):
        """
        Implement this method to obtain url to take screenshot from item
        :param item:
        :return:
        """
        raise NotImplementedError

    def get_file_name(self, item):
        """
        Implement this method to obtain file name to store in S3
        :param item:
        :return:
        """
        raise NotImplementedError

    def update_item_with_s3_key(self, s3_key, item):
        """
        Implement this method to update item with s3 key saved
        :param file_name:
        :return:
        """
        return item
