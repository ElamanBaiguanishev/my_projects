def a(list, item):
    low = 0
    high = len(list) - 1
    while low <= high:
        mid = (low + high) // 2
        elem = list[mid]
        if elem == item:
            return mid
        if elem > item:
            high = mid - 1
        else:
            low = mid + 1
    return None


print(a([1, 3, 4, 5, 6, 7, 9], 11))
