import logging

from scrapy.exceptions import DropItem


class CompletnessPipeline(object):
    """
    Check all sensible data in item is present
    """


    def process_item(self, item, spider):
        required_fields = self.get_required_fields(item)
        for req in required_fields:
            reason = None
            if callable(req):
                if not req(item):
                    reason = req.__name__
            else:
                if req not in item or not item[req]:
                    reason = "required_%s" % req
            if reason:
                logging.warning("Dropped %s.  Reason: %s" % (item, reason))
                raise DropItem
        item = self.post_process_item(item)
        return item


    def get_required_fields(self, item):
        """
        Implement this method to obtain fields and function(item) to validate
        :param item:
        :return:
        """
        raise NotImplementedError

    def post_process_item(self, item):
        """
        Implement this method when wanting to change item after validation is correct.
        i.e. generate new id
        :param item:
        :return: Item
        """
        return item
