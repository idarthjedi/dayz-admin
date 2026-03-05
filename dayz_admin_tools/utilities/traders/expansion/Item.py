from __future__ import annotations

from typing import Optional


class Item:

    _name: str
    _filesource: str
    _parent: Optional[Item]
    _variants: Optional[list[Item]]

    def __init__(
        self,
        name: str,
        filesource: str,
        parent: Optional[Item] = None,
        variants: Optional[list[Item]] = None,
    ):
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
    def parent(self) -> Optional[Item]:
        return self._parent

    @parent.setter
    def parent(self, parent: Optional[Item]) -> None:
        self._parent = parent

    @property
    def variants(self) -> Optional[list[Item]]:
        return self._variants

    @variants.setter
    def variants(self, variants: Optional[list[Item]]) -> None:
        self._variants = variants

    @staticmethod
    def create_new(classname: str) -> dict:
        return {
            "ClassName": classname,
            "MaxPriceThreshold": 0,
            "MinPriceThreshold": 0,
            "SellPricePercent": -1.0,
            "MaxStockThreshold": 1,
            "MinStockThreshold": 1,
            "QuantityPercent": -1,
            "SpawnAttachments": [],
            "Variants": [],
        }
