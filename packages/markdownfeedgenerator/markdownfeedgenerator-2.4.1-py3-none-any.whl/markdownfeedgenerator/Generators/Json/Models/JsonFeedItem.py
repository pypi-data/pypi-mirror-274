from markdownfeedgenerator.Generators.Json.Models import JsonFeedItemStoreSync
from markdownfeedgenerator.Generators.Json.Models.Author import Author


class JsonFeedItem(JsonFeedItemStoreSync):
    def __init__(
        self,
        _id: str | None = None,
        url: str | None = None,
        external_url: str | None = None,
        title: str | None = None,
        content_html: str | None = None,
        content_text: str | None = None,
        summary: str | None = None,
        image: str | None = None,
        banner_image: str | None = None,
        date_published: str | None = None,
        date_modified: Author | None = None,
        author: Author | None = None,
        tags: [str] = None
    ):
        JsonFeedItemStoreSync.__init__(
            self,
            ['id', 'url', 'external_url', 'title', 'content_html', 'content_text', 'summary', 'image', 'banner_image',
             'date_published', 'date_modified', 'author', 'tags'])

        # Mostly for convenience, we could also just use the store, but this makes it easier for JsonFeedItem references
        # to know exactly what can be customized.
        self.id = _id
        self.url = url
        self.external_url = external_url
        self.title = title
        self.content_html = content_html
        self.content_text = content_text
        self.summary = summary
        self.image = image
        self.banner_image = banner_image
        self.date_published = date_published
        self.date_modified = date_modified
        self.author = author
        self.tags = tags if tags else []
