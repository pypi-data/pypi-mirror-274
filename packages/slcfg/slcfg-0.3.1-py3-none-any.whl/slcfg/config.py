import typing

from slcfg import item as itemlib
from slcfg import layer as layerlib


def read_config[T](
    model: typing.Callable[..., T],
    layers: list[layerlib.Layer],
    on_conflict: itemlib.ConflictPolicy | None = None,
):
    value_tree: itemlib.ValueTree = {}
    for layer in layers:
        for item in layer.getter():
            value_tree = itemlib.set_item(value_tree, item, on_conflict)

    return model(**value_tree)
