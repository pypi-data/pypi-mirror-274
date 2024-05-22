from typing import Callable, Iterable
from injector_collections.Generator import Generator
from injector_collections.Collection import Collection
from injector_collections.CollectionItem import CollectionItem

def generateCollections(
        inject: Callable,
        collectionModule: str,
        scannedModules: Iterable[str]):
    generator = Generator()
    generator.generate(inject, collectionModule, scannedModules)
