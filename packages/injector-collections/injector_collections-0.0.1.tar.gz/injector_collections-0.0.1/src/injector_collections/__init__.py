from types import ModuleType
from typing import Callable, Iterable
from injector_collections.Generator import Generator
from Collection import Collection
from CollectionItem import CollectionItem

def generateCollections(
        inject: Callable,
        collectionModule: ModuleType,
        scanPathes: Iterable[str]):
    generator = Generator()
    generator.generate(inject, collectionModule, scanPathes)
