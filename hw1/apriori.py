import sys
from itertools import combinations

transactions: list = []
minimum_support: float = 0.

def apriori(candidates: list) -> list:
    L: list = filter_by_minimum_support(candidates)
    k: int = 2
    U: list = L.copy()
    while L:
        C: list = generate_candidates(L, k)
        L: list = filter_by_minimum_support(C)
        for item_set in L:
            U.append(item_set)
        k += 1
    return U

def filter_by_minimum_support(candidates: list) -> list:
    return list(filter(
        lambda item_set: calculate_support(item_set) >= minimum_support,
        candidates
    ))

def calculate_support(item_set: tuple) -> float:
    count: int = 0
    for transaction in transactions:
        if set(item_set) == set(item_set) & set(transaction):
            count += 1
    return count / len(transactions)

def generate_candidates(L: list, k: int) -> list:
    return prune(L, self_join(L, k), k)

def self_join(L: list, k: int) -> list:
    joined_item_sets: set = set()
    for (item_set1, item_set2) in combinations(L, 2):
        joined_item_set: set = set(item_set1) | set(item_set2)
        if len(joined_item_set) < k:
            continue
        for item_set in combinations(joined_item_set, k):
            joined_item_sets.add(tuple(item_set))
    return joined_item_sets

def prune(L: list, item_sets: list, k: int) -> list:
    pruned_item_sets: set = set()
    for item_set in item_sets:
        is_prunable: bool = False
        for item in combinations(item_set, k - 1):
            if not item in L:
                is_prunable = True
                break
        if not is_prunable:
            pruned_item_sets.add(item_set)
    return pruned_item_sets

# Dev Environment: Windows 11, Python 3.11.5
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Execute with three arguments: minimum support(%), input file name, output file name")
        quit()
    
    minimum_support: float = int(sys.argv[1]) / 100
    input_file_name: str = sys.argv[2]
    output_file_name: str = sys.argv[3]

    with open(file = input_file_name, mode = 'r') as input_file:
        total_item_set: set = set()
        while True:
            line: str = input_file.readline().strip()
            if not line:
                break

            transaction: list = list(map(int, line.split('\t')))
            for item in transaction:
                total_item_set.add((item, ))

            transactions.append(transaction)
        
        print(apriori(list(total_item_set)))

    # output_file = open(file = output_file_name, mode = 'w')

