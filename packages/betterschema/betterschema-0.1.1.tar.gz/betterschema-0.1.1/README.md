
# betterschema

betterschema is a schema validation and data watching framework for Python. It allows you to define data schemas, validate data against these schemas, and watch for changes in the data with custom watchers.

## Features

- **Schema Definition**: Easily define data schemas using type hints and decorators.
- **Data Validation**: Automatically validate data against the defined schemas.
- **Nested Schemas**: Support for nested schemas within data models.
- **Watchers**: Monitor changes to data attributes and perform custom actions.
- **Optional Fields**: Handle optional fields within your schemas.
- **Type Checking**: Enforce type constraints on data attributes.

## Installation

You can install betterschema via pip:

```sh
pip install betterschema
```

## Usage

Here's a simple example of how to use betterschema:

```python
import betterschema.core as core

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

# Creating an instance of the schema
foo = Foo({
    "foo1": "hello",
    "foo2": 0,
    "foo3": True,
    "foo4": ["a", "b", "c"],
    "foo6": {"a": 1, "b": 2},
    "bar": Foo.EmbeddedSchema({
        "bar1": "world",
        "bar2": 20,
        "bar3": False,
    })
})

# Updating values
foo.foo1 = "hello2"
foo.foo2 = 1
foo.foo3 = True

# Checking values
assert foo.foo1 == "hello2"
assert foo.foo2 == 1
assert foo.foo3 == True

# Watching values
foo.foo1 = "hi"  # This will raise a ValueError
```

## Running Tests

You can run the included unit tests to ensure everything is working correctly:

```sh
python -m unittest discover
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License.

---

Feel free to adjust this README as per your specific requirements and add any additional sections you deem necessary.