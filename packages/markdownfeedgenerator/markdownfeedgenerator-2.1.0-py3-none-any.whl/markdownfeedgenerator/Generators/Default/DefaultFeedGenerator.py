import asyncio
import json
import os
import logging
from pathlib import Path
from typing import Callable

from math import ceil

from markdownfeedgenerator.MarkdownFile import MarkdownFile
from markdownfeedgenerator.Generators.Default.DefaultFeedGeneratorSettings import DefaultFeedGeneratorSettings
from markdownfeedgenerator.Generators.Default.Models import ItemStore
from markdownfeedgenerator.Generators.Default.Models.Feed import Feed
from markdownfeedgenerator.Generators.Default.Models.FeedItem import FeedItem


class DefaultFeedGenerator:
    def __init__(self, feed_details: Feed = None, generator_settings: DefaultFeedGeneratorSettings = None):
        if not feed_details:
            feed_details = ItemStore()
            feed_details.set('title', 'Untitled Feed')

        if not generator_settings:
            generator_settings = DefaultFeedGeneratorSettings()

        logging.info(f'Using generator with settings: "{str(generator_settings)}"')

        self.feed_details = feed_details
        self.generator_settings = generator_settings

        self._check_settings()

    async def run(self) -> None:
        # Discover markdown file paths
        markdown_file_paths = DefaultFeedGenerator.discover_markdown_file_paths(
            self.generator_settings.source_directory, self.generator_settings.skip_files)

        # Convert a list of file paths into a list of markdown files, async chunked work
        markdown_files = await DefaultFeedGenerator.chunked_work(
            markdown_file_paths, self._file_paths_to_markdown_files, self.generator_settings.async_work_group_size)

        # Convert a list of markdown files into a list of feed items, async chunked work
        feed_items = await DefaultFeedGenerator.chunked_work(
            markdown_files, self._markdown_files_to_feed_items, self.generator_settings.async_work_group_size)

        # Sort the feed items
        feed_items = self._sort_feed_items(feed_items)

        # Page tracking
        current_page = 1
        feed_items_per_export = self.generator_settings.feed_items_per_export
        total_pages = ceil(len(feed_items) / feed_items_per_export) if feed_items_per_export else 1

        # Convert feed items into a feed and export the feed
        for chunked_feed_items in DefaultFeedGenerator.chunk(feed_items, feed_items_per_export):
            # Convert feed items into a feed
            feed = self._feed_items_to_feed(
                chunked_feed_items, current_page, total_pages, len(feed_items))

            # Check the feed is valid
            feed.check()

            logging.info(f'Successfully created feed with {len(feed.feed_items)} items.')

            # Export the feed
            self._export_feed(feed)

            current_page += 1

    def run_standalone(self):
        """
        Run this in synchronous mode.
        """
        logging.info(f'Running feed generator in standalone mode.')
        asyncio.run(self.run())

    def _check_settings(self):
        """
        Check the settings to ensure they contain the correct values for this generator.
        """
        pass

    def _check_feed_item(self, feed_item: FeedItem):
        """
        Check if a feed item is valid or not.
        """
        pass

    def _sort_feed_items(self, feed_items: [FeedItem]) -> [FeedItem]:
        """
        Sort a list of feed items. Override this to provided custom sorting.
        """
        return feed_items

    def _process_markdown_file(self, markdown_file: MarkdownFile) -> MarkdownFile:
        """
        Perform any needed processing on a markdown file.
        """
        return markdown_file

    def _file_path_to_markdown_file(self, file_path: str) -> MarkdownFile:
        """
        Convert a file path to a markdown file.
        """
        return MarkdownFile.load(file_path)

    def _markdown_file_to_feed_item(self, markdown_file: MarkdownFile) -> FeedItem:
        """
        Convert a markdown file to a feed item.
        """
        feed_item = FeedItem()
        feed_item.set('url', markdown_file.file_path)
        feed_item.inject(markdown_file.front_matter)
        return feed_item

    async def _file_paths_to_markdown_files(self, file_paths: [str]) -> [MarkdownFile]:
        """
        Convert a list of file paths into a list of markdown files.
        """
        markdown_files = []

        for file_path in file_paths:
            markdown_file = self._file_path_to_markdown_file(file_path)

            logging.info(f'Successfully converted file path "{file_path}" to markdown file.')

            markdown_file = self._process_markdown_file(markdown_file)

            logging.info(f'Successfully processed markdown file "{markdown_file.file_path}".')

            markdown_files.append(markdown_file)

        return markdown_files

    async def _markdown_files_to_feed_items(self, markdown_files: [MarkdownFile]) -> [FeedItem]:
        """
        Convert a list of file paths into a list of markdown files.
        """
        feed_items = []

        for markdown_file in markdown_files:
            feed_items.append(
                self._markdown_file_to_feed_item(markdown_file))

            logging.info(f'Successfully converted markdown file "{markdown_file.file_path}" to feed item.')

        # Check all the feed items are valid
        [self._check_feed_item(feed_item) for feed_item in feed_items]

        return feed_items

    def _feed_items_to_feed(self, feed_items: [FeedItem], page: int, total_pages: int, total_items: int) -> Feed:
        """
        Convert a list of feed items to a feed.
        """
        feed = self._create_feed()
        feed.page = page
        feed.feed_items = feed_items
        feed.total_pages = total_pages
        feed.total_items = total_items
        feed.merge(self.feed_details)
        return feed

    def _create_feed(self) -> Feed:
        """
        Create a new feed instance.
        """
        return Feed()

    def _export_feed(self, feed: Feed):
        """
        Export a feed.
        """
        print(json.dumps(feed.dump(), indent=2))

    @staticmethod
    async def chunked_work(work_items: list, process_list_fn: Callable, work_size: int = 10) -> list:
        """
        This function takes a list of work items, chunks them into lists of a specified size and then
        calls a process callback function over each of those chunks. This function allows you to run chunks of work
        in parallel. The function will then await completion of all the work chunks and return the processed list.
        """
        futures = []
        for file_list_chunk in DefaultFeedGenerator.chunk(work_items, work_size):
            futures.append(
                process_list_fn(file_list_chunk))

        processed = []
        for work_group in await asyncio.gather(*futures):
            processed += [m for m in work_group]

        logging.info(f'Successfully completed work on {len(work_items)} work items.')

        return processed

    @staticmethod
    def discover_markdown_file_paths(directory_path: str, skip_files: list = None) -> [str]:
        """
        Discover all markdown files within a provided directory, skipping some files if needed.
        """
        if skip_files is None:
            skip_files = []

        if not os.path.isdir(directory_path):
            raise Exception(f'The provided path "{directory_path}", must be a directory.')

        return list(filter(
                lambda x: os.path.basename(x) not in skip_files,
                [str(path) for path in Path(directory_path).glob('**/*.md')]))

    @staticmethod
    def chunk(items: list, length: int = None) -> list:
        """
        Chunk a list into a specific length. If no length is provided, just yield the original list.
        """
        if length is None:
            yield items
            return

        for i in range(0, len(items), length):
            yield items[i:i + length]
