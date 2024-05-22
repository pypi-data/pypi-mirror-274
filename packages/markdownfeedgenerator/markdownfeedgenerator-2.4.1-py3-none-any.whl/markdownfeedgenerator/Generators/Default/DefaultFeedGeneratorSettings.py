import json
import os


class DefaultFeedGeneratorSettings:
    def __init__(
        self,
        async_work_group_size: int = 10,
        feed_items_per_export: int = 100,
        source_directory: str = None,
        target_directory: str = None,
        skip_files: list = None
    ):
        self.async_work_group_size = async_work_group_size
        self.feed_items_per_export = feed_items_per_export
        self.source_directory = source_directory
        self.target_directory = target_directory

        if self.source_directory:
            self.source_directory = self.source_directory.rstrip(os.sep)

        if self.target_directory:
            self.target_directory = self.target_directory.rstrip(os.sep)

        self.skip_files = skip_files

        if not self.skip_files:
            self.skip_files = []

    def check(
        self
    ):
        pass

    def __str__(
        self
    ):
        return json.dumps(
            {'work_group_size': self.async_work_group_size, 'feed_items_per_export': self.feed_items_per_export,
             'source_directory': self.source_directory, 'target_directory': self.target_directory, })
