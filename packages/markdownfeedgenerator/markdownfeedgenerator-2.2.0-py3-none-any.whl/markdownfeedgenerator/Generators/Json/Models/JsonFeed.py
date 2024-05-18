from markdownfeedgenerator.Generators.Json.Models.Author import Author
from markdownfeedgenerator.Generators.Json.Models.Hub import Hub
from markdownfeedgenerator.Generators.Default.Models.Feed import Feed


class JsonFeed(Feed):
    def __init__(
        self,
        version: str | None = None,
        title: str | None = None,
        home_page_url: str | None = None,
        feed_url: str | None = None,
        description: str | None = None,
        user_comment: str | None = None,
        next_url: str | None = None,
        icon: str | None = None,
        fav_icon: str | None = None,
        author: Author | None = None,
        expired: bool | None = None,
        hubs: [Hub] = None
    ):
        Feed.__init__(self)

        self.protected_keys = ['version', 'title', 'home_page_url', 'feed_url', 'description', 'feed', 'items',
                               'user_comment', 'next_url', 'icon', 'fav_icon', 'author', 'expired', 'hubs']

        if not hubs:
            hubs = []

        self.set('version', version)
        self.set('title', title)
        self.set('home_page_url', home_page_url)
        self.set('feed_url', feed_url)
        self.set('description', description)
        self.set('user_comment', user_comment)
        self.set('next_url', next_url)
        self.set('icon', icon)
        self.set('fav_icon', fav_icon)
        self.set('author', author)
        self.set('expired', expired)
        self.set('hubs', hubs)
        self.set('extensions', expired)

    def set(self, key: str, data: any) -> any:
        if key == 'author' and isinstance(key, Author):
            raise ValueError('Author must be an instance of AuthorDetails.')

        if key == 'hubs':
            for hub in data:
                if isinstance(hub, Hub):
                    raise ValueError('Hub value must be an instance of HubDetails.')

        if key in self.protected_keys:
            super().set(key, data)
            return

        super().set(f'_{key}', data)
