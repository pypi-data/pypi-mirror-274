from dataclasses import dataclass
from typing import Generic, Iterable, Type, TypeVar

from apischema import ValidationError, deserialize, identity, serialize
from apischema.conversions import Conversion
from apischema.conversions.converters import default_deserialization, default_serialization
from ovld import TypeMap

T = TypeVar("T")


@dataclass(eq=False)
class Collection(Generic[T]):
    model: Type[T]
    strict: bool = False

    def query(self, s: str) -> Iterable[T]:
        raise NotImplementedError()

    def lookup(self, s: str) -> T:
        raise NotImplementedError()

    def describe(self, obj: T) -> str:
        raise NotImplementedError()


class MapCollection(Collection):
    def __init__(self, model, elements, strict=False):
        super().__init__(model=model, strict=strict)
        self.elements = elements
        self.reverse_lookup = {self.key(v): k for k, v in self.elements.items()}

    def key(self, obj):
        return obj

    def query(self, s):
        for k, v in self.elements:
            if s in k:
                yield v

    def lookup(self, s):
        try:
            return self.elements[s]
        except KeyError:
            raise ValidationError(f"Cannot resolve: '{s}'")

    def describe(self, obj):
        if (key := self.key(obj)) in self.reverse_lookup:
            return self.reverse_lookup[key]
        if self.strict:
            raise ValidationError("Can only serialize elements in the collection.")
        else:
            return obj


class CollectionAwareSerializer:
    def __init__(self, collections: list[Collection]):
        self.map = TypeMap()
        for c in collections:
            self.map.register(c.model, c)

    def _default_serialization(self, styp):
        try:
            coll = self.map[styp]
        except KeyError:
            return default_serialization(styp)
        coll = list(coll.keys())[0]
        return [
            Conversion(
                converter=coll.describe, source=styp, target=str | dict, sub_conversion=identity
            ),
        ]

    def _default_deserialization(self, dtyp):
        try:
            coll = self.map[dtyp]
        except KeyError:
            return default_deserialization(dtyp)
        coll = list(coll.keys())[0]
        conversion = Conversion(converter=coll.lookup, source=str, target=dtyp)
        if coll.strict:
            return [conversion]
        else:
            return [conversion, identity]

    def serialize(self, *args, **kwargs):
        return serialize(*args, default_conversion=self._default_serialization, **kwargs)

    def deserialize(self, *args, **kwargs):
        return deserialize(*args, default_conversion=self._default_deserialization, **kwargs)
