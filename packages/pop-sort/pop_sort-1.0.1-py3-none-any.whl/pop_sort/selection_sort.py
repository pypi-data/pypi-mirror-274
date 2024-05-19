from .decorators import reverse_decorator


@reverse_decorator
def selection_sort(arr, **kwargs):
    """
    Implementation of selection sort algorithm
    :param arr: array to be sorted
    :param reverse: True if sorted array should be reversed
    :return: sorted array
    """
    for i in range(len(arr)):
        min_idx = i
        for j in range(i, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
