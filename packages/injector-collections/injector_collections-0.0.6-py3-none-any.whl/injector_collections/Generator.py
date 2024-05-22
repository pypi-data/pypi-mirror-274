import os
import pkgutil
import importlib
from types import ModuleType
from typing import Any, Callable, Iterable, Type
from jinja2 import FileSystemLoader
from jinja2 import Environment
from injector_collections.CollectionItem import CollectionItem
import injector_collections
from importlib import util

class Generator:
    generatedCollectionsFileName = 'generated.py'
    collectionsTemplateFilename = 'collections.jinja'
    def generate(
            self,
            inject: Callable,
            collectionModule: str,
            scannedModules: Iterable[str]
            ):
        collectionModuleDirectory = self.getModuleDirectory(collectionModule)
        # empty collections module to avoid circular imports
        with open(f'{collectionModuleDirectory}/{self.generatedCollectionsFileName}', 'w') as f:
            pass

        collectionMetadata = self.gatherCollectionMetadata(scannedModules)

        with open(f'{collectionModuleDirectory}/{self.generatedCollectionsFileName}', 'w') as f:
            f.write(self.renderCollectionsTemplate(inject, collectionMetadata))

        # reload the collections module to make generated collections
        # visible when using import from other places
        # collectionModule = importlib.import_module(collectionModule)
        # importlib.reload(collectionModule.generated)
        # importlib.reload(collectionModule)

    def getModuleDirectory(self, module: str|ModuleType) -> str:
        if isinstance(module, str):
            moduleSpec = util.find_spec(module)
            modulePath = moduleSpec.origin
        else:
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
            scannedModules: Iterable[str],
            ) -> dict[Type, list[tuple[Any, Any]]]:
        ''' Gather Metadata for Collection generation with template

        Recursively walks through all modules in 'scannedModules' and gathers
        metadata for every class decorated with '@CollectionItem'.
        '''
        for m in scannedModules:
            for spec in self.walkModules(m):
                with open(spec.origin, 'r') as f:
                    if '@CollectionItem' in f.read():
                        importlib.import_module(spec.name)

        return CollectionItem.getItems()

    def walkModules(self, rootModule: str):
        info = util.find_spec(rootModule)
        yield info

        if info.submodule_search_locations is None:
            return

        #for modinfo in pkgutil.walk_packages(info.submodule_search_locations):
        for modinfo in pkgutil.iter_modules(info.submodule_search_locations):
            name = f'{info.name}.{modinfo.name}'
            yield util.find_spec(name)
            submods = self.walkModules(name)
            next(submods) # remove the root, which was just yielded
            for mi in submods:
                yield mi
