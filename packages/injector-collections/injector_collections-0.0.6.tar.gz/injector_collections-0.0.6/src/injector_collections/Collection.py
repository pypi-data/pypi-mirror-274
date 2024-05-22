from typing import Type
from injector_collections.CollectionItem import CollectionItem

class Collection:
    def __init__(self):
        self._items: dict[Type[CollectionItem], CollectionItem] = {}

    @property
    def items(self) -> dict[Type[CollectionItem], CollectionItem]:
        return self._items

    def __getitem__(self, key):
        return self._items[key]

    def __setitem__(self, key, item):
        self._items[key] = item
