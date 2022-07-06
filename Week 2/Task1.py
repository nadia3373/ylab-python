"""
Разработать программу для вычисления кратчайшего пути (https://github.com/mnv/python-basics).
"""


import copy, sys

costs = []
reduced_costs = []
rows = []
columns = []

def main():
    # Если при запуске программы было введено количество точек,
    # использовать его и запросить ввод координат для каждой точки
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
        destinations = {}
        for i in range(n):
            destination = input("Точка " + str(i + 1) + ": ").split()
            destination = tuple(destination)
            destinations[i] = destination
    # Иначе использовать данные по умолчанию
    else:
        # Координаты точек по умолчанию
        destinations = {0: (0, 2), 1: (2, 5), 2: (5, 2), 3: (6, 6), 4: (8, 3)}
        n = len(destinations)
    # Сохранить индексы точек
    for i in range(n):
        rows.append(i)
        columns.append(i)
    # Расчёт матрицы расстояний для каждой точки
    for i in destinations:
        cost = []
        for j in destinations:
            if not i == j:
                value = ((float(destinations[j][0]) - float(destinations[i][0])) ** 2 + (float(destinations[j][1]) - float(destinations[i][1])) ** 2) ** 0.5
            else:
                value = float("inf")
            cost.append(value)
        reduced_costs.append(cost)
    # Скопировать матрицу расстояний для расчёта длины пути в конце
    costs = copy.deepcopy(reduced_costs)
    # Сокращать матрицу до минимальной размерности, составляя маршрут методом ветвей и границ
    route = reduce_matrix()
    output = []
    # Сформировать маршрут по порядку
    for i in range(len(route)):
        if route[i][0] == 0:
            previous = route[i]
            output.append(previous)
            while len(output) < n:
                for j in range(len(route)):
                    if (route[j][0] == previous[1]) and (not route[j] in output):
                        output.append(route[j])
                        previous = route[j]
    # Упорядочить координаты точек согласно маршруту
    order = []
    for i in range(len(output)):
        if i == 0:
            order.append(destinations[i])
        else:
            for j in destinations:
                if j == output[i][0]:
                    order.append(destinations[j])
    order.append(destinations[0])
    # Записать длину каждого отрезка маршрута
    prices = []
    route_length = 0
    for i in range(len(output)):
        for j in range(len(costs)):
            for k in range(len(costs[j])):
                if j == output[i][0] and k == output[i][1]:
                    prices.append(costs[j][k])
    # Отобразить результат
    for i in range(len(order) - 1):
        temp = [prices[i]]
        if i == 0:
            route_length = temp
            print(str(order[i]), end = "")
        else:
            route_length[0] += temp[0]
        print(" --> " + str(order[i + 1]) + " " + str(route_length) + " ", end = "")
    print("= " + str(route_length[0]))

def least_value(list, excluded_value):
    min_value = float("inf")
    for i in range(len(list)):
        if (list[i] < min_value) and (not i == excluded_value):
            min_value = list[i]
    return min_value

def reduce_matrix():
    route = []
    while True:
        lower_bound = 0
        for i in range(len(reduced_costs)):
            least = min(reduced_costs[i])
            lower_bound += least
            for j in range(len(reduced_costs)):
                reduced_costs[i][j] -= least
        for i in range(len(reduced_costs)):
            least = min(cost[i] for cost in reduced_costs)
            lower_bound += least
            for j in range(len(reduced_costs)):
                reduced_costs[j][i] -= least
        max_bound = 0
        row = 0
        column = 0
        path = set()
        for i in range(len(reduced_costs)):
            for j in range(len(reduced_costs[i])):
                if reduced_costs[i][j] == 0:
                    bound = least_value(reduced_costs[i], j) + least_value((list(col[j] for col in reduced_costs)), i)
                    if bound > max_bound:
                        max_bound = bound
                        row = i
                        column = j
                        path = [rows[i], columns[j]]
        route.append(path)
        reduced_costs[column][row] = float("inf")
        del reduced_costs[row]
        for col in reduced_costs:
            del col[column]
        del rows[row]
        del columns[column]
        if len(reduced_costs) == 1:
            lock_element = set()
            lock_element = [rows[0], columns[0]]
            route.append(lock_element)
            return route

if __name__ == '__main__':
    main()
