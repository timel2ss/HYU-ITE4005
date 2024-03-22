import sys
from itertools import combinations

transactions: list = []
minimum_support: float = 0.
support_map: dict = dict()

def apriori(candidates: list):
    L: list = filter_by_minimum_support(candidates)
    k: int = 2
    while L:
        C: list = generate_candidates(L, k)
        L: list = filter_by_minimum_support(C)
        k += 1

def filter_by_minimum_support(candidates: list) -> list:
    global support_map
    L: set = set()
    for candidate in candidates:
        support: float = calculate_support(candidate)
        if support < minimum_support:
            continue
        support_map[candidate] = support
        L.add(candidate)
    return list(L)

def calculate_support(item_set: frozenset) -> float:
    count: int = 0
    for transaction in transactions:
        if item_set == item_set & transaction:
            count += 1
    return count / len(transactions) * 100

def generate_candidates(L: list, k: int) -> list:
    return prune(L, self_join(L, k), k)

def self_join(L: list, k: int) -> list:
    joined_item_sets: set = set()
    for (item_set1, item_set2) in combinations(L, 2):
        joined_item_set: frozenset = frozenset(item_set1) | frozenset(item_set2)
        if len(joined_item_set) < k:
            continue
        for item_set in combinations(joined_item_set, k):
            joined_item_sets.add(frozenset(item_set))
    return list(joined_item_sets)

def prune(L: list, item_sets: list, k: int) -> list:
    pruned_item_sets: set = set()
    for item_set in item_sets:
        is_prunable: bool = False
        for item in combinations(item_set, k - 1):
            if not frozenset(item) in L:
                is_prunable = True
                break
        if is_prunable:
            continue
        pruned_item_sets.add(item_set)
    return list(pruned_item_sets)

def powerset(item_set: frozenset) -> list:
    powerset: set = set()
    for i in range(1, len(item_set)):
        for item in combinations(item_set, i):
            powerset.add(frozenset(item))
    return list(powerset)

# Dev Environment: Windows 11, Python 3.11.5
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f'usage: python {sys.argv[0]} [minimum support(%)] [input file name] [output file name]')
        quit()
    
    minimum_support: float = float(sys.argv[1])
    input_file_name: str = sys.argv[2]
    output_file_name: str = sys.argv[3]

    with open(file = input_file_name, mode = 'rt') as input_file:
        total_item_set: set = set()
        while True:
            line: str = input_file.readline().strip()
            if not line:
                break

            transaction: frozenset = frozenset(map(int, line.split('\t')))
            for item in transaction:
                total_item_set.add(item)

            transactions.append(transaction)

        candidates: list = []
        for item_set in total_item_set:
            candidates.append(frozenset([item_set]))

        apriori(candidates)

    with open(file = output_file_name, mode = 'wt') as output_file:
        for item_set in support_map.keys():
            if len(item_set) < 2:
                continue

            support: str = format(support_map[item_set], '.2f')

            for x in powerset(item_set):
                str_of_x: str = ','.join(map(str, x))

                y = set(item_set) - set(x)
                str_of_y: str = ','.join(map(str, y))

                confidence: str = format(support_map[item_set] / support_map[x] * 100, '.2f')

                output_file.write(f'{{{str_of_x}}}\t{{{str_of_y}}}\t{support}\t{confidence}\n')
