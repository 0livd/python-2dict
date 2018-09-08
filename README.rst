Python-todict
#############

Python-todict allows you to easily turn any python object into a dictionary.
It can then be easily serialized, to json for example.
The class of the object you want to convert needs to inherit from two mixin classes and hold an attribute listing the attributes to export.
List, dict, tuple and set attributes are supported and any attribute object that implements the mixins are recursively converted.

Usage
=====

    >>> from todict.mixins import ToDictMixin, FromDictMixin
    >>> class MyClass(ToDictMixin, FromDictMixin):
    ...     TO_SERIALIZE = ["my_attr"]
    ...     def __init__(self):
    ...         self.my_attr = "data"
    ...
    >>> MyClass().to_dict()
    {'my_attr': 'data'}
    >>> restored_obj = MyClass.from_dict({'my_attr': 'test'})
    >>> getattr(restored_obj, "my_attr")
    'test'

Launch tests
============

    >>> pip install -r requirements-dev.txt
    >>> tox

* **Python**: 2.7, 3.6.
