a1 = [-1, 3, 8, 2, 9, 5]
a2 = [4, 1, 2, 10, 5, 20]
target = 24

def get_couples(a1, a2, target):
    s1 = set(a1)
    s2 = set(a2)
    result = set()
    delta = 0
    while not(result):
        for el1 in a1:
            el2 = target - el1
            if el2+delta in a2:
                result.add((el1, el2+delta))
            if el2-delta in a2:
                result.add((el1, el2-delta))
        delta += 1
    return result

print(get_couples(a1, a2, target))