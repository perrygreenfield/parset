import ruamel.yaml as ry
import six

ustr = six.text_type

ypref = u'tag:yaml.org,2002:'

def YScalarInt(value):
    return ry.ScalarNode(tag=ypref+u'int', value=ustr(value))

def YScalarFloat(value):
    return ry.ScalarNode(tag=ypref+u'float', value=ustr(value))

def YScalarStr(value):
    return ry.ScalarNode(tag=ypref+u'str', value=ustr(value))

def YMap(vlist):
    return ry.MappingNode(tag=ypref+u'map', value=vlist)

def YSeq(kvlist):
    return ry.SequenceNode(tag=ypref+u'seq', value=kvlist)
