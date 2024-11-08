def a(list_, item):
    low = 0
    high = len(list_) - 1
    while low <= high:
        mid = (low + high) // 2
        current_element = list_[mid]
        if current_element == item:
            return mid
        elif current_element > item:
            high = mid - 1
        else:
            low = mid + 1
    return None


print(a([1, 2, 3, 4], 5))
