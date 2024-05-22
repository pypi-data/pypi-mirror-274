# Injector Collections

This package adds collections to the
[Injector](https://github.com/python-injector/injector) python package. A
collection is an injectable class containing several other classes, which were
tagged using the `@CollectionItem` keyword and a designated `Collection`-class.

## Setup

To be able to use this package, You must create a new module-directory inside
your python project. The name of this module-directory does not matter, let's
name it `my_collections` here. Inside this module-directory the two submodules
(python-files) `generated.py` and `stubs.py` must be created. Also a module-file
`generate-collections.py` should be created.
The following file-tree will be the result:
```
my_collections
├── __init__.py
├── generate_collections.py
├── stubs.py
└── generated.py
```
Then include into `__init__.py` everything from `stubs` and `generated`:
```python
from injection.collections.stubs import *
import injection.collections.generate_collections
from injection.collections.generated import *
```
**Important:** Make sure, that You import the `generate_collections` module
before importing the generated collections, since otherwise of course you will
only have stubs on the first invokation.

## Usage / Example

Be sure to have done everything described in [Setup](#setup).

Let's say You have an application and want to add several plugins which are all
used in the app afterwards, but of course this list of plugins must be easily
extensible. You already use injector to instantiate your App:

```python
# app.py

from injector import inject

class App:
    @inject
     def __init__(self, '''plugins shall be injected here''', '''some other injected classes'''):
         # here comes some code

         def run(self):
             # plugins should be executed here
             # runs the app

from injector import Injector

injector = Injector()
outer = injector.get(App)
```

Now the first step is to create a stub collection for your plugins:
``` python
# my_collections/stub.py

from injector_collections import Collection

class PluginCollection(Collection):
    pass
```
**Note:** The collection class (here `PluginCollection`) should not have any
implementation. Currently any implementation will just be ignored and cannot be
used after the actual class was generated from the stub. The stubs sole purpose
is actually just to provied the LSP with some definitions, before the real
collection is generated.

Next add some Plugins as an example. And Tag them with `@PluginCollection` and
your previously defined `PluginCollection` as argument:
```python
# plugins.py

from injector_collections import CollectionItem
# the following line will import PluginCollection from stubs, if not yet
# existing or from the generated collections, if they were already generated.
from my_collections import PluginCollection

@CollectionItem(PluginCollection)
class HelloPlugin:
    def run(self):
        print("Hello Friends!")

@CollectionItem(PluginCollection)
class GoodbyPlugin:
    def run(self):
        print("Goodby Friends!")
```

**Important:** Currently you need to import `CollectionItem` literally, as the
code will be scanned for files containing the `@CollectionItem` string, which
will then be imported to auto-generate the collections!

Now we're almost done. We just have to make sure the plugins are generated when
**before** the application runs. Now we will edit the
`my_collections/generate_collections.py` to have it generate our
`PluginCollection`:
``` python
# generate_collections.py

from injector import inject
from injector_collections import generateCollections

# This auto-generates the real collections from the stubs. You need to provide
# the my_collections-module and a list of modules to scan for your collection
# items (in this case the plugins module suffices). If those modules are
# directories, all modules in them will be scanned recursively.
generateCollections(inject, "my_collections", ['plugins'])
```

Now you just need to import the `PluginCollection` to your `App` and use it:

```python
# app.py

from my_collections import PluginCollection

from plugins import HelloPlugin

from injector import inject

class App:
    @inject
     def __init__(self, plugins: PluginCollection, '''some other injected classes'''):
         # here comes some code
         self.plugins = plugins

         def run(self):
             # plugins.items contains a dict containing the plugins:
             for plugin in self.plugins.items.values():
                 plugin.run() # prints "Hello Friends!" and "Goodby Friends!"
             # Or just call a single plugin from the collection:
             self.plugins[HelloPlugin].run()
             # runs the app
...
```

### In Production

For a production system, just remove the generation of collections (in the
example remove the `import generate_collections` line) and just make sure to
check in the `my_collections` module. Because it suffices to generate the
collections once.
