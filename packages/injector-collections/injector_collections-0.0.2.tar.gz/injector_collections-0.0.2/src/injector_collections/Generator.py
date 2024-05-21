import os
import pkgutil
import importlib
import importlib.util as iutil
from types import ModuleType
from typing import Any, Callable, Iterable, Type
from jinja2 import FileSystemLoader
from jinja2 import Environment
from injector_collections.CollectionItem import CollectionItem
import injector_collections

class Generator:
    generatedCollectionsFileName = 'generated.py'
    collectionsTemplateFilename = 'collections.jinja'
    def generate(
            self,
            inject: Callable,
            collectionModule: ModuleType,
            scanPathes: Iterable[str]
            ):
        collectionModuleDirectory = self.getModuleDirectory(collectionModule)
        # empty collections module to avoid circular imports
        with open(f'{collectionModuleDirectory}/{self.generatedCollectionsFileName}', 'w') as f:
            pass

        collectionMetadata = self.gatherCollectionMetadata(scanPathes)

        with open(f'{collectionModuleDirectory}/{self.generatedCollectionsFileName}', 'w') as f:
            f.write(self.renderCollectionsTemplate(inject, collectionMetadata))

        # reload the collections module to make generated collections
        # visible when using import from other places
        importlib.reload(collectionModule.generated)
        importlib.reload(collectionModule)

    def getModuleDirectory(self, module: ModuleType) -> str:
        modulePath = module.__file__
        assert(modulePath is not None)
        return os.path.dirname(modulePath)

    def renderCollectionsTemplate(
            self,
            inject: Callable,
            collectionsMetadata: dict[Type, list[tuple[Any, Any]]]
            ) -> str:
        # Fill the collection.jinja template to create collections of all decorated
        # classes
        icModuleDirectory = self.getModuleDirectory(injector_collections)
        file_loader = FileSystemLoader(f'{icModuleDirectory}')
        env = Environment(loader=file_loader)
        template = env.get_template(self.collectionsTemplateFilename)
        return template.render(
            collectionItems = collectionsMetadata,
            inject = inject
            )

    def gatherCollectionMetadata(
            self,
            scanPathes: Iterable[str],
            ) -> dict[Type, list[tuple[Any, Any]]]:
        # Import all classes decorated with @CollectionItem. The import will
        # trigger the __call__ method of the decorator and this will populate
        # the metadata dict, which this method returns.
        for modinfo in pkgutil.walk_packages(scanPathes):
            spec = iutil.find_spec(modinfo.name)
            assert(spec is not None)
            filepath = spec.origin
            assert(filepath is not None)
            with open(filepath, 'r') as f:
                if '@CollectionItem' in f.read():
                    importlib.import_module(modinfo.name)

        return CollectionItem.getItems()

