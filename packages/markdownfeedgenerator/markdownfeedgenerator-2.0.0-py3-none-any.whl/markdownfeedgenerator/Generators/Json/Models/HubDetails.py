from markdownfeedgenerator.Generators.Json.Models import JsonFeedItemStore


class HubDetails(JsonFeedItemStore):
    """
    Represents the properties of a hub.
    """
    def __init__(
        self,
        hub_type: str = None,
        url: str = None
    ):
        JsonFeedItemStore.__init__(self, ['type', 'url'])

        self.set('type', hub_type)
        self.set('url', url)

    def check(self):
        if not self.has('type') or not self.has('url'):
            raise ValueError('You must provide a valid value for both "type" and "url".')
