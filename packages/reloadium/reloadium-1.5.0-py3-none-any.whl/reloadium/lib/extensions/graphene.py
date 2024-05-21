from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union

from reloadium.lib.extensions.extension import Extension
from reloadium.corium.objects import Action, Container, Object, Variable, obj_dc
from reloadium.corium.static_anal import symbols
from dataclasses import dataclass


__RELOADIUM__ = True


@dataclass(**obj_dc)
class OrderedType(Variable):
    TYPE_NAME = "OrderedType"

    @classmethod
    def is_candidate(cls, sym: symbols.Symbol, py_obj: Any, potential_parent: Container) -> bool:
        import graphene.utils.orderedtype

        if isinstance(py_obj, graphene.utils.orderedtype.OrderedType):
            return True

        return False

    def compare(self, against: Object) -> bool:
        if self.py_obj.__class__.__name__ != against.py_obj.__class__.__name__:
            return False

        left = dict(self.py_obj.__dict__)
        left.pop("creation_counter")

        right = dict(self.py_obj.__dict__)
        right.pop("creation_counter")

        ret = left == right
        return ret

    @classmethod
    def get_rank(cls) -> int:
        return 200


@dataclass
class Graphene(Extension):
    NAME = "Graphene"

    ALLOWED_IN_FREE = True

    def __post_init__(self) -> None:
        super().__post_init__()

    def get_objects(self) -> List[Type[Object]]:
        return [OrderedType]
