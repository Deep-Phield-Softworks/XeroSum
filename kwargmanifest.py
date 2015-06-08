#!/usr/bin/env python

from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping as pdict
from persistent.list import PersistentList as plist
import transaction


from subclassloader import *


class Manifest_KWARG:

    def __init__(self):
        self.db_file = 'kwarg_manifest.fs'
        self.db = self.open(name,  db_file)
        self.types = ['Entity', 'Feature', 'Field', 'Item', 'Shape', 'Tile']
        for t in self.types:
            if t not in self.db:
                self.db[t] = OOBTree()

    def open(self, key, db_file):
            db = DB(FileStorage.FileStorage(db_file))
            cnx = db.open()
            root = cnx.root()
            if key not in root:
                root[key] = OOBTree()
                transaction.commit()
            return root[key]

    def get_kwargs(self, key, archetype=None):
        kwargs = None
        key = str(key)
        archtype = str(archetype)
        if archetype in self.db:
            kwargs = self.db[archetype][key]
        else:
            for archetype in self.db:
                if key in self.db[archetype]:
                    kwargs = self.db[archetype][key]
                    break
        return kwargs

    def set_kwargs(self, key,  archetype,  kwargs):
        set = False
        if isinstance(kwargs, dict):
            key = str(key)
            archtype = str(archetype)
            self.db[archetype][key] = kwargs
            set = True
        return set

kwarg_manifest = Manifest_KWARG()

"""If run as main, make a new kwarg_manifest.fs and populate it"""
if __name__ == "__main__":
    kwarg_manifest = Manifest_KWARG()

    """Make test items"""
    torch = {'class': Item, 'frame': (16, 6), 'weight': 3.0,  'use_frame': (16, 5)}
    kwarg_manifest.set_kwargs('torch',  'Item',  torch)
