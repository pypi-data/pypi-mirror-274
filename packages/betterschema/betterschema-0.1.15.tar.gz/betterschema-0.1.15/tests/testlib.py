""" Test the core module """

# pylint: disable=E1101, R0903, W0201
import unittest

from betterschema import core


@core.schema
class DEF:
    """DEF schema"""

    x: int
    y: str
    z: bool


@core.schema
class ABC:
    """ABC schema"""

    a: int
    b: str = 1
    c: bool
    # d: t.Optional[int]  # not supported yet
    e: DEF


class TestCore(unittest.TestCase):
    """Test core module"""

    def test_libmodule(self):
        """Test lib module"""
        print(str(ABC.__annotations__))

        a = ABC(
            {
                "a": 10,
                "b": "hello",
                "c": True,
                "e": {
                    "x": 10,
                    "y": "hello",
                    "z": True,
                },
            }
        )
        assert a.a == 10
        assert a.b == "hello"
        assert a.c is True
        print(a.e)
        assert a.e.x == 10
        assert a.e.y == "hello"
        assert a.e.z is True

        print(a.__annotations__)
        a.a = 10
        a.b = "hello"
        a.c = True

        try:
            a.nonexistent = 10
            assert False
        except AttributeError:
            pass

        print(a.a)
        print(a.b)
        print(a.c)

        try:
            a.a = "hello"
            assert False
        except TypeError:
            pass

        # a.abc = "world"


if __name__ == "__main__":
    unittest.main()
