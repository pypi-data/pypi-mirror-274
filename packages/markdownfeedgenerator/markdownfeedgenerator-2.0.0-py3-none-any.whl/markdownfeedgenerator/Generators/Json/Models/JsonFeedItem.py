from markdownfeedgenerator.Generators.Json.Models import JsonFeedItemStore
from markdownfeedgenerator.Generators.Json.Models.AuthorDetails import AuthorDetails


class JsonFeedItem(JsonFeedItemStore):
    def __init__(
        self,
        id: str | None = None,
        url: str | None = None,
        external_url: str | None = None,
        title: str | None = None,
        content_html: str | None = None,
        content_text: str | None = None,
        summary: str | None = None,
        image: str | None = None,
        banner_image: str | None = None,
        date_published: str | None = None,
        date_modified: AuthorDetails | None = None,
        author: AuthorDetails | None = None,
        tags: [str] = None
    ):
        JsonFeedItemStore.__init__(self, ['id', 'url', 'external_url', 'title', 'content_html', 'content_text',
                                          'summary', 'image', 'banner_image', 'date_published', 'date_modified',
                                          'author', 'tags'])

        if not tags:
            tags = []

        self.set('id', id)
        self.set('url', url)
        self.set('external_url', external_url)
        self.set('title', title)
        self.set('content_html', content_html)
        self.set('content_text', content_text)
        self.set('summary', summary)
        self.set('image', image)
        self.set('banner_image', banner_image)
        self.set('date_published', date_published)
        self.set('date_modified', date_modified)
        self.set('author', author)
        self.set('tags', tags)

