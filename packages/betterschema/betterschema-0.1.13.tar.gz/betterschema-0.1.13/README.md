
# BetterSchema

BetterSchema is a schema validation and data watching framework for Python. It allows you to define data schemas, validate data against these schemas, and watch for changes in the data with custom watchers.

## Features

- **Schema Definition**: Easily define data schemas using type hints and decorators.
- **Data Validation**: Automatically validate data against the defined schemas.
- **Nested Schemas**: Support for nested schemas within data models.
- **Watchers**: Monitor changes to data attributes and perform custom actions.
- **Optional Fields**: Handle optional fields within your schemas.
- **Type Checking**: Enforce type constraints on data attributes.

## Installation

You can install BetterSchema via pip:

```sh
pip install betterschema
```

## Usage

### Defining Schemas

To define a schema, you can use the `@core.schema` decorator on a class definition. Inside the class, you can define the attributes of the schema using type hints. You can also define nested schemas within the main schema class.

```python
import betterschema.core as core

@core.schema
class Foo:
    foo1: str # String field
    foo2: int # Integer field
    foo3: bool # Boolean field
    foo4: list[str] # List of strings
    foo5: core.optional[int] # Optional field
    foo6: dict[str, int] # Dictionary field

    @core.schema
    class EmbeddedSchema:
        bar1: str
        bar2: int
        bar3: bool

    bar: EmbeddedSchema # Nested schema field
```

### Creating Instances

You can create instances of the schema by passing a dictionary with the required fields to the schema class constructor. The data will be validated against the schema automatically.

```python

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

# For nested schemas, you can also give a dictionary directly
foo = Foo({
    "foo1": "hello",
    "foo2": 0,
    "foo3": True,
    "foo4": ["a", "b", "c"],
    "foo6": {"a": 1, "b": 2},
    "bar": {
        "bar1": "world",
        "bar2": 20,
        "bar3": False,
    }
})

```

### Updating Values

You can update the values of the schema attributes directly. The data will be validated on each update.

```python

# Updating values
foo.foo1 = "hello2"
foo.foo2 = 1

# if you try to set an invalid value, it will raise an exception
foo.foo1 = 1  # This will raise a TypeError

# you can also specify a dictionary to update multiple values at once
# in order to do this, you need to use the `<<` operator
foo << {
    "foo1": "hello3",
    "foo2": 2,
}

# for nested schemas, you can update the whole schema at once 
foo.bar = {
    "bar1": "world2",
    "bar2": 30,
    "bar3": True,
}

# or use the `<<` operator to do partial updates

foo.bar << {
    "bar1": "world3",
    "bar2": 40,
}

```

### Watching Values

You can define watchers to monitor changes to specific attributes of the schema. Watchers are defined using the `@core.watch` decorator, which takes a tuple of the form `(schema_class, attribute_name)` as an argument.

```python

@core.watch((Foo, "foo1"), (Foo, "foo2"))
def watch_values(inst, name: str, old, new):
    print(f"watch_values: {inst}.{name}, {old} -> {new}")
    if name == "foo1" and new == "hi":
        raise ValueError("foo1 cannot be 'hi'")

```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License.

