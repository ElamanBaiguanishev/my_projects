from collections import defaultdict, deque


def min_time_to_complete_processes(n, processes):
    # Построение графа и списка зависимостей
    adj_list = defaultdict(list)
    in_degree = [0] * (n + 1)
    process_time = [0] * (n + 1)

    # Заполняем данные
    for i in range(n):
        data = list(map(int, processes[i].split()))
        ti = data[0]
        process_time[i + 1] = ti
        for dependency in data[1:]:
            adj_list[dependency].append(i + 1)
            in_degree[i + 1] += 1

    # Поиск топологической сортировки с помощью BFS
    finish_time = [0] * (n + 1)
    queue = deque()

    # Инициализация начальных процессов (без зависимостей)
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
            finish_time[i] = process_time[i]

    # Топологическая сортировка и вычисление времени завершения
    while queue:
        current = queue.popleft()
        for neighbor in adj_list[current]:
            finish_time[neighbor] = max(finish_time[neighbor], finish_time[current] + process_time[neighbor])
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Минимальное время завершения всех процессов
    return max(finish_time)


# Пример использования
n = int(input().strip())
processes = [input().strip() for _ in range(n)]
print(min_time_to_complete_processes(n, processes))
