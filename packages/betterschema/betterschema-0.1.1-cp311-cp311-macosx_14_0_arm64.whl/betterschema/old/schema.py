import typing as t
import logging
from betterschema import baselib

logger = logging.getLogger(__name__)


def _class_fullname(cls: t.Type[t.Any]):
    return f"{cls.__module__}.{cls.__name__}"


def _get_attr_func(name):
    def getter(self):
        if self is None:
            return None
        return self.__dict__.get(name)

    return getter


def _set_attr_func(name):
    # TODO: check values before set
    def setter(self, value):
        # get the type of the attribute
        attr_type = self.__schema_annotations__.get(name)
        print(f"Setting {name} of type {attr_type}")
        origin = t.get_origin(attr_type)
        if t.get_origin(attr_type) is not None:
            # typing.List and typing.Mapping types
            if origin == list:
                # check if the value is a list
                if isinstance(value, list):
                    # get the type of the list
                    list_type = t.get_args(attr_type)[0]
                    # check if the list is empty
                    if len(value) == 0:
                        self.__dict__[name] = []
                    else:
                        # check if the list is of the correct type
                        if all(isinstance(i, list_type) for i in value):
                            self.__dict__[name] = value
                        else:
                            raise ValueError(f"{name} is not of type {list_type}")
                else:
                    raise ValueError(f"{name} is not a list")
            elif origin == dict:
                # check if the value is a dictionary
                if isinstance(value, dict):
                    # get the type of the dictionary
                    dict_type = t.get_args(attr_type)[1]
                    # check if the dictionary is empty
                    if len(value) == 0:
                        self.__dict__[name] = {}
                    else:
                        # check if the dictionary is of the correct type
                        if all(isinstance(i, dict_type) for i in value.values()):
                            self.__dict__[name] = value
                        else:
                            raise ValueError(f"{name} is not of type {dict_type}")
                else:
                    raise ValueError(f"{name} is not a dictionary")
        elif t.get_origin(attr_type) is None:
            # classes or primitives
            if hasattr(attr_type, "__schema_annotations__"):
                # dict to schema type
                if isinstance(value, dict):
                    if name not in self.__dict__:
                        # create an instance of the class
                        instance = attr_type()
                        # merge the dictionary with the instance
                        instance = _merge_dict(instance, value)
                        # set the attribute
                        self.__dict__[name] = instance
                    else:
                        # merge the dictionary with the instance
                        self.__dict__[name] = _merge_dict(self.__dict__[name], value)
                else:
                    # we cannot compare the type because we have modified the type
                    if _class_fullname(type(value)) != _class_fullname(attr_type):
                        raise ValueError(f"{name} is not of type {attr_type}")
                    self.__dict__[name] = value
            elif isinstance(value, attr_type):
                if name in self.__schema_checks__:
                    for check in self.__schema_checks__[name]:
                        if not check(value):
                            raise ValueError(f"Check failed for {name}")
                self.__dict__[name] = value
            else:
                raise ValueError(f"{name} is not of type {attr_type}")

    return setter


def _merge_dict(self, val: t.Dict[str, t.Any]):
    # TODO recurisvely do this.
    if not isinstance(val, dict):
        raise ValueError("Value is not a dictionary")
    for k, v in val.items():
        if hasattr(self, k):
            setattr(self, k, v)
        else:
            raise AttributeError(f"{k} is not defined")
    return self


def _to_string(self):
    keys = self.__schema_annotations__.keys()
    res = "{"
    for k in keys:
        if not isinstance(getattr(self, k), str):
            res += f'"{k}": {getattr(self, k).__str__()}, '
        else:
            res += f'"{k}": "{getattr(self, k)}", '
    res = res[:-2] + "}"
    return res


def define(cls: t.Type[t.Any]):
    attrs = {}
    inner_classes = {}

    for k, v in cls.__annotations__.items():
        print(k, str(v))
        attrs[k] = property(
            _get_attr_func(k),
            _set_attr_func(k),
            None,
            k,
        )

    # iterate all classes defined in the class
    for k in dir(cls):
        if hasattr(getattr(cls, k), "__annotations__"):
            inner_classes[k] = define(getattr(cls, k))

    attrs["__ilshift__"] = _merge_dict
    attrs["__str__"] = _to_string

    attrs["__schema_annotations__"] = cls.__annotations__
    attrs["__schema_checks__"] = {}
    for k, v in inner_classes.items():
        attrs[k] = v

    # create a class definition
    new_cls = type(cls.__name__, (object,), attrs)
    return new_cls


def check(cls: t.Type[t.Any], attr: property):
    assert isinstance(attr, property)

    def decorator(func):
        def wrapper(value):
            return func(value)

        if attr.__doc__ not in cls.__schema_checks__:
            cls.__schema_checks__[attr.__doc__] = []
        cls.__schema_checks__[attr.__doc__].append(wrapper)
        return wrapper

    return decorator
