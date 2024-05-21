import logging
import os

import chevron

from markdownfeedgenerator import write_to_file, read_from_file
from markdownfeedgenerator.Generators.Default.Models.Feed import Feed
from markdownfeedgenerator.Generators.Json.JsonFeedGenerator import JsonFeedGenerator
from markdownfeedgenerator.Generators.Json.JsonFeedGeneratorSettings import JsonFeedGeneratorSettings
from markdownfeedgenerator.Generators.Json.Models.JsonFeed import JsonFeed


class HtmlFeedGenerator(JsonFeedGenerator):
    # Default template path
    DEFAULT_TEMPLATE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'template.html')

    def __init__(
        self,
        feed: JsonFeed = None,
        generator_settings: JsonFeedGeneratorSettings = None,
        template_file_path: str = None
    ):

        JsonFeedGenerator.__init__(self, feed, generator_settings)
        self.template_file_path = template_file_path

    async def _export_feed(
        self,
        feed: Feed
    ):
        """
        Export a feed.
        """
        feed_url = self.get_feed_page_name(feed.page)
        next_feed_url = self.get_feed_page_name(feed.page + 1) if (feed.page + 1) < feed.total_pages else None
        previous_feed_url = self.get_feed_page_name(feed.page - 1) if feed.page > 1 else None
        feed_file_target = os.path.join(self.generator_settings.target_directory, feed_url)

        if self.generator_settings.feed_base_url:
            previous_feed_url = self.generator_settings.feed_base_url + '/' + previous_feed_url

        if self.generator_settings.feed_base_url:
            next_feed_url = self.generator_settings.feed_base_url + '/' + next_feed_url

        template = read_from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'template.html'))

        content = chevron.render(
            template, {
                **{'nextPageUrl': next_feed_url, 'previousPageUrl': previous_feed_url, 'title': feed.get('title'),
                    'files': [f.dump() for f in feed.items]}, **feed.dump()})

        write_to_file(feed_file_target, content)

        logging.info(f'Successfully wrote feed page to "{feed_file_target}".')

    @staticmethod
    def get_feed_page_name(
        page_number: int
    ) -> str:
        if page_number <= 1:
            return 'index.html'

        return f'{page_number}.html'
