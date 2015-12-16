# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
This is an Astropy affiliated package.
"""

from traitlets import (TraitType, Integer, Int, Long, Float, Complex, CInt,
     CLong, CFloat, CComplex, Unicode, Bytes, CUnicode, CBytes, ObjectName,
     DottedObjectName, List, Set, Tuple, Dict, Instance, Type, This,
     ForwardDeclaredInstance, ForwardDeclaredType, Bool, CBool, Enum,
     CaselessStrEnum, TCPAddress, CRegExp, Union, Any, Undefined, TraitError)

from  astropy import units as u

class Quantity(TraitType):

    info_text = "requires an astropy quantity (i.e., with units)"

    def __init__(self, default_value=Undefined, unit=None,
        equivalency=None, **metadata):
        
        if isinstance(unit, u.UnitBase):
            self.unit = unit
        else:
            raise ValueError("must be instance of an astropy unit")
        self.equivalency = equivalency # xxx need to validate
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

    def validate(self, obj, value):
        if isinstance(value, u.Quantity):
            if value.shape == ():            
                if self.unit.is_equivalent(value.unit, self.equivalency):
                    return value
                else:
                    raise TraitError("Provided Quantity doesn't have a compatible unit")
            else:
                raise TraitError("Provided Quantity isnt' a scalar")
        else:
            self.error(obj, value)



