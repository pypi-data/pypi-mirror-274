from typing import Any


class Pair:
    """Pair data structure."""

    def __init__(self, first: Any = None, second: Any = None):
        self.__first: Any = first
        self.__second: Any = second

    def __str__(self):
        p: str = "Pair : <"
        if self.__first is not None and self.__second is not None:
            p += str(self.__first)
            p += ", "
            p += str(self.__second)
        return p + ">"

    def __repr__(self):
        return f"PyAlStruct.Pair({str(self)})"

    @property
    def first(self) -> Any:
        return self.__first

    @first.setter
    def first(self, data: Any) -> None:
        self.__first = data

    @property
    def second(self) -> Any:
        return self.__second

    @second.setter
    def second(self, data: Any) -> None:
        self.__second = data


def equals(pair1: Pair, pair2: Pair) -> bool:
    """
    Return True if pair1 and pair2 are equal, False otherwise.
    pair1 and pair2 are equal if they have the same second or they are both None.
    :param pair1: First pair to compare.
    :param pair2: Second pair to compare.
    :return: boolean -- True if pair1 and pair2 are equal, else False.
    """
    if pair1 is None and pair2 is None:
        return True
    if pair1 is None or pair2 is None:
        return False
    return pair1.second == pair2.second
