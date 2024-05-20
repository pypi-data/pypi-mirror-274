""" Test for betterschema.core """

# pylint: disable=E1101, W0104, E1136, R0903, R0912, R0915
import unittest
from pprint import pprint

from betterschema import core


@core.schema
class Foo:
    """Foo schema"""

    foo1: str
    foo2: int
    foo3: bool
    foo4: list[str]
    foo5: core.optional[int]
    foo6: dict[str, int]

    @core.schema
    class EmbeddedSchema:
        """Embedded schema"""

        bar1: str
        bar2: int
        bar3: bool

    bar_instance: EmbeddedSchema


@core.watch((Foo, "foo1"), (Foo, "foo2"))
def watch_values(inst, name: str, old, new):
    """Watch values"""
    print(f"watch_values: {inst}.{name}, {old} -> {new}")
    if name == "foo1" and new == "hi":
        raise ValueError("foo1 cannot be 'hi'")


class TestSchema(unittest.TestCase):
    """Test core module"""

    def test_schema(self):
        """Test schema"""
        print(dir(Foo))
        try:
            foo_instance = Foo(
                {
                    "foo1": "hello",
                    "foo2": 0,
                }
            )
        except AttributeError as e:
            print("expected value: ", e)
        else:
            raise AssertionError("AttributeError not raised")
        foo_instance = Foo(
            {
                "foo1": "hello",
                "foo2": 0,
                "foo3": True,
                "foo4": ["a", "b", "c"],
                "foo6": {"a": 1, "b": 2},
                "bar_instance": Foo.EmbeddedSchema(
                    {
                        "bar1": "world",
                        "bar2": 20,
                        "bar3": False,
                    }
                ),
            }
        )
        # foo_instance = Foo()
        foo_instance.foo1 = "hello2"
        foo_instance.foo2 = 1
        foo_instance.foo3 = True
        foo_instance.foo6 = {"a": 1, "b": 2}

        pprint(core.__watches__)
        pprint(core.__schemas__)

        foo_instance.foo4 = ["a", "b", "c"]
        try:
            foo_instance.foo4 = ["a", "b", "c", 1]
        except TypeError as e:
            print("expected value: ", e)
        else:
            raise AssertionError("ValueError not raised")

        try:
            foo_instance.foo6 = {"a": 1, "b": 2, "c": "3"}
        except TypeError as e:
            print("expected value: ", e)
        else:
            raise AssertionError("ValueError not raised")

        foo_instance.bar_instance = {
            "bar1": "world",
            "bar2": 20,
            "bar3": False,
        }
        foo_instance.bar_instance.bar1 = "world2"
        foo_instance.bar_instance.bar2 = 30
        foo_instance.bar_instance.bar3 = True

        assert foo_instance.foo1 == "hello2"
        assert foo_instance.foo2 == 1
        assert foo_instance.foo3 is True
        assert foo_instance.foo4 == ["a", "b", "c"]
        assert foo_instance.bar_instance.bar1 == "world2"
        assert foo_instance.bar_instance.bar2 == 30
        assert foo_instance.bar_instance.bar3 is True

        try:
            foo_instance.foo1 = "world"
        except ValueError as e:
            # reraise the exception
            raise e

        try:
            foo_instance.foo1 = "hi"
        except ValueError as e:
            print("expected value: ", e)
        else:
            raise AssertionError("ValueError not raised")

        foo_instance << {"foo2": 1}
        assert foo_instance.foo2 == 1

        foo_instance << {"foo2": 2, "foo3": False}
        assert foo_instance.foo2 == 2
        assert foo_instance.foo3 is False

        foo_instance << {"foo4": ["d", "e", "f"]}
        assert foo_instance.foo4 == ["d", "e", "f"]

        foo_instance << {"bar_instance": {"bar1": "hello", "bar2": 10, "bar3": True}}
        assert foo_instance.bar_instance.bar1 == "hello"
        assert foo_instance.bar_instance.bar2 == 10
        assert foo_instance.bar_instance.bar3 is True

        try:
            foo_instance << {"random": "value"}
        except AttributeError as e:
            pass
        else:
            raise AssertionError("ValueError not raised")

        try:
            foo_instance << {"foo2": "value"}
        except TypeError as e:
            pass
        else:
            raise AssertionError("TypeError not raised")

        try:
            foo_instance << {"foo4": "value"}
        except TypeError as e:
            pass
        else:
            raise AssertionError("TypeError not raised")

        try:
            foo_instance << {"bar_instance": "value"}
        except TypeError as e:
            pass
        else:
            raise AssertionError("TypeError not raised")

        foo_instance << {"bar_instance": {"bar1": "hello", "bar2": 10, "bar3": True}}


if __name__ == "__main__":
    unittest.main()
