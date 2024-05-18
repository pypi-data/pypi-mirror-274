from enum import Enum
import betterschema.core as core
from pprint import pprint
import yaml
import json


class RenderType(Enum):
    JSON = 1
    YAML = 2


def render(schema_instance, render_type=RenderType.YAML):
    if not core.is_schema_instance(schema_instance):
        raise ValueError("Invalid schema instance")
    if render_type == RenderType.JSON:
        return render_json(schema_instance)
    elif render_type == RenderType.YAML:
        return render_yaml(schema_instance)
    else:
        raise ValueError("Invalid render type")


def object_to_dict(schema_instance):
    # create a dict from the keys listed in __annotations__
    schema_dict = {}
    for key in schema_instance.__annotations__:
        tmp = getattr(schema_instance, key)
        if core.is_schema_instance(tmp):
            tmp = object_to_dict(tmp)
        schema_dict[key] = tmp
    return schema_dict


def render_json(schema_instance) -> str:
    schema_dict = object_to_dict(schema_instance)
    json_str = json.dumps(schema_dict)
    # print(json_str)
    return json_str


def render_yaml(schema_instance) -> str:
    schema_dict = object_to_dict(schema_instance)
    yaml_str = yaml.dump(schema_dict)
    # print(yaml_str)
    return yaml_str
