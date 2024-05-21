from markdownfeedgenerator.Generators.Json.Models import JsonFeedItemStoreSync


class Author(JsonFeedItemStoreSync):
    """
    Represents the properties of an author.
    """

    def __init__(
        self,
        name: str = None,
        url: str = None,
        avatar: str = None
    ):
        JsonFeedItemStoreSync.__init__(self, ['name', 'url', 'avatar'])

        self.name = name
        self.url = url
        self.avatar = avatar

    def check(
        self
    ):
        if not self.has_value('name') and not self.has_value('url') and not self.has_value('avatar'):
            raise ValueError('You must provide a value for at least one of the "name", "url" or "avatar" properties.')

        super().check()
