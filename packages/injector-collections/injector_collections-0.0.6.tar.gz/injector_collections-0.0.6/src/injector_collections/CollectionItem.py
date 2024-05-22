from typing import Any, Type, TypeVar

T = TypeVar('T')

class CollectionItem:
    _items: dict[Type, list[tuple[Any, Any]]] = {}

    def __init__(self, collectionClass: Type):
        self._collectionClass: Type = collectionClass

    def __call__(self, classVar: Type[T]) -> Type[T]:
        if self._collectionClass not in self._items:
            self._items[self._collectionClass] = []

        self._items[self._collectionClass].append((classVar.__name__, classVar))

        return classVar

    @classmethod
    def getItems(cls) -> dict[Type, list[tuple[Any, Any]]]:
        return cls._items
