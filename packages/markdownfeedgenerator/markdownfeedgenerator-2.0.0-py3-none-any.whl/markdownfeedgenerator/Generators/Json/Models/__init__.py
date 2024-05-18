from markdownfeedgenerator.Generators.Default.Models import ItemStore


class JsonFeedItemStore(ItemStore):
    def __init__(self, protected_keys: list = None):
        ItemStore.__init__(self)

        if not protected_keys:
            protected_keys = []

        self.protected_keys = protected_keys

    def set(self, key: str, data: any) -> any:
        if key in self.protected_keys:
            super().set(key, data)
            return

        super().set(f'_{key}', data)
