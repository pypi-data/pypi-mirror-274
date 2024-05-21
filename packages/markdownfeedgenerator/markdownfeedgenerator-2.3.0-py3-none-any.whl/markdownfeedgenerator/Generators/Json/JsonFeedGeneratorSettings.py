from markdownfeedgenerator.Generators.Default.DefaultFeedGeneratorSettings import DefaultFeedGeneratorSettings


class JsonFeedGeneratorSettings(DefaultFeedGeneratorSettings):
    def __init__(
        self,
        async_work_group_size: int = 10,
        feed_items_per_export: int = 100,
        source_directory: str = None,
        target_directory: str = None,
        skip_files: list = None,
        feed_base_url: str = ''
    ):
        DefaultFeedGeneratorSettings.__init__(
            self, async_work_group_size, feed_items_per_export, source_directory, target_directory, skip_files)

        self.feed_base_url = feed_base_url
