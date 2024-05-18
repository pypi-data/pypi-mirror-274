import unittest
import betterschema.core as core
import typing as t

# import faulthandler

# faulthandler.enable()


@core.schema
class DEF:
    x: int
    y: str
    z: bool


@core.schema
class ABC:
    a: int
    b: str = 1
    c: bool
    # d: t.Optional[int]  # not supported yet
    e: DEF


class TestCore(unittest.TestCase):
    def test_libmodule(self):
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
        assert a.c == True
        print(a.e)
        assert a.e.x == 10
        assert a.e.y == "hello"
        assert a.e.z == True

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
