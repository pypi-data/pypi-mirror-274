from markdownfeedgenerator.Generators.Json.Models import JsonFeedItemStore


class AuthorDetails(JsonFeedItemStore):
    """
    Represents the properties of an author.
    """
    def __init__(
        self,
        name: str = None,
        url: str = None,
        avatar: str = None
    ):
        JsonFeedItemStore.__init__(self, ['name', 'url', 'avatar'])

        self.set('name', name)
        self.set('url', url)
        self.set('avatar', avatar)

    def check(self):
        if not self.has('name') and not self.has('url') and not self.has('avatar'):
            raise ValueError('You must provide a value for at least one of the "name", "url" or "avatar" properties.')
