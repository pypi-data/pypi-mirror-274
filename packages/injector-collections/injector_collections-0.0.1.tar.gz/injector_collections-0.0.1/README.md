# Injector Collections

This package adds collections to the
[Injector](https://github.com/python-injector/injector) python package. A
collection is an injectable class containing several other classes, which were
tagged using the `@CollectionItem` keyword and a designated `Collection`-class.

## Setup

To be able to use this package, You must create a new module-directory inside
your python project. The name of this module-directory does not matter, let's
name it `collections` here. Inside this module-directory the two submodules
(python-files) `generated.py` and `stubs.py` must be created. The following
file-tree will be the result:
```
collections
├── generated.py
├── __init__.py
└── stubs.py
```
Then include into `__init__.py` everything from `stubs` and `generated`:
```python
from collections.stubs import *
from collections.generated import *
```
Make sure, that `collections.generated` is imported last, since it shall
overwrite the collections from `collections.stubs`.

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
# collections/stub.py

from injector_collections import Collection

class PluginCollection(Collection)
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
from collections import PluginCollection

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
code will be scanned for files containing the `CollectionItem` keyword, which
must then be imported to auto-generate the collections!

Now we're almost done. We just have to make sure the plugins are generated when
**before** the application runs. Let's create first another module for this:
``` python
# generate_collections.py

import os
from injector import inject
from injector_collections import generateCollections
import collections

scandir = os.path.dirname(__file__)
# This auto-generates the real collections from the stubs. You need to provide
# the collections-module You created during setup and a list of directories to
# scan (recursively) for your collection items.
generateCollections(inject, collections, [scandir])
```

Now you only need to import `generate_collections` and of course the collection
itself to your `App` and use it:

```python
# app.py

import generate_collections
from collections import PluginCollection

from plugins import HelloPlugin

from injector import inject

class App:
    @inject
     def __init__(self, plugins: PluginCollection, '''some other injected classes'''):
         # here comes some code
         self.plugins = plugins

         def run(self):
             # plugins.items contains a dict containing the plugins:
             for plugin in plugins.items.values():
                 plugin.run() # prints "Hello Friends!" and "Goodby Friends!"
             # Or just call a single plugin from the collection:
             plugins[HelloPlugin].run()
             # runs the app
...
```
**Important:** `PluginCollection` and other collections must be imported only
after they were generated (by `generate_collections`). Otherwise You will just
have the stubs imported (if not generated previously).

### In Production

For a production system, just remove the generation of collections and just
make sure to check in the generated collections module. Because it suffices to
generate the collections once.
