#!/usr/bin/env python
from persistent.mapping import PersistentMapping as pdict


"""
Effect class stores and yields information related to effects.
Effects are usually applied to the contents of a Shape object.
They can also be applied to a Matter subclass which then
becomes responsible for containing and managing them.

Effects use kwarg dictionaries to initialize them. This uses the
self.accepted_kwargs inheritance scheme similar to the other
archetypes. However, Effects process their kwargs slightly
differently. Specifically, Effects only set as attributes kwargs
key value pairs where the boolean of the value is True. (So the
value must not be False, None, 0, etc). This facilitates the testing
of the attributes of an Effect through the use of a boolean. IE if
a duration would be 0, it will just not be stored as an attribute. Also,
if a dictionary is contained within the kwargs, it will be stored in
self.contents as a dict. When the Effect is "applied" it will yield up
its self.contents as a list of dictionaries.
"""


class Effect:

    def __init__(self,  **kwargs):
        self.accepted_kwargs = {'type': 'damage',
                                                 'image_key': 'icons.png',
                                                 'frame': (0, 0),
                                                 'magnitude': 1,
                                                 'duration': 0,
                                                 'tick_threshold': 0,
                                                 'tick_accumulator': 0
                                                }
        self.contents = pdict({})
        for k in self.accepted_kwargs:
            if k in kwargs:
                if bool(kwargs[k]):
                    self.contents[0][k] = kwargs[k]
            elif isinstance(k,  dict):
                if bool(kwargs[k]):
                    self.contents[len(self.contents)] = self.store(**k)

    def store(self,  **kwargs):
        d = {}
        for k in kwargs:
            if bool(kwargs[k]):
                d[k] = kwargs[k]
        return d

    def yield_effects(self):
        return [self.contents[k] for k in self.contents]
