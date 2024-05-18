from typing import Any

from al_struct.algorithms.sort.bubble import sort as bubblesort
from al_struct.algorithms.sort.insertion import sort as insertionsort
from al_struct.algorithms.sort.merge import sort as mergesort
from al_struct.algorithms.sort.quick import sort as quicksort
from al_struct.algorithms.sort.selection import sort as selectionsort


class BinarySearch:
    """
    Apply binary search for a target in an array.
    Default sort algorithm is selection sort.
    """
    def __init__(self, array: Any, sort: str = 'quick'):
        match sort:
            case 'bubble':
                self._array = bubblesort(array)
            case 'merge':
                self._array = mergesort(array)
            case 'quick':
                self._array = quicksort(array)
            case 'insertion':
                self._array = insertionsort(array)
            case 'selection':
                self._array = selectionsort(array)

    @property
    def array(self) -> Any:
        return self._array

    def exists(self, target: Any) -> bool:
        """
        Return boolean value about the existence of the target.
        :param target: The target to search for.
        :return: bool -- True if target exists, otherwise False.
        """
        left, right = 0, len(self._array) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if self._array[mid] == target:
                return True
            elif self._array[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return False

    def find_index(self, target: Any) -> int:
        """
        Return the index of target if exists in the array.
        :param target: The target to search for.
        :return: int -- The index of target if exists, otherwise return '-1'.
        """
        left, right = 0, len(self._array) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if self._array[mid] == target:
                return self._array.index(mid)
            elif self._array[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def find_element(self, target: Any) -> Any:
        """
        Return the element if exists in the array.
        :param target: The target to search for.
        :return: The element if exists, otherwise 'None'.
        """
        left, right = 0, len(self._array) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if self._array[mid] == target:
                return self._array[mid]
            elif self._array[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return None
