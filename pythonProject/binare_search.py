list = [1, 3, 5, 7, 9]


def binary_search(list_, item):
    low = 0
    high = len(list_) - 1
    while low <= high:
        mid = (low + high) // 2
        guess = list_[mid]
        if guess == item:
            return mid
        elif guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return None


print(binary_search(list, 9))
