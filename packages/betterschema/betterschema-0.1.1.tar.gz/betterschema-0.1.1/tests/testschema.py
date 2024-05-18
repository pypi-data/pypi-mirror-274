import betterschema.core as core
import typing as t
import unittest
from pprint import pprint

import faulthandler

faulthandler.enable()


@core.schema
class Foo:
    foo1: str
    foo2: int
    foo3: bool
    foo4: list[str]
    foo5: core.optional[int]
    foo6: dict[str, int]

    @core.schema
    class EmbeddedSchema:
        bar1: str
        bar2: int
        bar3: bool

    bar: EmbeddedSchema


@core.watch((Foo, "foo1"), (Foo, "foo2"))
def watch_values(inst, name: str, old, new):
    print(f"watch_values: {inst}.{name}, {old} -> {new}")
    if name == "foo1" and new == "hi":
        raise ValueError("foo1 cannot be 'hi'")


class TestSchema(unittest.TestCase):

    def test_schema(self):
        # not supported yet
        print(dir(Foo))
        try:
            foo = Foo(
                {
                    "foo1": "hello",
                    "foo2": 0,
                }
            )
        except AttributeError as e:
            print("expected value: ", e)
        else:
            raise AssertionError("AttributeError not raised")
        foo = Foo(
            {
                "foo1": "hello",
                "foo2": 0,
                "foo3": True,
                "foo4": ["a", "b", "c"],
                "foo6": {"a": 1, "b": 2},
                "bar": Foo.EmbeddedSchema(
                    {
                        "bar1": "world",
                        "bar2": 20,
                        "bar3": False,
                    }
                ),
            }
        )
        # foo = Foo()
        foo.foo1 = "hello2"
        foo.foo2 = 1
        foo.foo3 = True
        foo.foo6 = {"a": 1, "b": 2}

        pprint(core.__watches__)
        pprint(core.__schemas__)

        foo.foo4 = ["a", "b", "c"]
        try:
            foo.foo4 = ["a", "b", "c", 1]
        except TypeError as e:
            print("expected value: ", e)
        else:
            raise AssertionError("ValueError not raised")

        try:
            foo.foo6 = {"a": 1, "b": 2, "c": "3"}
        except TypeError as e:
            print("expected value: ", e)
        else:
            raise AssertionError("ValueError not raised")

        foo.bar = {
            "bar1": "world",
            "bar2": 20,
            "bar3": False,
        }
        foo.bar.bar1 = "world2"
        foo.bar.bar2 = 30
        foo.bar.bar3 = True

        assert foo.foo1 == "hello2"
        assert foo.foo2 == 1
        assert foo.foo3 == True
        assert foo.foo4 == ["a", "b", "c"]
        assert foo.bar.bar1 == "world2"
        assert foo.bar.bar2 == 30
        assert foo.bar.bar3 == True

        try:
            foo.foo1 = "world"
        except ValueError as e:
            raise AssertionError("ValueError not raised")

        try:
            foo.foo1 = "hi"
        except ValueError as e:
            print("expected value: ", e)
        else:
            raise AssertionError("ValueError not raised")

        foo << {"foo2": 1}
        assert foo.foo2 == 1

        foo << {"foo2": 2, "foo3": False}
        assert foo.foo2 == 2
        assert foo.foo3 == False

        foo << {"foo4": ["d", "e", "f"]}
        assert foo.foo4 == ["d", "e", "f"]

        foo << {"bar": {"bar1": "hello", "bar2": 10, "bar3": True}}
        assert foo.bar.bar1 == "hello"
        assert foo.bar.bar2 == 10
        assert foo.bar.bar3 == True

        try:
            foo << {"random": "value"}
        except AttributeError as e:
            pass
        else:
            raise AssertionError("ValueError not raised")

        try:
            foo << {"foo2": "value"}
        except TypeError as e:
            pass
        else:
            raise AssertionError("TypeError not raised")

        try:
            foo << {"foo4": "value"}
        except TypeError as e:
            pass
        else:
            raise AssertionError("TypeError not raised")

        try:
            foo << {"bar": "value"}
        except TypeError as e:
            pass
        else:
            raise AssertionError("TypeError not raised")

        foo << {"bar": {"bar1": "hello", "bar2": 10, "bar3": True}}


if __name__ == "__main__":
    unittest.main()
