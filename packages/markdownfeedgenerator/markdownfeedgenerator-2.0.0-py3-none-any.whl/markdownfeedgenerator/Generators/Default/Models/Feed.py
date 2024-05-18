from markdownfeedgenerator.Generators.Default.Models import ItemStore
from markdownfeedgenerator.Generators.Default.Models.FeedItem import FeedItem


class Feed(ItemStore):
    def __init__(self, items: dict = None):
        ItemStore.__init__(self)

        self.feed_items: [FeedItem] = []
        self.page = None
        self.total_pages = None
        self.total_items = None

        if items:
            self.inject(items)

    def check(self):
        if not self.has('title'):
            raise ValueError('The feed item does not have a valid title.')

    def dump(self) -> dict:
        self.set('items', [x.dump() for x in self.feed_items])
        self.set('page', self.page)
        self.set('total_pages', self.total_pages)
        self.set('total_items', self.total_items)
        return super().dump()
