from typing import Any


def _merge(arr: iter(Any), left_side: iter(Any), right_side: iter(Any)) -> None:
    i, j, k = 0, 0, 0
    while i < len(left_side) and j < len(right_side):
        if left_side[i] < right_side[j]:
            arr[k] = left_side[i]
            i += 1
        else:
            arr[k] = right_side[j]
            j += 1
        k += 1
    while i < len(left_side):
        arr[k] = left_side[i]
        i += 1
        k += 1
    while j < len(right_side):
        arr[k] = right_side[j]
        j += 1
        k += 1


def sort(arr: iter(Any)) -> iter(Any):
    """
    Perform quick sort on the input list 'arr' in-place.

    :param arr: The input list to be sorted.
    :return: arr -- The sorted array.
    """
    sorted_arr = arr.copy()
    if len(sorted_arr) > 1:
        mid = len(sorted_arr) // 2
        left_side = sorted_arr[:mid]
        right_side = sorted_arr[mid:]
        sort(left_side)
        sort(right_side)
        _merge(sorted_arr, left_side, right_side)
    return sorted_arr


# Example usage:
if __name__ == "__main__":
    my_list = [64, 34, 25, 12, 22, 11, 90]
    sorted_list = sort(my_list)

    print("Original List:", my_list)
    print("Sorted List:", sorted_list)
