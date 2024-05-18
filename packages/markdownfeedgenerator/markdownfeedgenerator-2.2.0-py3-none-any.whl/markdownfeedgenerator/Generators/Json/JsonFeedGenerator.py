import json
import logging
import os

from markdownfeedgenerator import write_to_file
from markdownfeedgenerator.Generators.Json import JsonFeedGeneratorSettings
from markdownfeedgenerator.Generators.Json.Models.JsonFeed import JsonFeed
from markdownfeedgenerator.Generators.Json.Models.JsonFeedItem import JsonFeedItem
from markdownfeedgenerator.MarkdownFile import MarkdownFile
from markdownfeedgenerator.Generators.Default.DefaultFeedGenerator import DefaultFeedGenerator
from markdownfeedgenerator.Generators.Default.Models.Feed import Feed


class JsonFeedGenerator(DefaultFeedGenerator):
    # JSON Feed version
    JSON_FEED_VERSION = f'https://jsonfeed.org/version/1'

    def __init__(self, feed_details: JsonFeed, generator_settings: JsonFeedGeneratorSettings):
        """
        Constructor
        """
        feed_details.set('version', JsonFeedGenerator.JSON_FEED_VERSION)
        DefaultFeedGenerator.__init__(self, feed_details, generator_settings)
        self.generator_settings = generator_settings

    def _check_settings(self):
        """
        Check feed settings
        """
        if not self.generator_settings.source_directory:
            self.generator_settings.source_directory = os.getcwd()

        if not self.generator_settings.target_directory:
            self.generator_settings.target_directory = os.path.join(os.getcwd(), 'feed')

    def _create_feed(self) -> JsonFeed:
        """
        Create a new feed instance.
        """
        return JsonFeed()

    def _markdown_file_to_feed_item(self, markdown_file: MarkdownFile) -> JsonFeedItem:
        """
        Convert a markdown file to a feed item.
        """
        feed_item = JsonFeedItem()
        feed_item.set('id', markdown_file.id)
        feed_item.set('url', markdown_file.file_path)
        feed_item.set('date_published', markdown_file.date.isoformat() if markdown_file.date else None)
        feed_item.set('summary', markdown_file.summary)
        feed_item.inject(markdown_file.front_matter)
        feed_item = self._inject_feed_item_details(feed_item, markdown_file)
        return feed_item

    def _inject_feed_item_details(
            self, feed_item_details: JsonFeedItem, markdown_file: MarkdownFile) -> JsonFeedItem:
        """
        Inject any additional feed item details.
        """
        return feed_item_details

    def _export_feed(self, feed: Feed):
        """
        Export a feed.
        """
        feed_url = 'feed.json' if feed.page == 1 else f'{feed.page - 1}.json'
        next_feed_url = f'{feed.page}.json' if feed.page < feed.total_pages else None
        feed_file_target = os.path.join(self.generator_settings.target_directory, feed_url)

        if self.generator_settings.feed_base_url:
            feed_url = f'{self.generator_settings.feed_base_url}/{feed_url}'

        if self.generator_settings.feed_base_url and next_feed_url:
            next_feed_url = f'{self.generator_settings.feed_base_url}/{next_feed_url}'

        feed.set('feed_url', feed_url)
        feed.set('next_url', next_feed_url)

        write_to_file(
            feed_file_target, json.dumps(feed.dump(), indent=2))

        logging.info(
            f'Successfully wrote feed page to "{feed_file_target}".')
