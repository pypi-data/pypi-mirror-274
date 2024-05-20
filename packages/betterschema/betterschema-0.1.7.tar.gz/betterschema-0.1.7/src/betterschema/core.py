""" core module """

# pylint: disable=E0401, E0611
import logging
from typing import Optional

from betterschema.baselib import __schemas__, __watches__
from betterschema.baselib import schema as baseschema
from betterschema.baselib import watch as basewatch

logger = logging.getLogger(__name__)


optional = Optional


def is_schema_instance(schema_instance):
    """Check if the schema instance is a schema instance."""
    if type(schema_instance).__name__ not in __schemas__:
        return False
    return type(schema_instance).__name__ in __schemas__


def _schema(cls):
    # make sure the cls is a class with __annotations__
    if not isinstance(cls, type):
        raise ValueError("schema must be a class")
    if not hasattr(cls, "__annotations__"):
        raise ValueError("schema must be a class with __annotations__")
    res = baseschema(cls)
    return res


def _watch(*args):
    # make sure the args is a list of tuples
    for arg in args:
        if not isinstance(arg, tuple):
            raise ValueError("args must be a list of tuples")
        # make sure the first element of the tuple is a class
        if not isinstance(arg[0], type):
            raise ValueError(
                "args must be a list of tuples with the first element as a class"
            )
        # make sure the second element of the tuple is a string
        if not isinstance(arg[1], str):
            raise ValueError(
                "args must be a list of tuples with the second element as a string"
            )

    def wrapper(func):
        return basewatch(list(args), func)

    return wrapper


schema = _schema
watch = _watch


__all__ = [
    "optional",
    "schema",
    "watch",
    "__watches__",
    "__schemas__",
    "is_schema_instance",
]
