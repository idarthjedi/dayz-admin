from __future__ import annotations # included to support self type reference in __init__ for parent classes
# see https://peps.python.org/pep-0563/


class Item:

    _name: str
    _filesource: str
    _parent: type[Item]
    _variants: list[type[Item]]

    def __init__(self, name: str, filesource: str, parent: type[Item] = None, variants: list[type[Item]] = None):
        self._name = name
        self._filesource = filesource
        self._parent = parent
        self._variants = variants

    @property
    def name(self) -> str:
        return self._name

    @property
    def filesource(self) -> str:
        return self._filesource

    @property
    def parent(self) -> type[Item]:
        return self._parent

    @parent.setter
    def parent(self, parent: type[Item]):
        self._parent = parent

    @property
    def variants(self) -> list[type[Item]]:
        return self._variants

    @variants.setter
    def variants(self, variants: list[type[Item]]):
        self._variants = variants

    @staticmethod
    def create_new(classname: str):

        return {
            "ClassName": classname,
            "MaxPriceThreshold": 0,
            "MinPriceThreshold": 0,
            "SellPricePercent": -1.0,
            "MaxStockThreshold": 1,
            "MinStockThreshold": 1,
            "QuantityPercent": -1,
            "SpawnAttachments": [],
            "Variants": []
        }
