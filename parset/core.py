# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
This is an Astropy affiliated package.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from collections import OrderedDict
import traitlets
from . import pyaml as y
import ruamel.yaml as ry
import six

class ParSet(traitlets.HasTraits):

#    def __init__(self):
#        super(ParSet, self).__init__()
#        self.trait_values = OrderedDict()

    def value_dict(self):
        '''
        Return a dictionary of all the traits keyed by name, and the values 
        being the current trait value (not class or type).
        ''' 
        return self._trait_values

    def ynode(self):
        tlist = []
        vdict = self.value_dict()
        tdict = self.traits()
        keys = self.trait_names()
        for key in keys:
            tlist.append((y.YScalarStr(key), 
                tdict[key].ynode(vdict[key])))
        return y.YMap(tlist)

    def save(self, filename):
        f = open(filename, 'w')
        self._save(f)
        f.close()

    def _save(self, stream):
        '''
        Save the parset to a yaml file
        '''
    
        dumper = ry.SafeDumper(stream)
        dumper.open()
        dumper.serialize(self.ynode())
        dumper.close()

    def load(self, filename):
        '''
        Load the parset from a file
        '''
        f = open(filename)
        data = ry.safe_load(f)
        f.close()
        if not isinstance(data, dict):
            raise ValueError("file not of expected parameter format")
        vdict = self.value_dict()
        tdict = self.traits()
        for key in data:
            if key in vdict:
                vdict[key] = tdict[key].validate(self, data[key])

    def __str__(self):
        sf = six.StringIO()
        self._save(sf)
        pstring = sf.getvalue()
        sf.close()
        return pstring

class ParameterHandler:
    '''
    This class wraps a function (or any callable object) with a 
    ParSet instance so that it can use the ParSet to validate
    the values, and read and write such ParSets from and to 
    human editable files.
    '''
    def __init__(self, callable, parset):
        '''
        Callable is the function or callable object to be bound
        to the parset supplied. The result is an object that
        is also callable but uses the ParSet machinery.
        '''
        self.callable = callable # need to test if callable
        self.parset = parset 

    def __call__(self, parset=None, **kw):
        '''
        Currently requires all original parameters supplied as keywords.
        Takes an optional parset argument that is either a ParSet instance
        or a filename of a parameter file (full path not required if in
        the parameter file search path).
        '''
        if parset is not None:
            if isinstance(parset, ParSet):
                self.parset = parset 
            elif isinstance(parset, ""):
                pass
            else:
                raise ValueError(
                    "parset must be ParSet instance or parameter file name")
        vtraits = self.parset.value_dict()
        for key in kw:
            self.parset.__setattr__(key, kw[key])
        # now invoke original function
        return self.callable(**self.parset.value_dict())