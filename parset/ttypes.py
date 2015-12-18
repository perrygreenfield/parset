# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
This is an Astropy affiliated package.
"""

import six
import traitlets as traits
from traitlets import (TraitType, TraitError, Undefined)

from  astropy import units as u
import ruamel.yaml as ry
import numpy as np
from . import pyaml as y

ustr = six.text_type

class Integer(TraitType):

    info_text = "Integer"

    def __init__(self, default_value=Undefined, comment='', **metadata):
        self.comment = comment
        super(Integer, self).__init__(default_value, **metadata)

    def validate(self, obj, value):
        if isinstance(value, int):
            return value
        elif np.isscalar(value) and isinstance(value, np.integer):
            return int(value)
        else:
            self.error(obj, value)

    def ynode(self, value):
        return y.YScalarInt(value)


class Quantity(TraitType):

    info_text = "requires an astropy quantity (i.e., with units)"

    def __init__(self, default_value=Undefined, unit=None,
        equivalency=None, comment='', **metadata):
        
        if isinstance(unit, u.UnitBase):
            self.unit = unit
        else:
            raise ValueError("must be instance of an astropy unit")
        self.equivalency = equivalency # xxx need to validate
        self.comment = comment
        super(Quantity, self).__init__( 
            default_value=default_value, **metadata)

    def validate(self, obj, value):
        if isinstance(value, u.Quantity):
            if self.unit.is_equivalent(value.unit, self.equivalency):
                return value
            raise TraitError("Provided Quantity doesn't have a compatible unit")
        else:
            self.error(obj, value)



class QuantityScalar(Quantity):

    info_text = "requires an astropy scalar quantity (i.e., with units)"

    def __init__(self, default_value=Undefined, unit=None,
                        equivalency=None, comment='', **metadata):
            super(QuantityScalar, self).__init__( 
                default_value=default_value, unit=unit, equivalency=equivalency,
                comment=comment, **metadata)

    def validate(self, obj, value):
        if isinstance(value, u.Quantity):
            if value.shape == ():            
                if self.unit.is_equivalent(value.unit, self.equivalency):
                    return value
                else:
                    raise TraitError("Provided Quantity doesn't have a compatible unit")
            else:
                raise TraitError("Provided Quantity isnt' a scalar")
        elif isinstance(value, ustr):
            parts = value.split(' ')
            if len(parts) < 2:
                raise TraitError("String missing units")
            try:
                num = float(parts[0])
                unit = u.Unit(' '.join(parts[1:]))
            except ValueError:
                raise ValueError("provided string can't be interpreted as quantity")
            return num * unit
        else:
            self.error(obj, value)

    def ynode(self, value):
        return y.YScalarStr(value)



