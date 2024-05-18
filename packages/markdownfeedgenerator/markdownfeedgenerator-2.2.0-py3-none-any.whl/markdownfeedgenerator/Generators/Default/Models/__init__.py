class ItemStore:
    def __init__(self, initial_values: dict = None):
        if initial_values:
            self.store = initial_values
        else:
            self.store = {}

    def set(self, key: str, data: any) -> any:
        self.store[key] = data

    def has(self, key: str) -> bool:
        return key in self.store

    def get(self, key: str) -> any:
        if not self.has(key):
            raise ValueError(f'Feed details store contains no value with key "{key}".')

        return self.store[key]

    def inject(self, values_to_inject: dict):
        for key in values_to_inject:
            self.set(key, values_to_inject[key])

    def merge(self, item_store: any):
        self.store = {**self.store, **item_store.store}

    def dump(self) -> dict:
        dump = {}
        for key in self.store:
            value = self.store[key]

            if isinstance(value, ItemStore):
                dump[key] = value.dump()
            elif isinstance(value, list):
                if len(value) > 0:
                    dump[key] = value
            elif value is not None:
                dump[key] = value

        return dump
